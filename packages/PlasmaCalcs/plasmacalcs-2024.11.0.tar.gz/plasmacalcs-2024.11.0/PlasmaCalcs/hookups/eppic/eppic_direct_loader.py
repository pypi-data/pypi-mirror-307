"""
File Purpose: EppicDirectLoader
"""
import os

# required external modules
import numpy as np
import xarray as xr

# optional external modules
from ...tools import ImportFailed
try:
    import h5py
except ImportError:
    h5py = ImportFailed("h5py")
try:
    import zarr
except ImportError:
    zarr = ImportFailed("zarr")

# internal modules
from ...errors import (
    LoadingNotImplementedError,
    OverrideNotApplicableError,
    CacheNotApplicableError,
)
from ...quantities import QuasineutralLoader
from ...tools import (
    using_attrs,
)
from ...defaults import DEFAULTS


''' --------------------- EppicDirectLoader --------------------- '''

class EppicDirectLoader(QuasineutralLoader):
    '''manages loading data directly from eppic output files.

    input_deck: EppicInputDeck
        input deck. E.g. EppicInputDeck.from_file('eppic.i').
        Currently, requires that input_deck.filename is not None.
    read_mode: str
        how to read the files.
        Currently, must be 'h5' or 'h5_2'. See help(EppicDirectLoader.read_mode) for details.

    attributes of self (not available at __init__)
    '''
    _h5_zfill = DEFAULTS.EPPIC_H5_SNAP_ZFILL
    _slice_maindims_in_load_direct = True   # [EFF] slice directly when reading h5 files, if using self.slices

    def __init__(self, input_deck, *, read_mode='h5', **kw_super):
        self.input_deck = input_deck
        self.read_mode = read_mode
        super().__init__(**kw_super)

    # # # READ MODE AND SNAPDIR # # #
    @property
    def read_mode(self):
        '''mode telling which files to read.
        Currently, must be 'h5' or 'h5_2'
        Maybe other modes will be added at some point.

        Options:
            'h5' --> read from .h5 files,
                    determine file format based on input_deck['hdf_output_arrays'].
            'h5_2' --> read from .h5 files,
                    assuming input_deck['hdf_output_arrays']==2.
        '''
        return self._read_mode
    @read_mode.setter
    def read_mode(self, value):
        if value != 'h5' and value != 'h5_2':
            raise ValueError(f'read_mode {value!r} not supported.')
        self._read_mode = value

    @property
    def full_read_mode(self):
        '''full read_mode, including hdf_output_arrays information.'''
        read_mode = self.read_mode
        if read_mode == 'h5':
            hdf_output_arrays = self.input_deck['hdf_output_arrays']
            return f'{read_mode}_{hdf_output_arrays}'
        else:
            return read_mode

    @property
    def snapdir(self):
        '''directory containing the snapshot files.
        If self.full_read_mode=='h5_2', this is '{self.dirname}/parallel'.
        Otherwise, this will crash with a NotImplementedError.
        '''
        if self.full_read_mode == 'h5_2':
            return os.path.join(self.input_deck.dirname, 'parallel')
        else:
            raise NotImplementedError(f'{type(self).__name__}.snapdir, when read_mode={self.full_read_mode!r}')

    def snap_filepath(self, snap=None):
        '''convert snap to full file path for this snap.

        snap: None, str, int, or Snap
            the snapshot number to load.
            if None, use self.snap.
        '''
        if self.full_read_mode == 'h5_2':
            return self._h5_2_filename(snap=snap)
        else:
            raise NotImplementedError(f'{type(self).__name__}.snap_filepath, when read_mode={self.full_read_mode!r}')


    # # # ADDING DIMENSIONS TO VAR STRING # # #
    def _var_dimmed(self, eppic_var):
        '''return eppic_var, possibly slightly adjusted based on currently-loading dimension(s).
        Here:
            append self.component if self._loading_component
            append self.fluid.N if self._loading_fluid
        E.g. 'flux' turns into 'fluxz2' when loading 'z' component and fluid 2.
        '''
        result = eppic_var
        if getattr(self, '_loading_component', False):
            result = result + str(self.component)
        if getattr(self, '_loading_fluid', False):
            result = result + str(self.fluid.N)
        return result

    def load_direct(self, var, *args, pre_dimmed=False, **kw):
        '''load var "directly", either from a file, from cache or self.setvars, or from self.direct_overrides.
        Steps:
            1) attempt to get var from cache or self.setvars.
                [EFF] only tries this if we are not self._inside_quantity_loader_call_logic,
                to avoid redundant calls to self.get_set_or_cached.
            2) add dimensions to var if appropriate, based on the currently-loading dimension(s).
                E.g., 'flux' turns into 'fluxz2' when loading 'z' component and fluid 2.
            3) If added any dims, check if the dimmed var appears in self.setvars or self.cache.
            4) super().load_direct(dimmed_var, *args, **kw),
                which will use self.load_fromfile(...) unless any overrides apply here.

        note: does not check here if var (before adding dims) appears in self.setvars.
        '''
        # (0) - bookkeeping; delete any previous value of self._load_direct_used_override
        try:
            del self._load_direct_used_override
        except AttributeError:
            pass   # that's fine. Just want to reset it before running this function.
        # (1)
        if not getattr(self, '_inside_quantity_loader_call_logic', False):
            try:
                result = self.get_set_or_cached(var)
            except CacheNotApplicableError:
                pass
            else:
                self._load_direct_used_override = var
                return result
        # (2)
        if pre_dimmed:
            eppic_var = var
        else:
            eppic_var = self._var_dimmed(var)
            # (3)
            if eppic_var != var:  # check setvars & cache
                try:
                    result = self.get_set_or_cached(eppic_var)
                except CacheNotApplicableError:
                    pass
                else:
                    self._load_direct_used_override = eppic_var
                    return result
        # (4)
        return super().load_direct(eppic_var, *args, **kw)

    # # # "GENERIC" LOAD VAR (dispatch based on read_mode) # # #
    def load_fromfile(self, eppic_var, *args, snap=None, **kw):
        '''return numpy array of eppic_var, loaded directly from file.
        use self.full_read_mode to determine which file(s) / how to read them.

        eppic_var: str
            the name of the variable to read. Should include all dimensions as appropriate.
            E.g., use 'fluxz2', not 'flux', to get flux for fluid 2 and component z.
        snap: None, str, int, or Snap
            the snapshot number to load.
            if None, use self.snap.

        Example:
            eppic_var='fluxx1', snap=7, read_mode='h5_2'
                --> h5py.File('parallel/parallel000007.h5')['fluxx1'][:]
        '''
        snap = self._as_single_snap(snap)  # expect single snap when loading from file.
        if hasattr(snap, 'exists_for') and not snap.exists_for(self):
            result = xr.DataArray(self.snap_dim.NAN, attrs=dict(units='raw'))
            return self.assign_snap_coord(result)  # [TODO][EFF] assign coords when making array instead...
        full_read_mode = self.full_read_mode
        if full_read_mode == 'h5_2':
            return self._h5_2_load_fromfile(eppic_var, *args, snap=snap, **kw)
        # reaching this line means the read mode is not recognized.
        raise LoadingNotImplementedError(f'unsupported full_read_mode: {full_read_mode!r}')

    def directly_loadable_vars(self, snap=None):
        '''return tuple of directly loadable variables.
        These are the variables that can be loaded directly from a file,
        using the current full_read_mode.

        snap: None, str, int, or Snap
            the snapshot number to load.
            if None, use self.snap.
        '''
        snap = self._as_single_snap(snap)  # expect single snap when loading from file.
        if hasattr(snap, 'exists_for') and not snap.exists_for(self):
            return np.nan
        full_read_mode = self.full_read_mode
        if full_read_mode == 'h5_2':
            result = list(self._h5_2_directly_loadable_vars(snap=snap))
        return result

    # # # H5_2 READ MODE # # #
    def _h5_2_load_fromfile(self, eppic_var, *args__None, snap=None, **kw__None):
        '''return numpy array of var, loaded directly from file, using "h5_2" read_mode.
        This corresponds to h5 read mode with hdf_output_arrays=2.

        eppic_var: str
            the name of the variable as stored in the snapshot.
        snap: None, str, int, or Snap
            the snapshot number to load.
            if None, use self.snap.

        Example:
            eppic_var='fluxx1', snap=7
                --> h5py.File('parallel/parallel000007.h5')['fluxx1'][:]
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        filename = self._h5_2_filename(snap=snap)
        if not os.path.exists(filename):
            raise FileNotFoundError(f'{os.path.abspath(filename)!r}')
        with h5py.File(filename, 'r') as file:
            try:
                result = file[eppic_var]
            except KeyError:
                errmsg = f'var={eppic_var!r} not recognized (in file {os.path.abspath(filename)!r})'
                raise LoadingNotImplementedError(errmsg)
            if getattr(self, '_slice_maindims_in_load_direct', False):
                # [EFF] slice here instead of reading all data then slicing later.
                slices = self.slices
                slicer = tuple(slices.get(d, slice(None)) for d in self.maindims)
                return result[slicer]
            else:
                return result[:]

    def _h5_2_filename(self, *args__None, snap=None, **kw__None):
        '''return name of file from which to load values, for read_mode='h5_2'.

        snap: None, str, int, or Snap
            the snapshot number to load.
            if None, use self.snap.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        snap = self._as_single_snap(snap)
        dir_ = self.snapdir  # probably {dirname}/parallel
        file_s = snap.file_s(self) if hasattr(snap, 'file_s') else str(snap)
        snap00N = file_s.zfill(self._h5_zfill)  # e.g. '000017' if _h5_zfill=6, snap=17.
        filename = os.path.join(dir_, f'parallel{snap00N}.h5')
        return filename

    def _h5_2_directly_loadable_vars(self, *, snap=None):
        '''return tuple of directly loadable variables, for read_mode='h5_2'.'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        filename = self._h5_2_filename(snap=snap)
        with h5py.File(filename, 'r') as file:
            return tuple(file.keys())

