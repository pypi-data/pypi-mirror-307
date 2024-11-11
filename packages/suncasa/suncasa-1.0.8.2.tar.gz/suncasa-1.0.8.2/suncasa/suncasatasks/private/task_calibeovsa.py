from ...casa_compat import check_dependencies
check_dependencies()

import platform
import matplotlib
if platform.system() == 'Linux':
    matplotlib.use('Agg')
import os
import shutil
import numpy as np

from eovsapy.util import extract as eoextract
from eovsapy.util import Time
from eovsapy import cal_header as ch
from eovsapy import dbutil as db
from eovsapy import pipeline_cal as pc
from eovsapy.sqlutil import sql2refcalX, sql2phacalX
from .. import concateovsa

from ...casa_compat import import_casatools, import_casatasks

tasks = import_casatasks('split', 'tclean', 'gencal', 'clearcal', 'applycal', 'flagdata', 'casalog', 'bandpass')
split = tasks.get('split')
tclean = tasks.get('tclean')
gencal = tasks.get('gencal')
clearcal = tasks.get('clearcal')
applycal = tasks.get('applycal')
flagdata = tasks.get('flagdata')
casalog = tasks.get('casalog')
bandpass = tasks.get('bandpass')

tools = import_casatools(['tbtool', 'mstool', 'qatool', 'iatool'])

tbtool = tools['tbtool']
mstool = tools['mstool']
qatool = tools['qatool']
iatool = tools['iatool']
tb = tbtool()
ms = mstool()
qa = qatool()
ia = iatool()

def calibeovsa(vis=None, caltype=None, caltbdir='', interp=None, docalib=True, doflag=True, flagant='13~15',
               doimage=False, imagedir=None, antenna=None, timerange=None, spw=None, stokes=None, dosplit=False,
               outputvis=None, doconcat=False, concatvis=None, keep_orig_ms=True):
    '''

    :param vis: EOVSA visibility dataset(s) to be calibrated 
    :param caltype:
    :param interp:
    :param docalib:
    :param qlookimage:
    :param flagant:
    :param stokes:
    :param doconcat:
    :return:
    '''

    if type(vis) == str:
        vis = [vis]

    for idx, f in enumerate(vis):
        if f[-1] == '/':
            vis[idx] = f[:-1]
        vis[idx] = str(vis[idx])

    # check if the calibration table directory is defined
    # pipeline should always use "caltbdir = /data1/eovsa/caltable/"
    if not caltbdir:
        print('Task calibeovsa')
        print('Path for generating calibration tables not defined')
        print('Use current path')
        caltbdir = './'

    for msfile in vis:
        casalog.origin('calibeovsa')
        if not caltype:
            casalog.post("Caltype not provided. Perform reference phase calibration and daily phase calibration.")
            caltype = ['refpha', 'phacal']  ## use this line after the phacal is applied  # caltype = ['refcal']
        if not os.path.exists(msfile):
            casalog.post("Input visibility does not exist. Aborting...")
            continue
        if msfile.endswith('/'):
            msfile = msfile[:-1]
        if not msfile[-3:] in ['.ms', '.MS']:
            casalog.post("Invalid visibility. Please provide a proper visibility file ending with .ms")
        # if not caltable:
        #    caltable=[os.path.basename(vis).replace('.ms','.'+c) for c in caltype]

        # get band information
        tb.open(msfile + '/SPECTRAL_WINDOW')
        nspw = tb.nrows()
        bdname = tb.getcol('NAME')
        bd_nchan = tb.getcol('NUM_CHAN')
        bd = [int(b[4:]) - 1 for b in bdname]
        reffreqs = tb.getcol('REF_FREQUENCY')
        bandwidths = tb.getcol('TOTAL_BANDWIDTH')
        chan_freqs_spw0 = tb.getcol('CHAN_FREQ', startrow=0, nrow=1)
        cfreq_spw0 = np.mean(chan_freqs_spw0)

        tb.close()
        tb.open(msfile + '/ANTENNA')
        nant = tb.nrows()
        antname = tb.getcol('NAME')
        antlist = [str(ll) for ll in range(len(antname) - 1)]
        antennas = ','.join(antlist)
        tb.close()

        # get time stamp, use the beginning of the file
        tb.open(msfile + '/OBSERVATION')
        trs = {'BegTime': [], 'EndTime': []}
        for ll in range(tb.nrows()):
            tim0, tim1 = Time(tb.getcell('TIME_RANGE', ll) / 24 / 3600, format='mjd')
            trs['BegTime'].append(tim0)
            trs['EndTime'].append(tim1)
        tb.close()
        trs['BegTime'] = Time(trs['BegTime'])
        trs['EndTime'] = Time(trs['EndTime'])
        btime = np.min(trs['BegTime'])
        etime = np.max(trs['EndTime'])
        # ms.open(vis)
        # summary = ms.summary()
        # ms.close()
        # btime = Time(summary['BeginTime'], format='mjd')
        # etime = Time(summary['EndTime'], format='mjd')
        ## stop using ms.summary to avoid conflicts with importeovsa
        t_mid = Time((btime.mjd + etime.mjd) / 2., format='mjd')
        print("This scan observed from {} to {} UTC".format(btime.iso, etime.iso))
        gaintables = []
        spwmaps = []

        if ('refpha' in caltype) or ('refamp' in caltype) or ('refcal' in caltype):
            refcal = sql2refcalX(btime)
            pha = refcal['pha']  # shape is 15 (nant) x 2 (npol) x 34 (nband)
            pha[np.where(refcal['flag'] == 1)] = 0.
            amp = refcal['amp']
            amp[np.where(refcal['flag'] == 1)] = 1.
            t_ref = refcal['timestamp']
            # find the start and end time of the local day when refcal is registered
            try:
                dhr = t_ref.LocalTime.utcoffset().total_seconds() / 60. / 60.
            except:
                dhr = -7.
            bt = Time(np.fix(t_ref.mjd + dhr / 24.) - dhr / 24., format='mjd')
            et = Time(bt.mjd + 1., format='mjd')
            (yr, mon, day) = (bt.datetime.year, bt.datetime.month, bt.datetime.day)
            dirname = caltbdir + str(yr) + str(mon).zfill(2) + '/'
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            # check if there is any ROACH reboot between the reference calibration found and the current data
            t_rbts = db.get_reboot(Time([t_ref, btime]))
            if not t_rbts:
                casalog.post("Reference calibration is derived from observation at " + t_ref.iso)
                print("Reference calibration is derived from observation at " + t_ref.iso)
            else:
                casalog.post(
                    "Oh crap! Roach reboot detected between the reference calibration time " + t_ref.iso + ' and the current observation at ' + btime.iso)
                casalog.post("Aborting...")
                print(
                    "Oh crap! Roach reboot detected between the reference calibration time " + t_ref.iso + ' and the current observation at ' + btime.iso)
                print("Aborting...")

            para_pha = []
            para_amp = []
            calpha = np.zeros((nspw, nant - 1, 2))
            calamp = np.zeros((nspw, nant - 1, 2))
            for s in range(nspw):
                for n in range(nant - 1):
                    for p in range(2):
                        calpha[s, n, p] = pha[n, p, bd[s]]
                        calamp[s, n, p] = amp[n, p, bd[s]]
                        para_pha.append(np.degrees(pha[n, p, bd[s]]))
                        para_amp.append(amp[n, p, bd[s]])

        if 'fluxcal' in caltype:
            calfac = pc.get_calfac(Time(t_mid.iso.split(' ')[0] + 'T23:59:59'))
            t_bp = Time(calfac['timestamp'], format='lv')
            if int(t_mid.mjd) == int(t_bp.mjd):
                accalfac = calfac['accalfac']  # (ant x pol x freq)
                # tpcalfac = calfac['tpcalfac']  # (ant x pol x freq)
                caltb_autoamp = dirname + t_bp.isot[:-4].replace(':', '').replace('-', '') + '.bandpass'
                if not os.path.exists(caltb_autoamp):
                    bandpass(vis=msfile, caltable=caltb_autoamp, solint='inf', refant='eo01', minblperant=0, minsnr=0,
                             bandtype='B', docallib=False)
                    tb.open(caltb_autoamp, nomodify=False)  # (ant x spw)
                    bd_chanidx = np.hstack([[0], bd_nchan.cumsum()])
                    for ll in range(nspw):
                        antfac = np.sqrt(accalfac[:, :, bd_chanidx[ll]:bd_chanidx[ll + 1]])
                        # # antfac *= tpcalfac[:, :,bd_chanidx[ll]:bd_chanidx[ll + 1]]
                        antfac = np.moveaxis(antfac, 0, 2)
                        cparam = np.zeros((2, bd_nchan[ll], nant))
                        cparam[:, :, :-3] = 1.0 / antfac
                        tb.putcol('CPARAM', cparam + 0j, ll * nant, nant)
                        paramerr = tb.getcol('PARAMERR', ll * nant, nant)
                        paramerr = paramerr * 0
                        tb.putcol('PARAMERR', paramerr, ll * nant, nant)
                        bpflag = tb.getcol('FLAG', ll * nant, nant)
                        bpant1 = tb.getcol('ANTENNA1', ll * nant, nant)
                        bpflagidx, = np.where(bpant1 >= 13)
                        bpflag[:] = False
                        bpflag[:, :, bpflagidx] = True
                        tb.putcol('FLAG', bpflag, ll * nant, nant)
                        bpsnr = tb.getcol('SNR', ll * nant, nant)
                        bpsnr[:] = 100.0
                        bpsnr[:, :, bpflagidx] = 0.0
                        tb.putcol('SNR', bpsnr, ll * nant, nant)
                    tb.close()
                    msg_prompt = "Scaling calibration is derived for {}.".format(msfile)
                    casalog.post(msg_prompt)
                    print(msg_prompt)
                gaintables.append(caltb_autoamp)
                spwmaps.append([])
            else:
                msg_prompt = "Caution: No TPCAL is available on {}. No scaling calibration is derived for {}.".format(
                    t_mid.datetime.strftime('%b %d, %Y'), msfile)
                casalog.post(msg_prompt)
                print(msg_prompt)

        if ('refpha' in caltype) or ('refcal' in caltype):
            # caltb_pha = os.path.basename(vis).replace('.ms', '.refpha')
            # check if the calibration table already exists
            caltb_pha = dirname + t_ref.isot[:-4].replace(':', '').replace('-', '') + '.refpha'
            if not os.path.exists(caltb_pha):
                gencal(vis=msfile, caltable=caltb_pha, caltype='ph', antenna=antennas, pol='X,Y',
                       spw='0~' + str(nspw - 1), parameter=para_pha)
                tb.open(caltb_pha, nomodify=False)
                phaflag_ = refcal['flag'][:, :, np.array(bd)]
                phaflag_new = np.full((nant, 2, nspw), True, dtype=np.bool_)
                phaflag_new[:-1, ...] = phaflag_
                phaflag_new = np.moveaxis(phaflag_new, 0, 2).reshape(2, 1, nant * nspw)
                tb.putcol('FLAG', phaflag_new)
                tb.close()

                # tb.open(caltb_pha, nomodify=False)
                # phaparam = np.angle(tb.getcol('CPARAM'),deg=True)
                # phaparam_ = np.degrees(refcal['pha'][:,:,np.array(bd)])
                # phaparam2 = np.zeros((nant, 2, nspw))
                # phaparam2[:-1,...] = phaparam_
                # # phaparam2 = phaparam2.swapaxes(0,1).reshape(2,1,nant*nspw)
                # phaparam2 = np.moveaxis(phaparam2,0,2).reshape(2,1,nant*nspw)
                # tb.close()

            gaintables.append(caltb_pha)
            spwmaps.append([])
        if ('refamp' in caltype) or ('refcal' in caltype):
            # caltb_amp = os.path.basename(vis).replace('.ms', '.refamp')
            caltb_amp = dirname + t_ref.isot[:-4].replace(':', '').replace('-', '') + '.refamp'
            if not os.path.exists(caltb_amp):
                gencal(vis=msfile, caltable=caltb_amp, caltype='amp', antenna=antennas, pol='X,Y',
                       spw='0~' + str(nspw - 1), parameter=para_amp)
                tb.open(caltb_amp, nomodify=False)
                ampflag_ = refcal['flag'][:, :, np.array(bd)]
                ampflag_new = np.full((nant, 2, nspw), True, dtype=np.bool_)
                ampflag_new[:-1, ...] = ampflag_
                ampflag_new = np.moveaxis(ampflag_new, 0, 2).reshape(2, 1, nant * nspw)
                tb.putcol('FLAG', ampflag_new)
                tb.close()
            gaintables.append(caltb_amp)
            spwmaps.append([])

        # calibration for the change of delay center between refcal time and beginning of scan -- hopefully none!
        xml, buf = ch.read_calX(4, t=[t_ref, btime], verbose=False)
        if buf is not None:
            dly_t2 = Time(eoextract(buf[0], xml['Timestamp']), format='lv')
            dlycen_ns2 = eoextract(buf[0], xml['Delaycen_ns'])[:nant - 1]
            xml, buf = ch.read_calX(4, t=t_ref)
            dly_t1 = Time(eoextract(buf, xml['Timestamp']), format='lv')
            dlycen_ns1 = eoextract(buf, xml['Delaycen_ns'])[:nant - 1]
            dlycen_ns_diff = dlycen_ns2 - dlycen_ns1
            for n in range(2):
                dlycen_ns_diff[:, n] -= dlycen_ns_diff[0, n]
            print('Multi-band delay is derived from delay center difference at {} & {}'.format(dly_t1.iso, dly_t2.iso))
            dlycen_pha0 = np.degrees(dlycen_ns_diff * 1e-9 * cfreq_spw0 * 2. * np.pi)
            # print('=====Delays relative to Ant 14=====')
            # for i, dl in enumerate(dlacen_ns_diff[:, 0] - dlacen_ns_diff[13, 0]):
            #     ant = antlist[i]
            #     print 'Ant eo{0:02d}: x {1:.2f} ns & y {2:.2f} ns'.format(int(ant) + 1, dl
            #           dlacen_ns_diff[i, 1] - dlacen_ns_diff[13, 1])
            # caltb_mbd0 = os.path.basename(vis).replace('.ms', '.mbd0')
            caltb_dlycen = dirname + dly_t2.isot[:-4].replace(':', '').replace('-', '') + '.dlycen'
            caltb_dlycen_pha0 = dirname + dly_t2.isot[:-4].replace(':', '').replace('-', '') + '.dlycen_pha0'
            if not os.path.exists(caltb_dlycen):
                gencal(vis=msfile, caltable=caltb_dlycen, caltype='mbd', pol='X,Y', antenna=antennas,
                       parameter=dlycen_ns_diff.flatten().tolist())
            if not os.path.exists(caltb_dlycen_pha0):
                gencal(vis=msfile, caltable=caltb_dlycen_pha0, caltype='ph', pol='X,Y', antenna=antennas,
                       parameter=dlycen_pha0.flatten().tolist())
            gaintables.append(caltb_dlycen)
            spwmaps.append(nspw * [0])
            gaintables.append(caltb_dlycen_pha0)
            spwmaps.append(nspw * [0])

        if 'phacal' in caltype:
            phacals = np.array(sql2phacalX([bt, et], neat=True, verbose=False))
            if not phacals.any() or len(phacals) == 0:
                print("Found no phacal records in SQL database, will skip phase calibration")
            else:
                # first generate all phacal calibration tables if not already exist
                t_phas = Time([phacal['t_pha'] for phacal in phacals])
                # sort the array in ascending order by t_pha
                sinds = t_phas.mjd.argsort()
                t_phas = t_phas[sinds]
                phacals = phacals[sinds]
                caltbs_phambd = []
                caltbs_phambd_pha0 = []
                for i, phacal in enumerate(phacals):
                    # filter out phase cals with reference time stamp >30 min away from the provided refcal time
                    if (phacal['t_ref'].jd - refcal['timestamp'].jd) > 30. / 1440.:
                        del phacals[i]
                        del t_phas[i]
                        continue
                    else:
                        t_pha = phacal['t_pha']
                        phambd_ns = phacal['pslope']
                        for n in range(2):
                            phambd_ns[:, n] -= phambd_ns[0, n]
                        # set all flagged values to be zero
                        phambd_ns[np.where(phacal['flag'] == 1)] = 0.
                        caltb_phambd = dirname + t_pha.isot[:-4].replace(':', '').replace('-', '') + '.phambd'
                        caltbs_phambd.append(caltb_phambd)
                        if not os.path.exists(caltb_phambd):
                            gencal(vis=msfile, caltable=caltb_phambd, caltype='mbd', pol='X,Y', antenna=antennas,
                                   parameter=phambd_ns.flatten().tolist())

                        # When applying the multi-band delays, they are referenced to the center of spw 0
                        # Make a corresponding calibration table for the reference phase at the center of spw 0
                        pha0 = np.degrees(phambd_ns * 1e-9 * cfreq_spw0 * 2. * np.pi)
                        caltb_phambd_pha0 = dirname + t_pha.isot[:-4].replace(':', '').replace('-', '') + '.phambd_pha0'
                        caltbs_phambd_pha0.append(caltb_phambd_pha0)
                        if not os.path.exists(caltb_phambd_pha0):
                            gencal(vis=msfile, caltable=caltb_phambd_pha0, caltype='ph', pol='X,Y', antenna=antennas,
                                   parameter=pha0.flatten().tolist())

                # now decides which table to apply depending on the interpolation method ("nearest" or "linear")
                if interp == 'nearest':
                    tbind = np.argmin(np.abs(t_phas.mjd - t_mid.mjd))
                    dt = np.min(np.abs(t_phas.mjd - t_mid.mjd)) * 24.
                    print("Selected nearest phase calibration table at " + t_phas[tbind].iso)
                    gaintables.append(caltbs_phambd[tbind])
                    spwmaps.append(nspw * [0])
                    gaintables.append(caltbs_phambd_pha0[tbind])
                    spwmaps.append(nspw * [0])
                if interp == 'linear':
                    # bphacal = sql2phacalX(btime)
                    # ephacal = sql2phacalX(etime,reverse=True)
                    bt_ind, = np.where(t_phas.mjd < btime.mjd)
                    et_ind, = np.where(t_phas.mjd > etime.mjd)
                    if len(bt_ind) == 0 and len(et_ind) == 0:
                        print("No phacal found before or after the ms data within the day of observation")
                        print("Skipping daily phase calibration")
                    elif len(bt_ind) > 0 and len(et_ind) == 0:
                        gaintables.append(caltbs_phambd[bt_ind[-1]])
                        spwmaps.append(nspw * [0])
                        gaintables.append(caltbs_phambd_pha0[bt_ind[-1]])
                        spwmaps.append(nspw * [0])
                    elif len(bt_ind) == 0 and len(et_ind) > 0:
                        gaintables.append(caltbs_phambd[et_ind[0]])
                        spwmaps.append(nspw * [0])
                        gaintables.append(caltbs_phambd_pha0[et_ind[0]])
                        spwmaps.append(nspw * [0])
                    elif len(bt_ind) > 0 and len(et_ind) > 0:
                        bphacal = phacals[bt_ind[-1]]
                        ephacal = phacals[et_ind[0]]
                        # generate a new table interpolating between two daily phase calibrations
                        dt_obs = t_mid.mjd - bphacal['t_pha'].mjd
                        dt_pha = ephacal['t_pha'].mjd - bphacal['t_pha'].mjd
                        phambd_diff = ephacal['pslope'] - bphacal['pslope']
                        phambd_ns = bphacal['pslope'] + dt_obs / dt_pha * phambd_diff
                        for n in range(2):
                            phambd_ns[:, n] -= phambd_ns[0, n]
                        # set all flagged values to be zero
                        phambd_ns[np.where(bphacal['flag'] == 1)] = 0.
                        phambd_ns[np.where(ephacal['flag'] == 1)] = 0.
                        caltb_phambd_interp = dirname + t_mid.isot[:-4].replace(':', '').replace('-',
                                                                                                 '') + '.phambd'
                        caltb_phambd_interp_pha0 = caltb_phambd_interp + '_pha0'
                        pha0 = np.degrees(phambd_ns * 1e-9 * cfreq_spw0 * 2. * np.pi)
                        if not os.path.exists(caltb_phambd_interp):
                            gencal(vis=msfile, caltable=caltb_phambd_interp, caltype='mbd', pol='X,Y', antenna=antennas,
                                   parameter=phambd_ns.flatten().tolist())
                        if not os.path.exists(caltb_phambd_interp_pha0):
                            gencal(vis=msfile, caltable=caltb_phambd_interp_pha0, caltype='ph', pol='X,Y',
                                   antenna=antennas, parameter=pha0.flatten().tolist())
                        print("Using phase calibration table interpolated between records at " + bphacal[
                            't_pha'].iso + ' and ' + ephacal['t_pha'].iso)
                        gaintables.append(caltb_phambd_interp)
                        spwmaps.append(nspw * [0])
                        gaintables.append(caltb_phambd_interp_pha0)
                        spwmaps.append(nspw * [0])

        if docalib:
            clearcal(msfile)
            applycal(vis=msfile, gaintable=gaintables, spwmap=spwmaps, applymode='calflag', calwt=False)
        if doflag:
            # flag zeros and NaNs
            flagdata(vis=msfile, mode='clip', clipzeros=True)
            if flagant:
                try:
                    flagdata(vis=msfile, antenna=flagant)
                except:
                    print("Something wrong with flagant. Abort...")

        if doimage:
            from matplotlib import pyplot as plt
            from suncasa.utils import helioimage2fits as hf
            from sunpy import map as smap

            if not antenna:
                antenna = '0~12'
            if not stokes:
                stokes = 'XX'
            if not timerange:
                timerange = ''
            if not spw:
                spw = '1~3'
            if not imagedir:
                imagedir = '.'
            # (yr, mon, day) = (bt.datetime.year, bt.datetime.month, bt.datetime.day)
            # dirname = imagedir + str(yr) + '/' + str(mon).zfill(2) + '/' + str(day).zfill(2) + '/'
            # if not os.path.exists(dirname):
            #    os.makedirs(dirname)
            bds = [spw]
            nbd = len(bds)
            imgs = []
            for bd in bds:
                if '~' in bd:
                    bdstr = bd.replace('~', '-')
                else:
                    bdstr = str(bd).zfill(2)
                imname = imagedir + '/' + os.path.basename(msfile).replace('.ms', '.bd' + bdstr)
                print('Cleaning image: ' + imname)
                try:
                    tclean(vis=msfile, imagename=imname, antenna=antenna, spw=bd, timerange=timerange, imsize=[512],
                           cell=['5.0arcsec'], stokes=stokes,
                           niter=500)
                except:
                    print('clean not successfull for band ' + str(bd))
                else:
                    imgs.append(imname + '.image')
                junks = ['.flux', '.mask', '.model', '.psf', '.residual']
                for junk in junks:
                    if os.path.exists(imname + junk):
                        shutil.rmtree(imname + junk)

            tranges = [btime.iso + '~' + etime.iso] * nbd
            fitsfiles = [img.replace('.image', '.fits') for img in imgs]
            hf.imreg(vis=msfile, timerange=tranges, imagefile=imgs, fitsfile=fitsfiles, usephacenter=False)
            plt.figure(figsize=(6, 6))
            for i, fitsfile in enumerate(fitsfiles):
                plt.subplot(1, nbd, i + 1)
                eomap = smap.Map(fitsfile)
                sz = eomap.data.shape
                if len(sz) == 4:
                    eomap.data = eomap.data.reshape((sz[2], sz[3]))
                eomap.plot_settings['cmap'] = plt.get_cmap('jet')
                eomap.plot()
                eomap.draw_limb()
                # the next line would cause trouble in higher versions of SunPy, as it requires WCS
                # eomap.draw_grid()

            plt.show()

    if dosplit:
        if not doconcat:
            if not outputvis:
                outputvis = [vis[n].split('.')[0] + '.corrected.ms' for n in range(len(vis))]
            for n in range(len(vis)):
                split(vis=vis[n], outputvis=outputvis[n], datacolumn='corrected')
                if not keep_orig_ms:
                    os.system('rm -rf {}'.format(vis[n]))
    else:
        outputvis = vis

    if doconcat:
        if not concatvis:
            msoutdir = os.path.dirname(vis[0])
            if len(vis) == 1:
                vis0 = os.path.basename(vis[0])
                concatvis = os.path.join(msoutdir, vis0.split('.')[0] + '.corrected.ms')
            if len(vis) > 1:
                visb = os.path.basename(vis[0])
                vise = os.path.basename(vis[-1])
                concatvis = os.path.join(msoutdir, visb.split('.')[0] + '-' + vise.split('.')[0][3:] + '.corrected.ms')
        if len(vis) == 1:
            split(vis=vis[0], outputvis=concatvis, datacolumn='corrected')
        if len(vis) > 1:
            concateovsa(vis, concatvis, datacolumn='corrected', keep_orig_ms=keep_orig_ms, cols2rm="model,corrected")
        return concatvis
    else:
        return outputvis
