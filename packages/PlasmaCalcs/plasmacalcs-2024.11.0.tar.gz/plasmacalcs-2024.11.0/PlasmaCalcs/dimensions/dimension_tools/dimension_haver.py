"""
File Purpose: DimensionHaver
"""
import contextlib
import itertools

import numpy as np
import xarray as xr

from .dim_point import DimPoint, DimRegion
from .dimension import Dimension, _paramdocs_dimension
from ..behavior import BehaviorHaver
from ...errors import QuantCalcError
from ...tools import (
    simple_setdefaultvia_property, simple_property,
    memory_size_check_loading_arrays_like,
    repr_simple,
    format_docstring,
    alias,
    using_attrs, maintaining_attrs,
    UNSET,
    TaskArray, TaskContainerCallKwargsAttrHaver,
)
from ...tools.multiprocessing import _paramdocs_tasks
from ...defaults import DEFAULTS



''' --------------------- DimensionHaver --------------------- '''

_paramdocs_loading = {
    'loader': '''callable of (*args_loader, **kw_loader) -> xarray.DataArray.
        will call loader to get result values at each combination of dims values in self.
        (loader will probably depend on dims values from self.)''',
    'dims': '''iterable of strs or Dimension objects
        load across these Dimensions.
        loads across the current values (when this method was called) of each dimension,
            not necessarily "all" values. (e.g., self.snap, not self.snaps)
        str values --> use self.dimensions[d] (where d is a str in dims).
        len(dims)==0 --> just return loader(var, *args_loader, **kw_loader).
        While loading, set dim.loading=True for each dim.''',
    'assign_coords': '''None or bool, default None
        whether to dim.assign_coord for each result of loader, for each dimension.
        None --> assign coord only if dim.name not already in array.coords.''',
    'array_MBmax': f'''UNSET, None, or number
        maximum result size allowed, in Megabytes.
        will raise a MemorySizeError if result size would be larger than this.
        UNSET --> use DEFAULTS.ARRAY_MBYTES_MAX (default: {DEFAULTS.ARRAY_MBYTES_MAX} MB).
        None --> no limit.
        Assumes that each result (at each dimpoint) will be the same size.''',
}

class DimensionHaver(BehaviorHaver, TaskContainerCallKwargsAttrHaver):
    '''class which can have multiple Dimensions attached to it.

    Manages multiple Dimensions and provides methods for working with them, such as:
        current_n_dimpoints, dim_values, enumerate_dimpoints, get_first_dimpoint.
    Additionally, provides load_across_dims, which is useful when loading arrays from multiple files,
        e.g. see EppicBasesLoader, EbysusBasesLoader.
    The logic for managing the dimensions is implemented in __init_subclass__;
        also note the Dimensions may attach methods to subclasses of this class via setup_haver, e.g.:
            class FluidDimension(Dimension, name='fluid'):
                pass   # no special methods for this example

            @FluidDimension.setup_haver  # setup FluidHaver by attaching various relevant properties & methods.
            class FluidHaver(DimensionHaver, dimension='fluid'):
                pass   # no special methods for this example

    when defining a subclass, can provide these kwargs (e.g. class Foo(DimensionHaver, dimension=...)):
        dimension: str or None
            name of the dimension which has a current value associated with it. e.g. "fluid", "component"
        dim_plural: str or None
            plural name for dimension. if None, append 's' to dimension. e.g. "fluids", "components"
    '''
    # # # PROPERTIES DEFINED HERE # # #
    dimensions = simple_setdefaultvia_property('_dimensions', '_get_dimensions_dict',
            doc='''dict of dimensions in self; {dimension name: Dimension object}.
            e.g. {'fluid': self.fluid_dim, 'snap': self.snap_dim, ...}.''')
    def _get_dimensions_dict(self):
        '''return dict of dimensions in self; {dimension name: Dimension object}'''
        return {dim: getattr(self, f'{dim}_dim') for dim in self._dim_types}

    # # # # __INIT_SUBCLASS__ # # # #
    def __init_subclass__(cls, *, dimension=None, dim_plural=None, **kw_super):
        '''called when subclassing DimensionHaver; sets some useful attributes related to dimension.

        dimension: str or None
            name of dimension associated with this subclass.
            if None, no particular dimension associated with this subclass.
        dim_plural: str or None
            plural form of dimension. if None, use str(dimension)+'s'.
    
        Sets various attributes in cls:
            cls._dimension = dimension,
            cls._dim_plural = dim_plural,
            cls._dim_types = dict of all {dimension name: Dimension subclass} from cls and cls.__bases__
                    (note - connecting self._dimension to this dict is not handled here;
                    it is handled by __setup_haver__ called by Dimension.setup_haver)
        '''
        # defaults
        if dim_plural is None:
            dim_plural = None if dimension is None else f'{dimension}s'
        # set attributes
        cls._dimension = dimension
        cls._dim_plural = dim_plural
        cls._dim_types = dict()
        for base in cls.__bases__:
            if hasattr(base, '_dim_types'):
                cls._dim_types.update(base._dim_types)
        # call super().__init_subclass__
        super().__init_subclass__(**kw_super)

    @classmethod
    def __setup_haver__(cls, dim_cls, **kw_super):
        '''called by dim_cls.setup_haver(cls) when setting up cls so that it "has" dim_cls dimension.'''
        cls._dim_types[cls._dimension] = dim_cls
        # call method from super if it exists
        try:
            super_setup = super().__setup_haver__
        except AttributeError:
            pass
        else:
            super().__setup_haver__(dim_cls, **kw_super)

    # # # # MULTI-DIMENSION-BASED METHODS # # # #
    # # GENERIC / HELPER METHODS # #
    def dims_get(self, attr, dims=None):
        '''return dict of {dim: getattr(self.dimensions[dim], attr) for dim in dims}.
        dims: None or iterable
            if provided, only include these dimensions.
        See also: dims_apply
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        dimensions = self.dimensions if dims is None else dims
        result = dict()  # could use dict-comprehension, but explicit looping makes debugging easier.
        for d in dimensions:
            result[d] = getattr(self.dimensions[d], attr)
        return result

    def dim_values(self, dims=None):
        '''return dict of current values for dimensions in self.
        dims: None or iterable
            if provided, only include these dimensions.
        Equivalent: DimRegion(self.dims_get('v', dims=dims))
        '''
        return DimRegion(self.dims_get('v', dims=dims))

    @property
    def dims(self):
        '''return dict of current values for dimensions in self. Equivalent: self.dim_values()'''
        return self.dim_values()

    def dims_apply(self, funcname, *args_func, dims=None, **kw_func):
        '''apply funcname to each dimension in self, with args_func and kw_func.
        dims: None or iterable of strs
            if provided, only apply to these dimensions.
        See also: dims_get
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        funcs = self.dims_get(funcname, dims)
        result = dict()  # could use dict-comprehension, but explicit looping makes debugging easier.
        for d, f in funcs.items():
            result[d] = f(*args_func, **kw_func)
        return result

    # # DIMPOINTS # #
    def current_n_dimpoints(self, dims=None):
        '''return number of points represented by current values of dims.
        dims: None or iterable of strs appearing in self.dimensions.keys()
            dimensions to consider. None --> use all dimensions.

        E.g. current_n_dimpoints(self, dims=['fluid', 'snap']) --> number of (fluid, snap) points;
            e.g. 3 fluids and 2 snaps --> 6 points.

        Note, for classes using maindims, maindims are not included in the number of dimpoints.

        Equivalent to len(list(self.iter_dimpoints(dims=dims, current=True)))
        '''
        ndims = self.dims_apply('current_n', dims=dims)
        result = 1
        for n in ndims.values():
            result = result * n
        return result

    def iter_dimpoints(self, dims=None, *, all=False, restore=True, enumerate=False):
        '''iterate through values of dims, returning DimPoints and setting dim values during iteration.
        DimPoints are dicts of {dim: value} for dim in dims, where not is_iterable_dim(value).
        Also, during iteration, set self.{dim} = value, as with self.iter_dim.

        dims: None or iterable of strs appearing in self.dimensions.keys()
            dimensions to consider. None --> use all dimensions.
        all: bool
            whether to iterate through all possible values, or only the current values.
            False --> iterate through current values (e.g., self.snap, self.fluid, ...).
                    similar to itertools.product(self.iter_snap(), self.iter_fluid(), ...)
            True --> iterate through all possible values (e.g., self.snaps, self.fluid, ...)
                    similar to itertools.product(self.iter_snaps(), self.iter_fluids(), ...)
                    Equivalent to all=False if all dims are set to None, e.g. self.snap=None, ...
        restore: bool
            whether to restore original dim values after iteration.
        enumerate: bool, default False
            whether to yield indices too, i.e. (idx, DimPoint) instead of just DimPoint.
            idx would be a dict of {dim: i} such that DimPoint values are {dim: dims[i] for dim,i in idx.items()}.
        '''
        dims = self.dimensions if dims is None else dims
        applying = 'iter_values' if all else 'iter'
        iters = self.dims_apply(applying, dims=dims, enumerate=enumerate)
        # itertools.product consumes all the iters before actually iterating,
        #   so it won't set or restore values during iteration.
        with self.maintaining(**{dim: restore for dim in dims}):
            for vals in itertools.product(*iters.values()):
                if enumerate:
                    idx = {dim: val[0] for dim, val in zip(dims, vals)}
                    point = DimPoint({dim: val[1] for dim, val in zip(dims, vals)})
                    self.set_attrs(**point)
                    yield (idx, point)
                else:
                    point = DimPoint({dim: val for dim, val in zip(dims, vals)})
                    self.set_attrs(**point)
                    yield point

    def enumerate_dimpoints(self, dims=None, *, all=False):
        '''iterate through values of dims, yielding (idx, DimPoint) pairs.
        idx is a dict of {dim: i} such that DimPoint values are {dim: dims[i] for dim,i in idx.items()}.
        Also, during iteration, set self.{dim} = value, as with self.iter_dim.

        Equivalent to self.iter_dimpoints(dims=dims, all=all, enumerate=True)
        '''
        return self.iter_dimpoints(dims=dims, all=all, enumerate=True)

    def as_single_dimpoint(self, values=None, *, dims=None, **values_as_kw):
        '''return DimPoint with values for dims, but raise DimensionValueError if any value is_iterable_dim.
        values: None or dict
            values to use for the dimpoint.
                values will be joined with **values_as_kw; provided any of either will be equivalent.
                E.g. can use values={'fluid': 'e'} or use fluid='e'.
            if any are provided --> use values corresponding to self.{dim}=values[dim] for dim in dims.
            else --> use values of self.{dim} for dim in dims. (equivalent: self.dims_apply('_as_single', dims=dims)) 
        dims: None or iterable of strs appearing in self.dimensions.keys()
            dimensions to include.
            None --> infer dimensions from keys of values (and values_as_kw).
                    if no values were provided (values=None, and empty values_as_kw),
                        use all dimensions from self.dimensions.keys().

        additional kwargs provide other {dim: value} items.

        Examples:
            self.as_single_dimpoint() --> DimPoint({dim: self.{dim} for dim in self.dimensions})
            self.as_single_dimpoint({'fluid': 'e'}) --> DimPoint({'fluid': 'e'})
            self.as_single_dimpoint(fluid='e') --> DimPoint({'fluid': 'e'})
            self.as_single_dimpoint({'fluid': 'e'}, snap=0) --> DimPoint({'fluid': 'e', 'snap': 0})
            self.as_single_dimpoint(dims=['fluid', 'snap']) --> DimPoint({'fluid': self.fluid, 'snap': self.snap})
        '''
        values_dict = dict() if values is None else values
        vals_to_use = {**values_dict, **values_as_kw}
        if dims is None:  # infer from keys of vals_to_use.
            dims = list(vals_to_use.keys()) if len(vals_to_use)>0 else None
            # if dims is still None, the dims_apply method will use all dimensions from self.dimensions.keys().
        with self.using(**vals_to_use):
            result = self.dims_apply('_as_single', dims=dims)  # << raises DimensionValueError if necessary
            return DimPoint(result)

    def get_first_dimpoint(self, dims=None, *, enumerate=False):
        '''return DimPoint taking the first value of each dim in self.dimensions.
        dims: None or iterable of strs appearing in self.dimensions.keys()
            dimensions to include. None --> use all dimensions.
        enumerate: bool
            whether to return (idx, DimPoint) instead of just DimPoint.
        '''
        point = DimPoint(self.dims_apply('_get_first', dims=dims))
        if enumerate:
            idx = {dim: 0 for dim in point}
            return (idx, point)
        else:
            return point

    def using_first_dimpoint(self, dims=None):
        '''return context manager which sets dimensions to their first values (when called); restore original on exit.
        Useful for testing a single code at a single dimpoint without needing to set each dimension individually.
        dims: None or iterable of strs appearing in self.dimensions.keys()
            dimensions to include. None --> use all dimensions.
        '''
        first_point = self.get_first_dimpoint(dims=dims)
        return self.using(**first_point)

    # # ATTRS MANIPULATION # #
    def pop_dim_keys(self, kw):
        '''return ({key: kw.pop(key) for key in self.dimensions if key in kw}, kw).'''
        return ({key: kw.pop(key) for key in self.dimensions if key in kw}, kw)

    def set_pop_dim_attrs(self, kw):
        '''set self.{key} = kw.pop(key) for each key in self.dimensions if key in kw.'''
        for key in self.dimensions:
            if key in kw:
                setattr(self, key, kw.pop(key))

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns list(self.dimensions.keys()), plus any behavior_attrs from super().

        (note: if self._dims_in_behavior_attrs=False, only return behavior_attrs from super().)
        '''
        # note: _dims_in_behavior_attrs property is defined by BehaviorHaver in behavior.py.
        super_attrs = list(getattr(super(), 'behavior_attrs', []))
        if getattr(self, '_dims_in_behavior_attrs', True):
            return list(self.dimensions.keys()) + super_attrs
        else:
            return super_attrs

    def assign_dim_coords(self, array, *dims, skip=[]):
        '''assign all dimensions in self as coords for array. (self.assign_{dim}_coord(array))
        Assumes array is an xarray and does not have any dimensions in self.
        (array is not edited directly; returns result of assigning coords.)

        dims: iterable of dimensions in self
            assign only these dimensions as coords. (use all dimensions if len(dims)==0)
        skip: iterable of dimensions in self
            do not assign these dimensions as coords.
        '''
        if len(dims)==0:
            dims = self.dimensions
        if len(skip) > 0:
            dims = [dim for dim in dims if dim not in skip]
        for dim in dims:
            array = getattr(self, f'assign_{dim}_coord')(array)
        return array

    def set_attrs(self, **attrs):
        '''sets these attrs in self.'''
        for attr, val in attrs.items():
            setattr(self, attr, val)
    
    using_attrs = using_attrs
    using = alias('using_attrs')
    maintaining_attrs = maintaining_attrs
    maintaining = alias('maintaining_attrs')

    # # LOADING # #
    # multiprocessing-related properties inherited from TaskContainerCallKwargsAttrHaver; define defaults here:
    def _default_ncpu(self):
        '''return default for ncpu during self.load_across_dims. returns DEFAULTS.LOADING_NCPU'''
        return DEFAULTS.LOADING_NCPU
    def _default_timeout(self):
        '''return default for timeout during self.load_across_dims. returns DEFAULTS.LOADING_TIMEOUT'''
        return DEFAULTS.LOADING_TIMEOUT
    def _default_ncoarse(self):
        '''return default for ncoarse during self.load_across_dims. returns DEFAULTS.LOADING_NCOARSE'''
        return DEFAULTS.LOADING_NCOARSE

    # other properties for loading
    array_MBmax = simple_property('_array_MBmax', default=None, doc=_paramdocs_loading['array_MBmax'])
    @array_MBmax.getter
    def array_MBmax(self):
        '''return self._array_MBmax if it exists and is not None. Else, return DEFAULTS.ARRAY_MBYTES_MAX.'''
        result = getattr(self, '_array_MBmax', None)
        return DEFAULTS.ARRAY_MBYTES_MAX if result is None else result

    @property
    def _extra_kw_for_quantity_loader_call(self):
        '''extra kwargs which can be used to set attrs self during self.__call__.
        The implementation here returns ['ncpu', 'timeout', 'ncoarse', 'print_freq', 'array_MBmax']
            + any values from super().
        '''
        kw_here = ['ncpu', 'timeout', 'ncoarse', 'print_freq', 'array_MBmax']
        kw_super = getattr(super(), '_extra_kw_for_quantity_loader_call', [])
        return kw_here + kw_super

    # helper methods for load_across_dims
    def _call_loader_at_dimpoint(self, dimpoint, loader, args_loader, **kw_loader):
        '''with self.using(**dimpoint): return loader(*args_loader, **kw_loader)'''
        with self.using(**dimpoint):
            return loader(*args_loader, **kw_loader)

    def _call_loader0_at_dimpoint(self, dimpoint, loader0, args_loader, *, nload, MBmax, **kw_loader):
        '''return self._call_loader_at_dimpoint(dimpoint, loader0, ...).
        Also does memory size check based on nload and MBmax.
        intended for internal use only, inside load_across_dims.

        arr0 is handled differently from other arrays in order to do some checks.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        result = self._call_loader_at_dimpoint(dimpoint, loader0, args_loader, **kw_loader)
        memory_size_check_loading_arrays_like(result, nload=nload, MBmax=MBmax)  # crashes if too large!
        return result

    # load_across_dims
    @format_docstring(default_ncpu=DEFAULTS.LOADING_NCPU,
                      default_timeout=DEFAULTS.LOADING_TIMEOUT,
                      default_ncoarse=DEFAULTS.LOADING_NCOARSE,
                      default_print_freq=DEFAULTS.PROGRESS_UPDATES_PRINT_FREQ)
    @format_docstring(**_paramdocs_loading, **_paramdocs_tasks, sub_ntab=2)
    def load_across_dims(self, loader, *args_loader, dims=[], assign_coords=None,
                         loader0=None, **kw_loader):
        '''return loader(...), iterating & joining across each dimension.

        loader: {loader}
        dims: {dims}
        assign_coords: {assign_coords}
        loader0: None or callable
            if provided, use loader0 to get the first array, then use loader for the rest.
            Internally the first array's .coords and .attrs are used to label the result;
            however all other arrays do not need to be converted to xarray.

        --- MULTIPROCESSING STRATEGY OPTIONS (from self) ---
        timeout: {timeout}
                # [TODO] make this happen, without making self un-picklable:
                in case of crash, results so far can be found in self._latest_load_tasks.
                Then possibly continued via:
                    results = self._latest_load_tasks(..., reset=False, skip_done=True)
                    result = self._load_across_dims_postprocess(results, dims, ...)
                    # [TODO] if crashing and resuming is common, make that easier to do^
            if self.timeout has not been set, use DEFAULTS.LOADING_TIMEOUT (default: {{default_timeout}}).
        ncpu: {ncpu}
            if self.ncpu has not been set, use DEFAULTS.LOADING_NCPU (default: {{default_ncpu}}).
        ncoarse: {ncoarse}
            if self.ncoarse has not been set, use DEFAULTS.LOADING_NCOARSE (default: {{default_ncoarse}}).
        print_freq: {print_freq}
            if self.print_freq has not been set, use DEFAULTS.PROGRESS_UPDATES_PRINT_FREQ (default: {{default_print_freq}}).

        additional args & kwargs are passed as loader(*args_loader, **kw_loader).
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        if len(dims) == 0:
            return loader(*args_loader, **kw_loader)
        # else, at least 1 dim.
        dimnames = list(dims)
        dims = [(d if isinstance(d, Dimension) else self.dimensions[d]) for d in dimnames]
        # memory size check logic
        MBmax = self.array_MBmax
        nload = self.current_n_dimpoints(dims=dimnames)
        # multiprocessing strategy
        mp_strategy = dict(ncpu=self.ncpu, timeout=self.timeout, ncoarse=self.ncoarse, print_freq=self.print_freq)
        _var = args_loader[0] if args_loader else kw_loader.get('var', None)
        _varstr = f' var={_var!r},' if isinstance(_var, str) else ''
        _printable_process_name = f'load_across_dims({loader.__name__},{_varstr} dims={dimnames}, ...)'
        # # METHOD 4 SETUP # #
        it_dimnames = [d.name for d in dims if d.is_iterable()]
        dshape = tuple(d.current_n() for d in dims if d.is_iterable())
        task_inputs = np.empty(dshape, dtype=object)
        # # START LOADING # #
        with contextlib.ExitStack() as context_stack:
            # set loading=(whether dim is being loaded across here), within this 'with' block.
            for d in dims:
                context_stack.enter_context(d.using(loading=True))
            unused_dims = [self.dimensions[d] for d in self.dimensions if d not in dimnames]
            for d in unused_dims:
                context_stack.enter_context(d.using(loading=False))
            # set ncpu=1 for all internal calculations (can't multiprocess inside a multiprocess)
            context_stack.enter_context(self.using(ncpu=1, pool=None))
            # restore dim values after loading, even if crash in the middle of exit block for self.using.
            #   (e.g. lots of small loading tasks + timeout error --> decent chance to crash in exit block.
            context_stack.enter_context(self.maintaining(*dimnames))
            # # LOAD ACROSS POINTS # #
            # # METHOD 4 # # -- assign all coords at the end. Use loader0 to get first array.
            #   rewritten to use TaskArray, which allows for multiprocessing.
            # setup task array
            for i, (idx, dimpoint) in enumerate(self.enumerate_dimpoints(dims=dimnames)):
                i_task = tuple(idx[d] for d in it_dimnames)  # index within tasks array
                if i == 0:
                    if loader0 is None:
                        loader0 = loader
                    task_inputs[i_task] = (self._call_loader0_at_dimpoint,
                                           (dimpoint, loader0, args_loader),
                                           {**kw_loader, 'nload': nload, 'MBmax': MBmax})
                else:
                    task_inputs[i_task] = (self._call_loader_at_dimpoint,
                                           (dimpoint, loader, args_loader),
                                           kw_loader)
            # perform tasks
            tasks = TaskArray(task_inputs, shape=dshape, printable_process_name=_printable_process_name)
            # self._latest_load_tasks = tasks   # want to do this. But, it makes self un-picklable...)
            arrs = tasks(**mp_strategy)
            result = self._load_across_dims_postprocess(arrs, dims, it_dimnames=it_dimnames, assign_coords=assign_coords)
            # SINGLE PROCESSOR WAY TO DO METHOD 4:
            # for idx, point in self.enumerate_dimpoints(dims=dimnames):
            #     # (note: enumerate_dimpoints sets dims' values during iteration)
            #     # load array
            #     if arr0 is None:
            #         array = loader0(*args_loader, **kw_loader)
            #         arr0 = array
            #     else:
            #         array = loader(*args_loader, **kw_loader)
            #     # postprocessing - memory size check
            #     if not memory_size_checked:
            #         memory_size_check_loading_arrays_like(array, nload=n_loading, MBmax=MBmax)
            #         memory_size_checked = True
            # # [EFF] TRYING DIFFERENT METHODS FOR EFFICIENCY # #
            # # all methods should produce equivalent results # #
            # # METHOD 1 # # -- old attempt
            #   always slower than method 2 --> removed.
            # # METHOD 2 # # -- assign final coords after all vars loaded.
            #   always slower than method 4 --> removed.
            # # METHOD 3 # # -- many assign_coord calls then xr.combine_by_coords(arrs).
            #   always slower than method 2 --> removed.
        return result

    def _load_across_dims_postprocess(self, arrs, dims, *, it_dimnames, assign_coords):
        '''postprocessing results from load_across_dims, after all tasks have been completed.
        i.e., after all arrays have been loaded, join them all together.

        [EFF] if xarray.DataArray, assumes all arrays have the same shape.
        '''
        try:
            arr0 = arrs.flat[0]
        except IndexError:
            errmsg = 'No arrays loaded; maybe due to empty self.enumerate_dimpoints(dims=dimnames)'
            raise QuantCalcError(errmsg) from None
        # join final results
        if isinstance(arr0, xr.DataArray):
            if any(arr.shape != arr0.shape for arr in arrs.flat):
                errmsg = ('[TODO] load_across_dims where some results have different shape. '
                          'Eventual implementation should broadcast if shapes compatible. '
                          f'Here, got shapes: {[arr.shape for arr in arrs.flat]}.')
                raise NotImplementedError(errmsg)
            dims_result = tuple([*it_dimnames, *arr0.dims])
            coords_result = arr0.coords.copy()
            for d in dims: # delete any coords that will be reassigned later!
                if d.name in coords_result:
                    del coords_result[d.name]
            if arr0.dtype.type is np.str_:  # special case...
                # without doing the conversion here, we get crash with:
                #    ValueError: setting an array element with a sequence
                # from call to np.asarray(arrs.tolist()) when each arr is an xr.DataArray of str(s).
                # this may be a bug with xarray itself; tested with xarray version '2024.6.0'.
                # but for now, the workaround here is fine to fix things!
                arrs_data = np.vectorize(lambda arr: arr.data)(arrs)
                arrlist = arrs_data.tolist()
            else:
                arrlist = arrs.tolist()
            result = xr.DataArray(arrlist, dims=dims_result, coords=coords_result, attrs=arr0.attrs)
            # assign coords for final result
            for d in dims:
                if d.is_iterable():
                    result = d.assign_coord_along(result, d.name)
                else:
                    result = d.assign_coord(result, overwrite=(assign_coords is not None))
        elif isinstance(arr0, xr.Dataset):
            # similar to above but handle each data var separately!
            # [TODO] encapsulate some of this stuff somewhere else?
            results = {k: [] for k in arr0.keys()}
            for k in results:
                k_arr0 = arr0[k]
                dims_k = tuple([*it_dimnames, *k_arr0.dims])
                coords_k = k_arr0.coords.copy()
                for d in dims: # delete any coords that will be reassigned later!
                    if d.name in coords_k:
                        del coords_k[d.name]
                # k_arrs is similar to arrs but for data var k, only.
                k_arrs = np.empty(arrs.shape, dtype=object)
                for idx, arr in np.ndenumerate(arrs):
                    k_arrs[idx] = arr[k]
                results[k] = xr.DataArray(k_arrs.tolist(), dims=dims_k, coords=coords_k, attrs=k_arr0.attrs)
                # assign coords for final result
                for d in dims:
                    if d.is_iterable():
                        results[k] = d.assign_coord_along(results[k], d.name)
                    else:
                        results[k] = d.assign_coord(results[k], overwrite=(assign_coords is not None))
            result = xr.Dataset(results, attrs=arr0.attrs)
        else:
            raise QuantCalcError(f'Unexpected type for arr0: {type(arr0)}; expected xarray.DataArray or Dataset.')
        return result

    @format_docstring(**_paramdocs_loading, sub_ntab=1)
    def load_across_dims_implied_by(self, var, loader, *args_loader, assign_coords=None,
                                    _min_split=1, **kw_loader):
        '''return loader(...), iterating & joining across each dimension implied by var.
        Equivalent to self.load_across_dims(loader, ..., dims=self.match_var_loading_dims(var)).

        var: str
            variable which implies dims to load across, via self.match_var_loading_dims(var).
        loader: {loader}
        assign_coords: {assign_coords}
        _min_split: int, default 1
            if an implied dim has current_n() < min_split, don't load across it.
            1 --> no minimum.

        additional args & kwargs are passed as loader(*args_loader, **kw_loader).
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        dims = self.match_var_loading_dims(var)
        if _min_split is not None:
            dims = [d for d in dims if self.dimensions[d].current_n() >= _min_split]
        return self.load_across_dims(loader, *args_loader, dims=dims, assign_coords=assign_coords,
                                     **kw_loader)

    # # # # DISPLAY # # # #
    def _repr_contents(self):
        '''return list of contents to go in repr of self.'''
        return [f'dims={repr_simple(self.dims)}']

    def __repr__(self):
        contents = ', '.join(self._repr_contents())
        return f"{type(self).__name__}({contents})"

