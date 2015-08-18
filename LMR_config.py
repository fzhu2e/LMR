"""
Class based config module to help with passing information to LMR modules for
reconstruction experiments.

Adapted from LMR_exp_NAMELIST by AndreP
"""

from os.path import join


class constants:

    class file_types:
        netcdf = 'NCD'
        ascii = 'ASC'
        numpy = 'NPY'
        numpy_zip = 'NPZ'
        dataframe = 'DF'

class core:
    """
    High-level parameters of reconstruction experiment

    Attributes
    ----------
    nexp: str
        Name of reconstruction experiment
    lmr_path: str
        Absolute path for the experiment
    clean_start: bool
        Delete existing files in output directory (otherwise they will be used
        as the prior!)
    recon_period: list(int)
        Time period for reconstruction
    nens: int
        Ensemble size
    iter_range: list(int)
        Number of Monte-Carlo iterations to perform
    loc_rad: float
        Localization radius for DA (in km)
    datadir_output: str
        Absolute path to working directory output for LMR
    archive_dir: str
        Absolute path to LMR reconstruction archive directory
    """
    nexp = 'testdev_multires_1y'
    lmr_path = '/home/chaos2/wperkins/data/LMR'
    online_reconstruction = False
    clean_start = True
    # TODO: More pythonic to make last time a non-inclusive edge
    recon_period = [1850, 2000]
    nens = 100
    seed = None
    iter_range = [0, 0]
    curr_iter = iter_range[0]
    loc_rad = None
    assimilation_time_res = [1.0]  # in yrs
    year_start_idx_shift = 3  # What we're defining as year start
                              # 0-11 where 0 indicates start at Jan.

    datadir_output = '/home/chaos2/wperkins/data/LMR/output/working'
    #datadir_output  = '/home/disk/kalman3/rtardif/LMR/output/wrk'
    #datadir_output  = '/home/disk/ekman/rtardif/nobackup/LMR/output'
    #datadir_output  = '/home/disk/ice4/hakim/svnwork/python-lib/trunk/src/ipython_notebooks/data'

    archive_dir = '/home/chaos2/wperkins/data/LMR/output/archive'
    #archive_dir = '/home/disk/kalman3/rtardif/LMR/output'
    #archive_dir = '/home/disk/kalman3/hakim/LMR/'

class proxies:
    """
    Parameters for proxy data

    Attributes
    ----------
    use_from: list(str)
        A list of keys for proxy classes to load from.  Keys available are
        stored in LMR_proxy2.
    proxy_frac: float
        Fraction of available proxy data (sites) to assimilate
    """

    use_from = ['pages']
    proxy_frac = 0.75

    class pages:
        """
        Parameters for PagesProxy class

        Attributes
        ----------
        datadir_proxy: str
            Absolute path to proxy data
        datafile_proxy: str
            Absolute path to proxy records file
        metafile_proxy: str
            Absolute path to proxy meta data
        dataformat_proxy: str
            File format of the proxy data
        regions: list(str)
            List of proxy data regions (data keys) to use.
        proxy_resolution: list(float)
            List of proxy time resolutions to use
        proxy_order: list(str):
            Order of assimilation by proxy type key
        proxy_assim2: dict{ str: list(str)}
            Proxy types to be assimilated.
            Uses dictionary with structure {<<proxy type>>: [.. list of measuremant
            tags ..] where "proxy type" is written as
            "<<archive type>>_<<measurement type>>"
        proxy_type_mapping: dict{(str,str): str}
            Maps proxy type and measurement to our proxy type keys.
            (e.g. {('Tree ring', 'TRW'): 'Tree ring_Width'} )
        simple_filters: dict{'str': Iterable}
            List mapping Pages2k metadata sheet columns to a list of values
            to filter by.
        """

        datadir_proxy = join(core.lmr_path, 'data', 'proxies')
        datafile_proxy = join(datadir_proxy,
                              'Pages2k_Proxies.df.pckl')
        metafile_proxy = join(datadir_proxy,
                              'Pages2k_Metadata.df.pckl')
        dataformat_proxy = 'DF'

        regions = ['Antarctica', 'Arctic', 'Asia', 'Australasia', 'Europe',
                   'North America', 'South America']
        proxy_resolution = core.assimilation_time_res

        # DO NOT CHANGE FORMAT BELOW

        proxy_order = ['Tree ring_Width',
                       'Tree ring_Density',
                       'Ice core_d18O',
                       'Ice core_d2H',
                       'Ice core_Accumulation',
                       'Coral_d18O',
                       'Coral_Luminescence',
                       'Lake sediment_All',
                       'Marine sediment_All',
                       'Speleothem_All']

        proxy_assim2 = {
            'Tree ring_Width': ['Ring width',
                                'Tree ring width',
                                'Total ring width',
                                'TRW'],
            'Tree ring_Density': ['Maximum density',
                                  'Minimum density',
                                  'Earlywood density',
                                  'Latewood density',
                                  'MXD'],
            'Ice core_d18O': ['d18O'],
            'Ice core_d2H': ['d2H'],
            'Ice core_Accumulation': ['Accumulation'],
            'Coral_d18O': ['d18O'],
            'Coral_Luminescence': ['Luminescence'],
            'Lake sediment_All': ['Varve thickness',
                                  'Thickness',
                                  'Mass accumulation rate',
                                  'Particle-size distribution',
                                  'Organic matter',
                                  'X-ray density'],
            'Marine sediment_All': ['Mg/Ca'],
            'Speleothem_All': ['Lamina thickness'],
            }

        # Create mapping for Proxy Type/Measurement Type to type names above
        proxy_type_mapping = {}
        for type, measurements in proxy_assim2.iteritems():
            # Fetch proxy type name that occurs before underscore
            type_name = type.split('_', 1)[0]
            for measure in measurements:
                proxy_type_mapping[(type_name, measure)] = type

        simple_filters = {'PAGES 2k Region': regions,
                          'Resolution (yr)': proxy_resolution}


class psm:
    """
    Parameters for PSM classes

    Attributes
    ----------
    use_psm: dict{str: str}
        Maps proxy class key to psm class key.  Used to determine which psm
        is associated with what Proxy type.
    """

    use_psm = {'pages': 'linear'}

    class linear:
        """
        Parameters for the linear fit PSM.

        Attributes
        ----------
        datatag_calib: str
            Source of calibration data for PSM
        datadir_calib: str
            Absolute path to calibration data
        datafile_calib: str
            Filename for calibration data
        dataformat_calib: str
            Data storage type for calibration data
        pre_calib_datafile: str
            Absolute path to precalibrated Linear PSM data
        psm_r_crit: float
            Usage threshold for correlation of linear PSM
        """
        datatag_calib = 'GISTEMP'
        datadir_calib = join(core.lmr_path, 'data', 'analyses')
        datafile_calib = 'gistemp1200_ERSST.nc'
        dataformat_calib = 'NCD'

        pre_calib_datafile = join(core.lmr_path,
                                  'PSM',
                                  'PSMs_' + datatag_calib + '.pckl')
        psm_r_crit = 0.2


class prior:
    """
    Parameters for the ensDA prior

    Attributes
    ----------
    prior_source: str
        Source of prior data
    datadir_prior: str
        Absolute path to prior data
    datafile_prior: str
        Name of prior file to use
    dataformat_prior: str
        Datatype of prior container
    state_variables: list(str)
        List of variables to use in the state vector for the prior
    """
    # Prior data directory & model source
    prior_source = 'ccsm4_last_millenium'
    datadir_prior = join(core.lmr_path, 'data', 'model', prior_source)
    #datafile_prior = 'tas_Amon_CCSM4_past1000_r1i1p1_085001-185012.nc'
    datafile_prior   = '[vardef_template]_CCSM4_past1000_085001-185012.nc'
    dataformat_prior = 'NCD'
    state_variables = ['tas_sfc_Amon']
    truncate_state = True

