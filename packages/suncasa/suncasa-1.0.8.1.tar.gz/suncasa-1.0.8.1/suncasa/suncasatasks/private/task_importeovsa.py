from ...casa_compat import check_dependencies
check_dependencies()

import sys
import os
import numpy as np
import numpy.ma as ma
import scipy.constants as constants
import time
from astropy.time import Time
from eovsapy import util
from eovsapy import dump_tsys as dtsys
import aipy
from suncasa.eovsa import impteovsa as ipe

py3 = sys.version_info.major >= 3

from ...casa_compat import import_casatools, import_casatasks

tasks = import_casatasks('split', 'casalog')
split = tasks.get('split')
casalog = tasks.get('casalog')

tools = import_casatools(['tbtool', 'mstool', 'qatool', 'iatool'])
tbtool = tools['tbtool']
mstool = tools['mstool']
qatool = tools['qatool']
iatool = tools['iatool']
tb = tbtool()
ms = mstool()
qa = qatool()
ia = iatool()

c_external = False


# idbdir = os.getenv('EOVSAIDB')
#
# if not idbdir:
#     print('Environmental variable for EOVSA idb path not defined')
#     print('Use default path on pipeline')
#     idbdir = '/data1/eovsa/fits/IDB/'


def udb_corr_external(filelist, udbcorr_path, use_exist_udbcorr=False):
    import pickle
    udbcorr_script = os.path.join(udbcorr_path, 'udbcorr_ext.py')
    if os.path.exists(udbcorr_script):
        os.system('rm -rf {}'.format(udbcorr_script))
    udbcorr_file = os.path.join(udbcorr_path, 'udbcorr_tmp.pickle')

    if use_exist_udbcorr and os.path.exists(udbcorr_file):
        with open(udbcorr_file, 'rb') as sf:
            filelist = pickle.load(sf)
    else:
        if os.path.exists(udbcorr_file):
            os.system('rm -rf {}'.format(udbcorr_file))
        with open(udbcorr_file, 'wb') as sf:
            pickle.dump(filelist, sf)
        fi = open(udbcorr_script, 'wb')
        fi.write(b'import pickle \n')
        fi.write(b'import pipeline_cal as pc \n')
        fi.write(b'import sys \n')
        fi.write(b'syspath = sys.path \n')
        fi.write(b"sys.path = [l for l in syspath if 'casa' not in l] \n")
        line = "with open('{}', 'rb') as sf: \n".format(udbcorr_file)
        fi.write(line.encode())
        fi.write(b'    filelist = pickle.load(sf) \n')

        fi.write(b'filelist_tmp = [] \n')
        fi.write(b'for ll in filelist: \n')
        fi.write(b"    try: \n")
        line = "        filelist_tmp.append(pc.udb_corr(ll, outpath='{}/', calibrate=True, desat=True)) \n".format(
            udbcorr_path)
        fi.write(line.encode())
        fi.write(b"    except: \n")
        fi.write(b"        pass \n")
        fi.write(b'filelist = filelist_tmp \n')
        line = "with open('{}', 'wb') as sf: \n".format(udbcorr_file)
        fi.write(line.encode())
        fi.write(b'    pickle.dump(filelist,sf) \n')
        fi.close()

        udbcorr_shellscript = os.path.join(udbcorr_path, 'udbcorr_ext.csh')
        if os.path.exists(udbcorr_shellscript):
            os.system('rm -rf {}'.format(udbcorr_shellscript))
        fi = open(udbcorr_shellscript, 'wb')
        fi.write(b'#! /bin/tcsh -f \n')
        fi.write(b' \n')
        # fi.write('setenv PYTHONPATH "/home/user/test_svn/python:/common/python/current:/common/python" \n')
        fi.write(b'source /home/user/.cshrc \n')
        line = '/common/anaconda2/bin/python {} \n'.format(udbcorr_script)
        fi.write(line.encode())
        fi.close()

        os.system('/bin/tcsh {}'.format(udbcorr_shellscript))

        with open(udbcorr_file, 'rb') as sf:
            filelist = pickle.load(sf)

    if filelist == []:
        raise ValueError('udb_corr failed to return any results. Please check your calibration.')
    return filelist


def trange2filelist(trange=[], verbose=False):
    '''This finds all solar IDB files within a timerange;
       Required inputs:
       trange - can be 1) a single string or Time() object in UTC: use the entire day, e.g., '2017-08-01' or Time('2017-08-01')
                          if just a date, find all scans withing the same date in local time.
                          if a complete time stamp, find the local date first (which may be different from that provided,
                            and return all scans within that day
                       2) a range of Time(), e.g., Time(['2017-08-01 00:00','2017-08-01 23:00'])
                       3) None -- use current date Time.now()
    '''

    if trange:
        if type(trange) == list or type(trange) == str:
            try:
                trange = Time(trange)
            except:
                print('trange format not recognised. Abort....')
                return None
    else:
        print('Please give a time range. Abort....')
        return None
    # if type(trange) == Time:
    try:
        # if single Time object, the following line would report an error
        nt = len(trange)
        if len(trange) > 1:
            # more than one value
            trange = Time([trange[0], trange[-1]])
        else:
            # single value in a list
            trange = Time(np.array([-1.0, 1.0]) * 5 / 24. / 60. + trange[0].mjd, format='mjd')
    except:
        trange = Time(np.array([-1.0, 1.0]) * 5 / 24. / 60. + trange.mjd, format='mjd')

    t1 = trange[0].datetime
    t2 = trange[1].datetime
    daydelta = (t2.date() - t1.date()).days
    if t1.date() != t2.date():
        # End day is different than start day, so read and concatenate two fdb files
        info = dtsys.rd_fdb(trange[0])
        for ll in range(daydelta):
            info2 = dtsys.rd_fdb(Time(trange[0].mjd + ll + 1, format='mjd'))
            if info2:
                for key in info.keys():
                    info.update({key: np.append(info[key], info2[key])})
    else:
        # Both start and end times are on the same day
        info = dtsys.rd_fdb(trange[0])

    # remove empty items
    for k, v in info.items():
        info[k] = info[k][~(info[k] == '')]

    sidx = np.where(
        np.logical_and(info['SOURCEID'] == 'Sun', info['PROJECTID'] == 'NormalObserving') & np.logical_and(
            info['ST_TS'].astype(float) >= trange[0].lv,
            info['ST_TS'].astype(float) <= trange[
                1].lv))
    filelist = info['FILE'][sidx]
    if verbose:
        print(
            '{} file found in the time range from {} to {}: '.format(len(filelist), t1.strftime('%Y-%m-%d %H:%M:%S UT'),
                                                                     t2.strftime('%Y-%m-%d %H:%M:%S UT')))
    idbdir = util.get_idbdir(Time(t1))
    inpath = '{}/{}/'.format(idbdir, trange[0].datetime.strftime("%Y%m%d"))
    filelist = [inpath + ll for ll in filelist]
    return filelist


def importeovsa_iter(filelist, timebin, width, visprefix, nocreatms, modelms, doscaling, keep_nsclms, fileidx):
    '''

    '''

    filename = filelist[fileidx]
    uv = aipy.miriad.UV(filename)
    # try:
    msname0 = list(filename.split('/')[-1])
    msname = visprefix + ''.join(msname0) + '.ms'
    # try:
    # uv.select('antennae', 0, 1, include=True)
    # uv.select('polarization', -5, -5, include=True)

    if 'antlist' in uv.vartable:
        ants = uv['antlist'].replace('\x00', '')
        antlist = list(map(int, ants.split()))
    else:
        antlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    good_idx = np.where(uv['sfreq'] > 0)[0]

    nf = len(good_idx)
    npol = uv['npol']
    nants = uv['nants']
    source_id = uv['source'].replace('\x00', '')
    sfreq = uv['sfreq'][good_idx]
    sdf = uv['sdf'][good_idx]
    ra, dec = uv['ra'], uv['dec']
    nbl = int(nants * (nants - 1) / 2)
    bl2ord = ipe.bl_list2(nants)
    npairs = int(nbl + nants)

    timesall = []
    uv.rewind()
    for preamble, data in uv.all():
        uvw, t, (i, j) = preamble
        timesall.append(t)
    timesjd = np.unique(timesall)
    # except:
    #     pass

    uv.select('clear', -1, -1, include=True)
    times = ipe.jd2mjds(np.asarray(timesjd))
    inttime = np.median((times - np.roll(times, 1))[1:]) / 60  ## time in minutes
    inttimed = inttime / (24 * 60)  ## time in days

    time_steps = np.round((times[-1] - times[0]) / inttime / 60).astype(int) + 1
    # time_steps = len(timesall) / (npairs * npol)
    if len(times) != time_steps:
        ### This is to solve the timestamp glitch in idb files.
        ### The timestamps are supposed to be evenly spaced
        ### However, some idb files may miss a few timestamps in the evenly-spaced time grid.
        ### The step will map the the data to the evenly-spaced time grid.
        timesnew = np.linspace(times[0], times[-1], time_steps)
        timesnew[np.hstack([[0], np.cumsum(np.round(np.diff(times) / 60 / inttime))]).astype(int)] = times
        times = timesnew
    durtim = int(np.round((times[-1] - times[0]) / 60 + inttime))  ## time in minutes
    time0 = time.time()

    flag = np.ones((npol, nf, time_steps, npairs), dtype=bool)
    out = np.zeros((npol, nf, time_steps, npairs), dtype=np.complex64)  # Cross-correlations
    uvwarray = np.zeros((3, time_steps, npairs), dtype=float)
    chan_band = ipe.get_band(sfreq=sfreq, sdf=sdf, date=Time(uv['time'], format='jd'))
    nband = len(chan_band)

    uv.rewind()
    l = -1
    for preamble, data in uv.all():
        uvw, t, (i0, j0) = preamble
        i = antlist.index(i0 + 1)
        j = antlist.index(j0 + 1)
        if i > j:
            # Reverse order of indices
            j = antlist.index(i0 + 1)
            i = antlist.index(j0 + 1)
        # Assumes uv['pol'] is one of -5, -6, -7, -8
        k = -5 - uv['pol']
        l += 1
        mask0 = data.mask
        data = ma.masked_array(ma.masked_invalid(data), fill_value=0.0)
        try:
            tidx = np.where(np.abs(timesjd - t) < inttimed)[0][0]
        except:
            tidx = l / (npairs * npol)
        out[k, :, tidx, bl2ord[i0, j0]] = data.data
        flag[k, :, tidx, bl2ord[i0, j0]] = np.logical_or(data.mask, mask0)
        # if i != j:
        if k == 3:
            uvwarray[:, tidx, bl2ord[i0, j0]] = -uvw * constants.speed_of_light / 1e9

    nrows = time_steps * npairs
    if doscaling:
        out2 = out.copy()
        for i0 in antlist:
            for j0 in antlist:
                if i0 < j0:
                    i, j = i0 - 1, j0 - 1
                    out2[:, :, :, bl2ord[i, j]] = out[:, :, :, bl2ord[i, j]] / np.sqrt(
                        np.abs(out[:, :, :, bl2ord[i, i]]) * np.abs(out[:, :, :, bl2ord[j, j]]))
        out2 = out2.reshape(npol, nf, nrows)
        out2[np.isnan(out2)] = 0
        out2[np.isinf(out2)] = 0
    # out2 = ma.masked_array(ma.masked_invalid(out2), fill_value=0.0)
    out = out.reshape(npol, nf, nrows) * 1e4
    flag = flag.reshape(npol, nf, nrows)
    uvwarray = uvwarray.reshape(3, nrows)
    uvwarray = np.tile(uvwarray, (1, nband))
    sigma = np.ones((4, nrows), dtype=float) + 1
    sigma = np.tile(sigma, (1, nband))

    casalog.post('IDB File {0} is readed in --- {1:10.2f} seconds ---'.format(filename, (time.time() - time0)))

    if not nocreatms:
        modelms = ipe.creatms(filename, visprefix)
        os.system('mv {} {}'.format(modelms, msname))
    else:
        casalog.post('----------------------------------------')
        casalog.post('copying standard MS to {0}'.format(msname, (time.time() - time0)))
        casalog.post('----------------------------------------')
        os.system("rm -fr {}".format(msname))
        os.system("cp -r {} {}".format(modelms, msname))
        casalog.post('Standard MS is copied to {0} in --- {1:10.2f} seconds ---'.format(msname, (time.time() - time0)))

    tb.open(msname, nomodify=False)
    casalog.post('----------------------------------------')
    casalog.post("Updating the main table of {}".format(msname))
    casalog.post('----------------------------------------')
    for l, cband in enumerate(chan_band):
        time1 = time.time()
        # nchannels = len(cband['cidx'])
        for row in range(nrows):
            if not doscaling or keep_nsclms:
                datacell = out[:, cband['cidx'][0]:cband['cidx'][-1] + 1, row]
                rownr = int(row + l * nrows)
                tb.putcell('DATA', rownr, datacell)
            tb.putcell('FLAG', rownr, flag[:, cband['cidx'][0]:cband['cidx'][-1] + 1, row])
        casalog.post('---spw {0:02d} is updated in --- {1:10.2f} seconds ---'.format((l + 1), time.time() - time1))
    tb.putcol('UVW', uvwarray)
    tb.putcol('SIGMA', sigma)
    tb.putcol('WEIGHT', 1.0 / sigma ** 2)
    timearr = times
    timearr = timearr.reshape(1, time_steps, 1)
    timearr = np.tile(timearr, (nband, 1, npairs))
    timearr = timearr.reshape(nband * npairs * time_steps)
    tb.putcol('TIME', timearr)
    tb.putcol('TIME_CENTROID', timearr)
    scan_id = tb.getcol('SCAN_NUMBER')
    scan_id *= 0
    tb.putcol('SCAN_NUMBER', scan_id)
    colnames = tb.colnames()
    cols2rm = ["MODEL_DATA", "CORRECTED_DATA"]
    for l in range(len(cols2rm)):
        if cols2rm[l] in colnames:
            tb.removecols(cols2rm[l])
    tb.close()

    casalog.post('----------------------------------------')
    casalog.post("Updating the OBSERVATION table of {}".format(msname))
    casalog.post('----------------------------------------')
    tb.open(msname + '/OBSERVATION', nomodify=False)
    tb.putcol('TIME_RANGE', np.asarray([times[0] - 0.5 * inttime, times[-1] + 0.5 * inttime]).reshape(2, 1))
    tb.putcol('OBSERVER', ['EOVSA team'])
    tb.close()

    casalog.post('----------------------------------------')
    casalog.post("Updating the POINTING table of {}".format(msname))
    casalog.post('----------------------------------------')
    tb.open(msname + '/POINTING', nomodify=False)
    timearr = times.reshape(1, time_steps, 1)
    timearr = np.tile(timearr, (nband, 1, nants))
    timearr = timearr.reshape(nband * time_steps * nants)
    tb.putcol('TIME', timearr)
    tb.putcol('TIME_ORIGIN', timearr)  # - 0.5 * delta_time)
    direction = tb.getcol('DIRECTION')
    direction[0, 0, :] = ra
    direction[1, 0, :] = dec
    tb.putcol('DIRECTION', direction)
    target = tb.getcol('TARGET')
    target[0, 0, :] = ra
    target[1, 0, :] = dec
    tb.putcol('TARGET', target)
    tb.close()

    casalog.post('----------------------------------------')
    casalog.post("Updating the SOURCE table of {}".format(msname))
    casalog.post('----------------------------------------')
    tb.open(msname + '/SOURCE', nomodify=False)
    radec = tb.getcol('DIRECTION')
    radec[0], radec[1] = ra, dec
    tb.putcol('DIRECTION', radec)
    name = np.array([source_id], dtype='|S{0}'.format(len(source_id) + 1))
    tb.putcol('NAME', name)
    tb.close()

    casalog.post('----------------------------------------')
    casalog.post("Updating the DATA_DESCRIPTION table of {}".format(msname))
    casalog.post('----------------------------------------')
    tb.open(msname + '/DATA_DESCRIPTION/', nomodify=False)
    pol_id = tb.getcol('POLARIZATION_ID')
    pol_id *= 0
    tb.putcol('POLARIZATION_ID', pol_id)
    # spw_id = tb.getcol('SPECTRAL_WINDOW_ID')
    # spw_id *= 0
    # tb.putcol('SPECTRAL_WINDOW_ID', spw_id)
    tb.close()

    # casalog.post('----------------------------------------')
    # casalog.post("Updating the POLARIZATION table of {}".format(msname))
    # casalog.post('----------------------------------------')
    # tb.open(msname + '/POLARIZATION/', nomodify=False)
    # tb.removerows(rownrs=np.arange(1, nband, dtype=int))
    # tb.close()

    casalog.post('----------------------------------------')
    casalog.post("Updating the FIELD table of {}".format(msname))
    casalog.post('----------------------------------------')
    tb.open(msname + '/FIELD/', nomodify=False)
    delay_dir = tb.getcol('DELAY_DIR')
    delay_dir[0], delay_dir[1] = ra, dec
    tb.putcol('DELAY_DIR', delay_dir)
    phase_dir = tb.getcol('PHASE_DIR')
    phase_dir[0], phase_dir[1] = ra, dec
    tb.putcol('PHASE_DIR', phase_dir)
    reference_dir = tb.getcol('REFERENCE_DIR')
    reference_dir[0], reference_dir[1] = ra, dec
    tb.putcol('REFERENCE_DIR', reference_dir)
    name = np.array([source_id], dtype='|S{0}'.format(len(source_id) + 1))
    tb.putcol('NAME', name)
    tb.close()

    # FIELD: DELAY_DIR, PHASE_DIR, REFERENCE_DIR, NAME

    # del out, flag, uvwarray, uv, timearr, sigma
    # gc.collect()  #
    if doscaling:
        if keep_nsclms:
            msname_scl = visprefix + ''.join(msname0) + '_scl.ms'
            os.system('cp -r {} {}'.format(msname, msname_scl))
        else:
            msname_scl = msname
        tb.open(msname_scl, nomodify=False)
        casalog.post('----------------------------------------')
        casalog.post("Updating the main table of {}".format(msname_scl))
        casalog.post('----------------------------------------')
        for l, cband in enumerate(chan_band):
            time1 = time.time()
            for row in range(nrows):
                rownr = int(row + l * nrows)
                tb.putcell('DATA', rownr, out2[:, cband['cidx'][0]:cband['cidx'][-1] + 1, row])
            casalog.post('---spw {0:02d} is updated in --- {1:10.2f} seconds ---'.format((l + 1), time.time() - time1))
        tb.close()

    if not (timebin == '0s' and width == 1):
        msfile = msname + '.split'
        if doscaling:
            split(vis=msname_scl, outputvis=msname_scl + '.split', datacolumn='data', timebin=timebin, width=width,
                  keepflags=False)
            os.system('rm -rf {}'.format(msname_scl))
            msfile_scl = msname_scl + '.split'
        if not (doscaling and not keep_nsclms):
            split(vis=msname, outputvis=msname + '.split', datacolumn='data', timebin=timebin, width=width,
                  keepflags=False)
            os.system('rm -rf {}'.format(msname))
    else:
        msfile = msname
        if doscaling:
            msfile_scl = msname_scl
    casalog.post("finished in --- {:.1f} seconds ---".format(time.time() - time0))
    if doscaling:
        return [True, msfile, msfile_scl, durtim]
    else:
        return [True, msfile, durtim]


def importeovsa(idbfiles=None, ncpu=None, timebin=None, width=None, visprefix=None, udb_corr=True, nocreatms=None,
                doconcat=None, modelms=None,
                doscaling=False, keep_nsclms=False, use_exist_udbcorr=False):
    casalog.origin('importeovsa')

    if type(idbfiles) == Time:
        filelist = trange2filelist(idbfiles)
    else:
        # If input type is not Time, assume that it is the list of files to read
        filelist = idbfiles

    if type(filelist) == str:
        filelist = [filelist]

    filelist_tmp = []
    for ll in filelist:
        if not os.path.exists(ll):
            casalog.post("Warning: {} not exist.".format(ll))
        else:
            filelist_tmp.append(ll)

    filelist = filelist_tmp
    if not filelist:
        casalog.post("No file in idbfiles list exists. Abort.")
        return False

    for idx, ll in enumerate(filelist):
        if ll[-1] == '/':
            filelist[idx] = ll[:-1]

    if not visprefix:
        visprefix = './'
    else:
        if os.path.exists(visprefix):
            pass
        else:
            casalog.post("The output path {} does not exist. Abort.".format(visprefix))
            return False
    if not timebin:
        timebin = '0s'
    if not width:
        width = 1

    if udb_corr:
        from eovsapy.pipeline_cal import udb_corr
        udbcorr_path = visprefix + '/tmp_UDBcorr/'
        if not os.path.exists(udbcorr_path):
            os.makedirs(udbcorr_path)
        filelist_tmp = []
        for ll in filelist:
            try:
                filelist_tmp.append(udb_corr(ll, outpath='{}/'.format(udbcorr_path), calibrate=True, desat=True))
            except:
                pass

        if filelist_tmp == []:
            raise ValueError('udb_corr failed to return any results. Please check your calibration.')
        else:
            filelist = filelist_tmp
        # filelist = udb_corr_external(filelist, udbcorr_path, use_exist_udbcorr)

    if not modelms:
        if nocreatms:
            filename = filelist[0]
            modelms = ipe.creatms(filename, visprefix)
    else:
        if not os.path.exists(modelms):
            if nocreatms:
                filename = filelist[0]
                modelms = ipe.creatms(filename, visprefix)

    iterable = range(len(filelist))

    t0 = time.time()
    casalog.post('Perform importeovsa in parallel with {} CPUs...'.format(ncpu))

    if ncpu == 1:
        res = []
        for fidx, ll in enumerate(filelist):
            res.append(
                importeovsa_iter(filelist, timebin, width, visprefix, nocreatms, modelms, doscaling, keep_nsclms, fidx))
    if ncpu > 1:
        import multiprocessing as mprocs
        from functools import partial
        imppart = partial(importeovsa_iter, filelist, timebin, width, visprefix, nocreatms, modelms, doscaling,
                          keep_nsclms)
        pool = mprocs.Pool(ncpu)
        res = pool.map(imppart, iterable)
        pool.close()
        pool.join()

    # print res
    t1 = time.time()
    timelapse = t1 - t0
    print('It took %f secs to complete' % timelapse)

    # results = pd.DataFrame({'succeeded': [], 'msfile': [], 'durtim': []})
    # for r in res:
    #     results = results.append(pd.DataFrame({'succeeded': [r[0]], 'msfile': [r[1]], 'durtim': [r[2]]}))
    # try:
    succeeded = []
    msfile = []
    durtim = []
    if doscaling:
        msfile_scl = []
        for r in res:
            succeeded.append(r[0])
            msfile.append(r[1])
            msfile_scl.append(r[2])
            durtim.append(r[3])
        results = {'succeeded': succeeded, 'msfile': msfile, 'msfile_scl': msfile_scl, 'durtim': durtim}
    else:
        for r in res:
            succeeded.append(r[0])
            msfile.append(r[1])
            durtim.append(r[2])
        results = {'succeeded': succeeded, 'msfile': msfile, 'durtim': durtim}
    # except:
    #     print 'errors occurred when creating the output summary.'

    if udb_corr:
        os.system('rm -rf {}'.format(udbcorr_path))

    if doconcat:
        from suncasa.suncasatasks.private import task_concateovsa as ce
        msname = os.path.basename(filelist[0])
        durtim = int(np.array(results['durtim']).sum())
        if doscaling:
            msfiles = list(np.array(results['msfile_scl'])[np.where(np.array(results['succeeded']) == True)])
            if keep_nsclms:
                concatvis = visprefix + msname + '-{:d}m{}.ms'.format(durtim, '_scl')
            else:
                concatvis = visprefix + msname + '-{:d}m{}.ms'.format(durtim, '')
        else:
            msfiles = list(np.array(results['msfile'])[np.where(np.array(results['succeeded']) == True)])
            concatvis = visprefix + msname + '-{:d}m{}.ms'.format(durtim, '')
        ce.concateovsa(msfiles, concatvis, datacolumn='data', keep_orig_ms=True, cols2rm="model,corrected")
        return concatvis
    else:
        msfiles = list(np.array(results['msfile'])[np.where(np.array(results['succeeded']) == True)])
        return [str(m) for m in msfiles]
