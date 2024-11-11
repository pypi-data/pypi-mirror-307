import numpy as np
from tqdm import tqdm
import os
from shutil import rmtree

from ..casa_compat import import_casatools,import_casatasks

tasks = import_casatasks('split', 'tclean', 'casalog', 'clearcal', 'gaincal')
split = tasks.get('split')
tclean = tasks.get('tclean')
casalog = tasks.get('casalog')
clearcal = tasks.get('clearcal')
gaincal = tasks.get('gaincal')

tools = import_casatools(['tbtool', 'mstool', 'qatool'])
tbtool = tools['tbtool']
mstool = tools['mstool']
qatool = tools['qatool']
tb = tbtool()
ms = mstool()
qa = qatool()

def get_bandinfo(msfile, spw=None, returnbdinfo=False, verbose=False):
    '''
    get center frequencies of all spectral windows for msfile
    spw: [option] return the cfreq of spw. spw can be a a string or a list of string.
    The syntax of spw follows the standard spw Parameter in CASA
    if spw is not provided, return the cfreq of all spws in the msfile.
    return cfreqs is in GHz
    if returnbounds is True, return a dictionary including comprehensive freq information of the ms.
    '''

    ms.open(msfile)
    spwInfo = ms.getspectralwindowinfo()
    nspw = len(spwInfo.keys())
    reffreqs = []
    bdwds = []
    chanwds = []
    nchans = []
    for s in range(nspw):
        s_ = str(s)
        reffreqs.append(spwInfo[s_]['RefFreq'])
        bdwds.append(spwInfo[s_]['TotalWidth'])
        chanwds.append(spwInfo[s_]['ChanWidth'])
        nchans.append(spwInfo[s_]['NumChan'])
    reffreqs = np.array(reffreqs) / 1e9
    bdwds = np.array(bdwds) / 1e9
    chanwds = np.array(chanwds) / 1e9
    nchans = np.array(nchans)
    cfreqs = reffreqs + bdwds / 2.0 - chanwds / 2.0
    bdinfo = {'bounds_all': np.hstack((reffreqs, reffreqs[-1] + bdwds[-1])), 'cfreqs_all': cfreqs,
              'bounds_all_lo': reffreqs, 'bounds_all_hi': reffreqs + bdwds, 'nchans': nchans}
    if spw:
        freqbounds_lo_spw = []
        freqbounds_hi_spw = []
        cfreqs_spw = []
        for sp in spw:
            if verbose:
                print(f'Parsing spw {sp}...')
            try:
                staql = {'spw': sp}
                ms.selectinit(reset=True)
                ms.msselect(staql, onlyparse=True)
                ndx = ms.msselectedindices()
                chan_sel = ndx['channel']
                bspw = chan_sel[0, 0]
                bchan = chan_sel[0, 1]
                espw = chan_sel[-1, 0]
                echan = chan_sel[-1, 2]
                bfreq = (spwInfo[str(bspw)]['Chan1Freq'] + spwInfo[str(bspw)]['ChanWidth'] * bchan) / 1e9
                efreq = (spwInfo[str(espw)]['Chan1Freq'] + spwInfo[str(espw)]['ChanWidth'] * echan) / 1e9
                cfreq = (bfreq + efreq) / 2.
            except ValueError:
                if verbose:
                    print("Parsing spw {} failed. Aborting...".format(sp))
                continue
            freqbounds_lo_spw.append(bfreq)
            freqbounds_hi_spw.append(efreq)
            cfreqs_spw.append(cfreq)
        cfreqs = np.array(cfreqs_spw)
        freqbounds_lo = np.array(freqbounds_lo_spw)
        freqbounds_hi = np.array(freqbounds_hi_spw)
        bdinfo['bounds_lo'] = freqbounds_lo
        bdinfo['bounds_hi'] = freqbounds_hi
        bdinfo['cfreqs'] = cfreqs

    ms.done()
    if returnbdinfo:
        return bdinfo
    else:
        return cfreqs


def get_bmsize(cfreq, refbmsize=70.0, reffreq=1.0, minbmsize=4.0):
    '''
    get beamsize at frequencies definded by cfreq based on refbmsize at reffreq
    cfreq: input frequencies at GHz
    refbmsize: reference beam size in arcsec
    reffreq: reference frequency in GHz
    minbmsize: minimum beam size in arcsec
    '''
    bmsize = refbmsize * reffreq / cfreq
    bmsize[bmsize < minbmsize] = minbmsize
    return bmsize


def get_trange(msfile):
    from astropy.time import Time
    tb.open(msfile)
    tr = np.array([tb.getcell('TIME', 0), tb.getcell('TIME', tb.nrows() - 1)]) / 24. / 3600.
    tb.close()
    return Time(tr, format='mjd')


def time2filename(msfile, timerange='', spw='', desc=False):
    from astropy.time import Time
    tb.open(msfile)
    starttim = Time(tb.getcell('TIME', 0) / 24. / 3600., format='mjd')
    endtim = Time(tb.getcell('TIME', tb.nrows() - 1) / 24. / 3600., format='mjd')
    tb.close()
    datstr = starttim.iso[:10]
    ms.open(msfile)
    metadata = ms.metadata()
    observatory = metadata.observatorynames()[0]
    ms.done()
    if timerange is None or timerange == '':
        starttim1 = starttim
        endtim1 = endtim
    else:
        (tstart, tend) = timerange.split('~')
        if tstart[2] == ':':
            starttim1 = Time(datstr + 'T' + tstart)
            endtim1 = Time(datstr + 'T' + tend)
        else:
            starttim1 = Time(qa.quantity(tstart, 'd')['value'], format='mjd')
            endtim1 = Time(qa.quantity(tend, 'd')['value'], format='mjd')
    if desc:
        tstr = starttim1.to_datetime().strftime(
            '{}_%Y%m%dT%H%M%S.%f'.format(observatory)) + endtim1.to_datetime().strftime('-%H%M%S.%f')
    else:
        midtime = Time((starttim1.mjd + endtim1.mjd) / 2., format='mjd')
        tstr = midtime.to_datetime().strftime('{}_%Y%m%dT%H%M%S.%f'.format(observatory))

    if spw:
        spstr = 'spw{}'.format(spw.replace('~', '-'))
        filename = '.'.join([tstr, spstr])
    else:
        filename = tstr

    return filename


def msclearhistory(msfile):
    '''Clears history in the a measurement sets file

    :param msfile: string
            The name of a measurement sets file

    :return:
    '''

    tb.open(msfile + '/HISTORY', nomodify=False)
    nrows = tb.nrows()
    if nrows > 0:
        tb.removerows(range(nrows))
    tb.close()


def clearflagrow(msfile, mode='clear'):
    '''

    :param msfile:
    :param mode: FLAG_ROW operation
    default: 'clear': (default) clear the FLAG_ROW
             'list': to list existing FLAG_ROW
    :return:
    '''

    if mode == 'list':
        tb.open(msfile, nomodify=True)
        a = tb.getcol('FLAG_ROW')
        nfrows = np.sum(a)
        nrows = float(len(a))
        print('{:0d} out of {:.0f} ({:.0f}%) rows are flagged in {}'.format(nfrows, nrows, nfrows / nrows * 100,
                                                                            os.path.basename(msfile)))
    elif mode == 'clear':
        tb.open(msfile, nomodify=False)
        a = tb.getcol('FLAG_ROW')
        a[:] = False
        tb.putcol('FLAG_ROW', a)
        print('reset successfully')
    tb.close()


def splitX(vis, datacolumn2='MODEL_DATA', **kwargs):
    import os
    """
    Splits specific data columns from a CASA measurement set (MS) into a new MS file,
    overcoming the limitation of splitting multiple data columns directly with CASA's standard split function.

    A temporary MS is used during processing to ensure the additional column (the `datacolumn2`) has the same shape as
    the data/corrected column in the output MS. This temporary file is removed at the end.

    :param str vis: Path to the original measurement set.
    :param str datacolumn2: The name of the additional data column to be included in the split. Defaults to 'MODEL_DATA'.
    :param kwargs: Additional keyword arguments to be passed to the CASA `split` task.
    :return: Path to the output measurement set with the specified columns split.
    :rtype: str
    """

    datacolumn2 = datacolumn2.upper()
    outmsfile = kwargs.get('outputvis', '').rstrip('/')

    # Clean up the output directory and associated flag versions
    if os.path.exists(outmsfile):
        rmtree(outmsfile)
    flagversions_path = f"{outmsfile}.flagversions"
    if os.path.exists(flagversions_path):
        rmtree(flagversions_path)

    # Perform the initial split to create the output MS with the data/corrected column into the data column
    split(vis=vis, **kwargs)

    # Prepare for the second split
    tmpms_file = f'{vis}.tmpms'
    kwargs2 = {k: v for k, v in kwargs.items() if k not in ['datacolumn', 'outputvis']}
    kwargs2.update({'outputvis': tmpms_file, 'datacolumn': datacolumn2.replace('_DATA', '')})

    # Ensure temporary MS is removed if it exists

    if os.path.exists(tmpms_file):
        rmtree(tmpms_file)

    # Perform the second split to temporary MS
    split(vis=vis, **kwargs2)

    # Process the additional column from the temporary MS
    tb.open(tmpms_file)
    nrows = tb.nrows()
    data = []
    for row in tqdm(range(nrows), desc=f'Extracting {datacolumn2} column', ascii=True):
        data.append(tb.getcell('DATA', row))
    tb.close()

    # Add additional data column to the output MS
    clearcal(outmsfile, addmodel=True)
    tb.open(outmsfile, nomodify=False)
    for row in tqdm(range(nrows), desc=f'writing {datacolumn2} column', ascii=True):
        tb.putcell(datacolumn2, row, data[row])
    tb.close()

    # Cleanup
    rmtree(tmpms_file)
    return outmsfile


def flagcaltboutliers(caltable, limit=[]):
    import numpy as np
    import numpy.ma as ma
    # def removeOutliers(x, outlierConstant):
    #     a = np.array(x)
    #     idx, = np.where(np.diff(np.sort(datamag[0, 0, :]))>)
    #     upper_quartile = np.percentile(a, 80)
    #     lower_quartile = np.percentile(a, 20)
    #     IQR = (upper_quartile - lower_quartile) * outlierConstant
    #     quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    #     return ma.masked_outside(x, quartileSet[1], quartileSet[0])

    if not os.path.exists(caltable): return 0
    if isinstance(limit, list):
        if len(limit) == 2:
            tb.open(caltable, nomodify=False)
            # subt = tb.query("ANTENNA1==1 && SPECTRAL_WINDOW_ID=10")
            # data = subt.getcol('CPARAM')
            # flag = subt.getcol('FLAG')
            # spw = subt.getcol('SPECTRAL_WINDOW_ID')
            # datamag = np.abs(data)
            # mdatamag = ma.masked_outside(datamag, limit[0], limit[1])
            # mask = np.logical_or(mdatamag.mask, flag)
            # dataidx1 = datamag<limit[0]
            # dataidx2 = datamag>limit[1]
            # mdatamag = ma.masked_array(mdatamag, mask)
            # mdatamag[0, 0, :] = removeOutliers(mdatamag[0, 0, :], 5)
            # mdatamag[1, 0, :] = removeOutliers(mdatamag[1, 0, :], 5)
            data = tb.getcol('CPARAM')
            flag = tb.getcol('FLAG')
            datamag = np.abs(data)
            dataidx1 = datamag < limit[0]
            dataidx2 = datamag > limit[1]
            flag[dataidx1] = True
            flag[dataidx2] = True
            tb.putcol('FLAG', flag)
            return 1
        else:
            print('limit must have two elements. Aborted!')
            return 0
    else:
        print('limit must be a list. Aborted!')


def modeltransfer(msfile, spw='', reference='XX', transfer='YY'):
    pol_dict = {'XX': 0, 'YY': 1, 'XY': 2, 'YX': 3}
    refidx = pol_dict[reference]
    trfidx = pol_dict[transfer]
    datams = mstool()
    datams.open(msfile, nomodify=False)

    if '~' in spw:
        sp0, sp1 = spw.split('~')
        for sp in range(int(sp0), int(sp1) + 1):
            staql = {'spw': str(sp)}
            datams.selectinit(reset=True)
            datams.msselect(staql)
            modeldata = datams.getdata(['model_data'])
            modeldata['model_data'][trfidx, ...] = modeldata['model_data'][refidx, ...]
            datams.putdata(modeldata)
        datams.close()
    else:
        datams.selectinit(reset=True)
        staql = {'spw': spw}
        datams.msselect(staql)
        modeldata = datams.getdata(['model_data'])
        modeldata['model_data'][trfidx, ...] = modeldata['model_data'][refidx, ...]
        datams.putdata(modeldata)
        datams.close()


def concat_slftb(tb_in=[], tb_out=None):
    if not tb_in:
        print('tb_in not provided. Abort...')
    if os.path.exists(tb_out):
        os.system('rm -r {}'.format(tb_out))
    os.system('cp -r {} {}'.format(tb_in[0], tb_out))
    tbdata = {}
    tb.open(tb_out)
    cols = tb.colnames()
    tb.close()
    cols.remove('WEIGHT')
    for col in cols:
        tbdata[col] = []
    for tbidx, ctb in enumerate(tb_in):
        tb.open(ctb, nomodify=True)
        tim0 = tb.getcol(cols[0])
        if len(tim0) == 0:
            continue
        else:
            for col in cols:
                if tbidx == 1 and col in ['CPARAM', 'PARAMERR', 'FLAG', 'SNR']:
                    tbdata[col].append(tb.getcol(col)[::-1, ...])
                else:
                    tbdata[col].append(tb.getcol(col))
        tb.close()

    if len(tbdata[cols[0]]) == 0:
        print('tables have no data. Return')
        return -1
    else:
        for col in cols:
            if col in ['CPARAM', 'PARAMERR', 'FLAG', 'SNR']:
                tbdata[col] = np.concatenate(tbdata[col], axis=2)
            else:
                tbdata[col] = np.concatenate(tbdata[col])
        tb.open(tb_out, nomodify=False)
        nrows = tb.nrows()
        nrows_new = len(tbdata[cols[0]])
        tb.addrows(nrows_new - nrows)
        for col in cols:
            tb.putcol(col, tbdata[col])
        tb.close()
        return tb_out


def gaincalXY(vis=None, caltable=None, pols='XXYY', msfileXY=None, gaintableXY=None, **kwargs):
    if pols == 'XXYY':
        pols = 'XX,YY'
    pols_ = pols.split(',')
    rm_msfileXY = False
    if msfileXY is None:
        rm_msfileXY = True
        msfileXY = {}
        for pol in pols_:
            msfileXY[pol] = '.'.join([vis, pol])
            if os.path.exists(msfileXY[pol]):
                os.system('rm -rf {}'.format(msfileXY[pol]))
            splitX(vis=vis, outputvis=msfileXY[pol], correlation=pol, datacolumn='data', datacolumn2='MODEL_DATA')
    if gaintableXY is not None:
        if 'gaintable' in kwargs.keys():
            kwargs.pop('gaintable')
    caltbXY = []
    for pol in pols_:
        caltb_ = '.'.join([caltable, pol])
        if gaintableXY is not None:
            kwargs['gaintable'] = gaintableXY[pol]
        gaincal(vis=msfileXY[pol], caltable=caltb_, **kwargs)
        caltbXY.append(caltb_)
    concat_slftb(caltbXY, caltable)
    if rm_msfileXY:
        for k, v in msfileXY.iteritems():
            os.system('rm -rf {}'.format(v))
    return


def getmodel(vis, spw=None):
    tb.open(vis, nomodify=True)
    subt = tb.query("DATA_DESC_ID==" + str(spw))
    model_d = subt.getcol('MODEL_DATA')
    subt.done()
    tb.done()
    return model_d


def putmodel(vis, spw=None, model=None):
    tb.open(vis, nomodify=False)
    subt = tb.query("DATA_DESC_ID==" + str(spw))
    model_d = subt.putcol('MODEL_DATA', model)
    subt.done()
    tb.done()
    return model_d
