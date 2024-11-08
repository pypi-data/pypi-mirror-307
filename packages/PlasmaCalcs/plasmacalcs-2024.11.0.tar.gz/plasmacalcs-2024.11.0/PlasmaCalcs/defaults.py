"""
File Purpose: defaults in PlasmaCalcs
"""
import numpy as np

class _Defaults():
    '''stores defaults for PlasmaCalcs. Use DEFAULTS instead.
    (DEFAULTS is an instance of _Defaults(), instantiated at the bottom of defaults.py)
    '''
    def update(self, other_defaults):
        '''update self with other_defaults, overwriting any existing values.
        other_defaults: dict or _Defaults instance
            dict --> update from other_defaults.items()
            else --> update from other_defaults.__dict__.items()
        '''
        if not isinstance(other_defaults, dict):
            other_defaults = other_defaults.__dict__
        for key, value in other_defaults.items():
            setattr(self, key, value)

    TRACEBACKHIDE = True
    IMPORT_FAILURE_WARNINGS = False

    TAB = ' '*4   # size of a single tab, e.g. for docstrings.

    EPPIC_H5_SNAP_ZFILL = 6  # how many digits to zfill the snapshot number with

    DEBUG = 0   # level of debugging; 0 = no debugging.
    PROGRESS_UPDATES_PRINT_FREQ = 2  # seconds between progress updates

    # skip these attrs during Behavior.label_array(), by default.
    SKIP_BEHAVIOR_ARRAY_LABELS = ['quasineutral', 'slices']

    # raise MemorySizeError before loading arrays larger than this, by default.
    # (to set to no limit, use None)
    ARRAY_MBYTES_MAX = 1000  # [MB]

    # during memory_size_check, pretend array alements are at least as memory-intensive as this dtype:
    # (only used if array elements are smaller than this dtype.) (to set to no minimum, use None)
    ARRAY_MEMORY_CHECK_DTYPE_MIN = np.float64

    # during load_across_dims, use this many cpus by default, if ncpu not provided.
    # use None to automatically determine limit (based on number of cores available)
    LOADING_NCPU = 1
    # during load_across_dims, timeout after this many seconds, by default, if timeout not provided.
    # timeout numbers must be an integer (due to limitations of signal.alarm method).
    # For no time limit, use None, 0, or negative number.
    LOADING_TIMEOUT = None
    # during load_across_dims, if ncpu>1, group tasks into groups of size ncoarse before performing them.
    # use ncoarse=1 to avoid any coarsening.
    LOADING_NCOARSE = 1
    # during load_across_dims, use this builtins.multiprocessing.pool.Pool instead of making a new one.
    # (if provided, ncpu will be ignored.)
    # use None to make a new pool each time, when needed.
    LOADING_POOL = None

    # [EFF] when stats_dimpoint_wise is None, this tells min size before using stats_dimpoint_wise.
    #    if result would have size less than this, first try stats_dimpoint_wise=False.
    #    (this includes maindims shape.)
    #    (stats_dimpoint_wise True seems to be faster for larger arrays but slower for smaller arrays.)
    #    None --> no minimum, i.e. always prefer stats_dimpoint_wise = False.
    STATS_DIMPOINT_WISE_MIN_N = 512 * 512 * 200
    # [EFF] when stats_dimpoint_wise, this tells min length of dimension before loading across it,
    #   in the first attempt to load across dims implied. 1 --> no minimum.
    #   (if the first attempt fails, will repeat but with min_split=1.)
    STATS_DIMPOINT_WISE_MIN_SPLIT = 10

    EPPIC_LDEBYE_SAFETY = 1.1  # eppic dx,dy,dz = electron ldebye * safety. Probably ~1 or a bit larger.
    EPPIC_DT_SAFETY = 0.9   # eppic dt = smallest timescale * safety. Probably ~1 or a bit smaller.

    # safety factor for Rosenberg's criterion for quasineutrality:
    #   quasineutrality is "reasonable" when (nusn / wplasma)^2 << 1.
    #   (use '<= EPPIC_ROSENBERG_SAFETY' instead of '<< 1'.)
    EPPIC_ROSENBERG_SAFETY = 0.5

    # for displaying trees. See Tree._html for details.
    TREE_CSS = '''
    <style type="text/css">
    summary {display: list-item}          /* show arrows for details/summary tags */
    details > *:not(summary){margin-left: 2em;}   /* indent details/summary tags. */
    </style>
    '''
    TREE_SHOW_DEPTH = 4  # default depth to show when displaying trees.
    TREE_MAX_DEPTH = 50  # max depth to render as html when displaying trees.
    TREE_SHORTHAND = False  # whether to use shorthand for Tree nodes when displaying trees.

    # fft renaming convention for dimensions, when rad=True, and freq_dims not provided.
    # dict of {old dim: new dim} pairs. Or, None, equivalent to empty dict.
    # for dims not appearing here, new dim will be 'freqrad_{dim}'.
    FFT_FREQ_RAD_DIMNAMES = {    
        'x': 'k_x',
        'y': 'k_y',
        'z': 'k_z',
        't': 'omega',
    }
    # default value for "keep" in xarray_fftN. Should be 0 < value <= 1.
    FFT_KEEP = 0.4
    # default value for "keep" in xarray_lowpass. Should be 0 < value <= 1.
    LOWPASS_KEEP = 0.4

    # default method to use for rounding fractional indexes to integers, as per interprets_fractional_indexing.
    # 'round' --> as per builtins.round(). round to nearest integer, ties toward even integers.
    # 'int' --> as per builtins.int(). round towards 0.
    # 'floor' --> as per math.floor(). round towards negative infinity.
    # 'ceil' --> as per math.ceil(). round towards positive infinity.
    # note that 'floor' is the default to avoid accidentally accessing using index=len(array).
    FRACTIONAL_INDEX_ROUNDING = 'floor'

    # default for gaussian filter sigma, if not provided.
    GAUSSIAN_FILTER_SIGMA = 1.0

    # if this number density in [m^-3] is too large for float32 in output units system,
    # then convert to float64. Commonly relevant if calculating 'n' in 'raw' Bifrost units.
    BIFROST_MAX_GUARANTEE_SUPPORT_N_SI = 1e30


class _PlotDefaults():
    '''stores defaults for PlasmaCalcs. Use DEFAULTS.PLOT instead.
    (DEFAULTS.PLOT is an instance of _PlotDefaults(), instantiated at the bottom of defaults.py)
    '''
    ASPECT = 'equal'  # default aspect ratio for plots
    LAYOUT = 'compressed'   # default layout for plots. 'constrained', 'compressed', 'tight', or 'none'

    # default for robust when determining vmin & vmax. True, False, or number between 0 and 50.
    # True --> use DEFAULTS.PLOT.ROBUST_PERCENTILE.
    ROBUST = True
    # default percentile for determining vmin & vmax, when using robust.
    ROBUST_PERCENTILE = 2.0

    # # params for plotting.colorbar.make_cax # #
    CAX_PAD = 0.01
    CAX_SIZE = 0.02
    CAX_LOCATION = 'right'
    # # other colorbar params # #
    CAX_MODE = 'mpl'   # 'mpl' or 'pc'. 'mpl' uses matplotlib logic to make cax; 'pc' uses PlasmaCalcs.make_cax.
                        # note that 'pc' looks better if using layout='none', but worse with any other layout.

    # # params for movies # #
    FPS = 30   # frames per second. if None, use matplotlib defaults.
    BLIT = True  # whether to use blitting. if None, use matplotlib defaults.
    MOVIE_EXT = '.mp4'  # movie filename extension to use if none provided. if None, use matplotlib defaults.

    MOVIE_TITLE_FONT = 'monospace'  # font for movie titles

    # [chars] suggested width of titles for subplots;
    # some routines might make multiline title if title would be longer than this.
    SUBPLOT_TITLE_WIDTH = 20  

    # [chars] suggested width of suptitle
    # some routines might make multiline suptitle if suptitle would be longer than this.
    SUPTITLE_WIDTH = 40

    # [seconds] minimum time between progress updates when saving movie.
    # use 0 for no minimum; use -1 for "never print".
    MOVIE_PROGRESS_UPDATE_FREQ = 1

    # whether to print help message about how to display movie inline,
    # if it might be applicable (e.g., using ipython) and plt.rcParams['animation.html']=='none'.
    MOVIE_REPR_INLINE_HELP = True

    # # other params # #
    # DIMS_INFER tell which array.dims to use for x axis, y axis, and time axis (if movie).
    #   each list will be checked in order, using first match in case of multiple matches.
    #   This only applies when trying to infer plot dims which were not specified.
    DIMS_INFER = {
        # plot time axis
        't': ('time', 't', 'snap', 'snapshot', 'frame'),
        # plot x axis
        'x': ('x', 'r', 'y', 'z',
              'freq_x', 'freq_y', 'freq_z',
              'kx', 'ky', 'kz',
              'k_x', 'k_y', 'k_z',
              ),
        # plot y axis
        'y': ('y', 'z',
              'freq_y', 'freq_z',
              'k_y', 'k_z',
              ),
    }
    # if dim in any set in DIMS_SAME, then the other dims are "redundant" with that dim.
    # usually not used, but e.g. in infer_subplot_title, if t_plot_dim is 'snap' or 't',
    # don't include the other one in the subplot title either, since they appear together in a set in DIMS_SAME.
    DIMS_SAME = [
        {'time', 'snap', 't'},
    ]

    SUBPLOTS_MAX_NROWS_NCOLS = 15  # max number of rows or cols in a subplots grid before crashing.
    SUBPLOTS_AXSIZE = (2,2)  # default size of each subplot, in inches.

    # # params for plotting.timelines # #
    # maximum length of a dimension before crashing when plotting timelines.
    # (helps to avoid accidentally creating one line for each x,y,z coords...)
    # e.g. if 10, when plotting 'fluid' and 'component', require len(fluids)<=10 and len(component)<=10.
    TIMELINES_DMAX = 10  # use None for no limit.

    # cycles for timelines. each cycle can be:
    #   dict --> interpretted as {matplotlib kwarg: list of values},
    #   None --> plt.rcParams['axes.prop_cycle']
    #   Cyler (from cycler module)
    TIMELINES_CYCLE0 = None  # default cycle for first dim. 
    TIMELINES_CYCLE1 = {'ls': ['-', '--', ':', '-.']}  # default cycle for second dim.

    # # params for faceplot # #
    # default viewing angle for 3D faceplots, as (elevation, azimuth, roll).
    # (-160, 30, 0) provides a decent angle for viewing x=0, y=0, z=0 faces.
    FACEPLOT_VIEW_ANGLE = (-160, 30, 0)

    # default kwargs for ax.plot of edges in 3D faceplots.
    # set to None to not plot edges.
    FACEPLOT_EDGE_KWARGS = {'color': '0.4', 'linewidth': 1, 'zorder': 1e3}

    # faceplot axes zoom factor. Default 1. Must be >0. See ax.set_box_aspect for details.
    FACEPLOT_AXES_ZOOM = 1.0

    # aspect for 3D plots
    # 'auto', 'equal', (x aspect, y aspect, z aspect),
    # or (1, x multiplier, y multiplier, z multiplier);
    #    multiplier multiplies aspect determined by data lengths. >1 --> longer.
    ASPECT3D = 'equal'

    # projection type for 3D plots. 'ortho' or 'persp'
    # For more details see mpl_toolkits.mplot3d.axes3d.Axes3D
    PROJ_TYPE = 'ortho'

    # for contour plots, if using colorbar, linewidth of lines in colorbar.
    # None --> use same width as contour lines.
    # 2-tuple of None or int: defines (min, max); None for no bound.
    #   E.g. (4, None) says "for thinner lines use 4; others same as contour lines".
    COLORBAR_LINEWIDTH = (4, None)

    # for contour plots, if using colorbar, linestyle of lines in colorbar.
    # None --> use same linestyle as contour lines.
    COLORBAR_LINESTYLE = None


class _PhysicalDefaults():
    '''stores physical values defaults for PlasmaCalcs. Use DEFAULTS.PHYSICAL instead.
    (DEFAULTS.PHYSICAL is an instance of _PhysicalDefaults(), instantiated at the bottom of defaults.py)
    '''
    # values of various physical constants in SI units
    CONSTANTS_SI = {
        'amu'     : 1.66054e-27,  # atomic mass unit
        'c'       : 2.99792E8,    # speed of light
        'kB'      : 1.38065E-23,  # boltzmann constant
        'eps0'    : 8.85419E-12,  # permittivity of free space
        'mu0'     : 1.25664E-6,   # permeability of free space
        'qe'      : 1.60218E-19,  # elementary charge
        'me'      : 9.10938E-31,  # electron mass
        'qme'     : 1.75882E11,   # q / m_e
        'hplanck' : 6.260701E-34, # planck constant (not hbar)
        'm_proton': 1.67262E-27,  # proton mass
        'eV'      : 1.602176634E-19,    # electron volt
        # also, see below for some additional derived constants:
    }
    CONSTANTS_SI['eV kB-1']  = CONSTANTS_SI['eV'] / CONSTANTS_SI['kB']
    CONSTANTS_SI['me amu-1'] = CONSTANTS_SI['me'] / CONSTANTS_SI['amu']
    for _key, _alias in (('qe', 'q_e'), ('me', 'm_e'), ('m_proton', 'm_p'), ('hplanck', 'h')):
        CONSTANTS_SI[_alias] = CONSTANTS_SI[_key]
    del _key, _alias

    # atomic weight [amu] of each element
    M_AMU = {
        'H' :  1.008,
        'He':  4.003,
        'C' : 12.01,
        'N' : 14.01,
        'O' : 16.0,
        'Ne': 20.18,
        'Na': 23.0,
        'Mg': 24.32,
        'Al': 26.97,
        'Si': 28.06,
        'S' : 32.06,
        'K' : 39.1,
        'Ca': 40.08,
        'Cr': 52.01,
        'Fe': 55.85,
        'Ni': 58.69,
        }

    # first ionization potential [eV] of each element
    IONIZE_EV = {
        'H' : 13.595,
        'He': 24.580,
        'C' : 11.256,
        'N' : 14.529,
        'O' : 13.614,
        'Ne': 21.559,
        'Na':  5.138,
        'Mg':  7.644,
        'Al':  5.984,
        'Si':  8.149,
        'S' : 10.357,
        'K' :  4.339,
        'Ca':  6.111,
        'Cr':  6.763,
        'Fe':  7.896,
        'Ni':  7.633,
        }

    # degeneracy of states, for saha ionization equation
    SAHA_G0 = {
        'H' :  2.0,
        'He':  1.0,
        'C' :  9.3,
        'N' :  4.0,
        'O' :  8.7,
        'Ne':  1.0,
        'Na':  2.0,
        'Mg':  1.0,
        'Al':  5.9,
        'Si':  9.5,
        'S' :  8.1,
        'K' :  2.1,
        'Ca':  1.2,
        'Cr': 10.5,
        'Fe': 26.9,
        'Ni': 29.5,
        }
    SAHA_G1 = {
        'H' :  1.0,
        'He':  2.0,
        'C' :  6.0,
        'N' :  9.0,
        'O' :  4.0,
        'Ne':  5.0,
        'Na':  1.0,
        'Mg':  2.0,
        'Al':  1.0,
        'Si':  5.7,
        'S' :  4.1,
        'K' :  1.0,
        'Ca':  2.2,
        'Cr':  7.2,
        'Fe': 42.7,
        'Ni': 10.5,
        }
    SAHA_G1G0 = {}
    for _e in SAHA_G0:
        SAHA_G1G0[_e] = SAHA_G1[_e] / SAHA_G0[_e]
    del _e


DEFAULTS = _Defaults()
DEFAULTS.PLOT = _PlotDefaults()  # e.g., can access CAX_PAD via DEFAULTS.PLOT.CAX_PAD
DEFAULTS.PHYSICAL = _PhysicalDefaults()  # e.g., can access M_AMU via DEFAULTS.PHYSICAL.M_AMU
