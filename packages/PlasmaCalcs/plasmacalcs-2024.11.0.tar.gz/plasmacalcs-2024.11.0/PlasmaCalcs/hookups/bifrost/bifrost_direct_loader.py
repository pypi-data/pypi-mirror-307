"""
File Purpose: BifrostDirectLoader
"""
import os

import numpy as np
import xarray as xr

from ...defaults import DEFAULTS
from ...errors import CacheNotApplicableError, SnapValueError
from ...tools import (
    simple_property,
    product,
)


''' --------------------- BifrostDirectLoader --------------------- '''

class BifrostDirectLoader():
    '''manages loading data directly from bifrost output files.'''
    
    # # # PROPERTIES AFFECTING DIRECT LOADING # # #
    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['stagger_direct', 'squeeze_direct'], plus any behavior_attrs from super().
        '''
        return ['stagger_direct', 'squeeze_direct'] + list(getattr(super(), 'behavior_attrs', []))

    stagger_direct = simple_property('_stagger_direct', default=True,
            doc='''whether to stagger arrays to cell centers when loading directly from file.
            if all arrays are at cell centers, don't need to worry about stagger anymore.
            else, need to be sure to align arrays before doing calculations on them.''')

    squeeze_direct = simple_property('_squeeze_direct', default=True,
            doc='''whether to squeeze arrays when loading directly from file.
            if True, remove dimensions of size 1, and alter self.maindims appropriately.''')

    def _maindims_post_squeeze(self):
        '''returns tuple of maindims remaining after squeezing if applicable. E.g. ('x', 'z').
        If not squeeze_direct or if 3D run, maindims will be ('x', 'y', 'z').
        Otherwise, remove any dims with size 1.
        '''
        if not self.squeeze_direct:
            return ('x', 'y', 'z')
        else:
            data_shape = (self.params['mx'], self.params['my'], self.params['mz'])
            return tuple(d for d, size in zip(('x', 'y', 'z'), data_shape) if size > 1)

    # # # DIRECT STAGGER INSTRUCTIONS # # #
    # {bifrost_var: ops to perform on var to align it to grid cell centers}
    _STAGGER_DIRECT_TO_CENTER_OPS = {
        # snap vars
        'r': None, 'e': None,  # None means no ops needed
        'px':'xup', 'py':'yup', 'pz':'zup',
        'bx':'xup', 'by':'yup', 'bz':'zup',
        # other vars: ??? (any other directly loadable vars that need staggering?)
        # (e.g.: 'efx': 'yup zup', 'efy': 'xup zup', 'efz': 'xup yup')
    }

    def _stagger_direct_to_center(self, array, bifrost_var):
        '''stagger directly loaded data array (of bifrost_var values) to cell centers.
        Instructions for how to stagger to center depends on bifrost_var.
        if bifrost_var doesn't require any ops to center it, do nothing.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        ops = self._STAGGER_DIRECT_TO_CENTER_OPS.get(bifrost_var, None)
        if ops is None:
            return array
        # else, stagger array to cell centers
        return self.stagger(array, ops)

    # # # FILE PATH INFO # # #
    @property
    def snapdir(self):
        '''directory containing the snapshot files.
        Here, gives self.dirname, because Bifrost outputs are stored at top-level of directory.
        '''
        return self.dirname

    def snap_filepath(self, snap=None):
        '''convert snap to full file path for this snap, i.e. to the snapname_NNN.idl file.'''
        snap = self._as_single_snap(snap)
        dir_ = self.snapdir
        file_s = snap.file_s(self) if hasattr(snap, 'file_s') else str(snap)
        filename = os.path.join(dir_, f'{self.snapname}_{file_s}.idl')
        return filename

    # # # DIRECT LOADING-RELATED INFO # # #
    def directly_loadable_vars(self, snap=None):
        '''return tuple of directly loadable variables for this snap.

        snap: None, str, int, Snap, or iterable indicating multiple snaps.
            the snapshot number to load. if None, use self.snap.
            if multiple snaps, return the result if all snaps have same result, else crash.
        '''
        kw = dict() if snap is None else dict(snap=snap)
        with self.using(**kw):
            multiple_snaps = self.snap_is_iterable()
            if multiple_snaps:
                snaps = self.snap
            else:
                snaps = [self._as_single_snap(snap)]
        result = None
        for snap in snaps:
            # result for this snap
            if hasattr(snap, 'exists_for') and not snap.exists_for(self):
                result_here = np.nan
            else:
                vpm = snap.var_paths_manager(self)
                result_here = vpm.vars
            # compare against known result
            if result is None:
                result = result_here
            elif result != result_here:
                errmsg = 'directly_loadable_vars differ between snaps. Retry with single snap instead.'
                raise SnapValueError(errmsg)
            # else, continue
        return result

    def var_paths_manager(self, snap=None):
        '''return VarPathsManager for this snap (or current snap if None provided)'''
        snap = self._as_single_snap(snap)
        return snap.var_paths_manager(self)

    @property
    def data_array_shape(self):
        '''shape of each data array. ('mx', 'my', 'mz') from self.params.
        Assumes shape is the same for all snaps; will crash if not.
        '''
        return (self.params['mx'], self.params['my'], self.params['mz'])

    @property
    def data_array_size(self):
        '''array size (number of elements) of each data array. (from data_array_shape)'''
        return product(self.data_array_shape)

    data_array_dtype = simple_property('_data_array_dtype', default=np.dtype('float32'),
            doc='''numpy dtype of each data array. default is np.dtype('float32').
            Used by np.memmap during self.load_fromfile.''')

    @property
    def data_array_nbytes(self):
        '''number of bytes in each data array. (from data_array_size and data_array_dtype)'''
        return self.data_array_size * self.data_array_dtype.itemsize

    data_array_order = simple_property('_data_array_order', default='F',
            doc='''ordering of data array axes: 'F' (Fortran) or 'C' (C order). Default 'F'.''')

    # # # LOAD DIRECT (add dimensions to var string) # # #
    def _var_dimmed(self, bifrost_var):
        '''return bifrost_var, possibly slightly adjusted based on currently-loading dimension(s).
        Here:
            append self.component if self._loading_component
        E.g. 'b' turns into 'bz' when loading 'z' component.
        '''
        result = bifrost_var
        if getattr(self, '_loading_component', False):
            result = result + str(self.component)
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
            bifrost_var = var
        else:
            bifrost_var = self._var_dimmed(var)
            # (3)
            if bifrost_var != var:  # check setvars & cache
                try:
                    result = self.get_set_or_cached(bifrost_var)
                except CacheNotApplicableError:
                    pass
                else:
                    self._load_direct_used_override = bifrost_var
                    return result
        # (4)
        return super().load_direct(bifrost_var, *args, **kw)

    # # # LOAD FROMFILE # # #
    def load_fromfile(self, bifrost_var, *args__None, snap=None, **kw__None):
        '''return numpy array of bifrost_var, loaded directly from file.

        bifrost_var: str
            the name of the variable to read. Should include all dimensions as appropriate.
            E.g. use 'bz' not 'b', to get magnetic field z-component.
        snap: None, str, int, or Snap
            the snapshot number to load. if None, use self.snap.
        '''
        snap = self._as_single_snap(snap)  # expect single snap when loading from file.
        if hasattr(snap, 'exists_for') and not snap.exists_for(self):
            result = xr.DataArray(self.snap_dim.NAN, attrs=dict(units='raw'))
            return self.assign_snap_coord(result)  # [TODO][EFF] assign coords when making array instead...
        vpm = snap.var_paths_manager(self)
        filepath = vpm.var2path[bifrost_var]
        offset = vpm.var2index[bifrost_var] * self.data_array_nbytes
        result = np.memmap(filepath, offset=offset,
                           mode='r',  # read-only; never alters existing files!
                           shape=self.data_array_shape,
                           dtype=self.data_array_dtype,
                           order=self.data_array_order,
                           )
        result = np.asarray(result)  # convert to numpy array.
        if self.stagger_direct:
            result = self._stagger_direct_to_center(result, bifrost_var)
        if self.squeeze_direct:
            assert result.shape == self.data_array_shape, "pre-squeeze shape check failed."
            result = np.squeeze(result)
        return result
