"""
File Purpose: manipulating xarrays
"""
import warnings

import numpy as np
import xarray as xr
from xarray.core.rolling import DataArrayCoarsen
# note: can't use "xr.core.rolling.DataArrayCoarsen" directly in a new python kernel,
#    although it does work after creating an xr.DataArray.coarsen() object.
from .imports import ImportFailed
try:
    import scipy.ndimage as scipy_ndimage
except ImportError as err:
    scipy_ndimage = ImportFailed('scipy.ndimage',
            'This module is required for some filtering functions.', err=err)

from .arrays import interprets_fractional_indexing
from .math import float_rounding as math_float_rounding
from .os_tools import next_unique_name
from .pytools import format_docstring
from .sentinels import UNSET
from .xarray_accessors import (
    pcAccessor, pcArrayAccessor, pcDatasetAccessor,
    # use pcAccessor.register if the function works on DataArray and Dataset inputs,
    # or pcArrayAccessor.register if the function works only on DataArray inputs,
    # or pcDatasetAccessor.register if the function works only on Dataset inputs.
)
from ..errors import (
    DimensionalityError, DimensionValueError, DimensionKeyError,
    InputError, InputConflictError, InputMissingError,
)
from ..defaults import DEFAULTS


''' --------------------- Docstrings --------------------- '''

_paramdocs_ensure_dims = {
    'promote_dims_if_needed': '''bool
        whether to promote non-dimension coords to dimensions.
        if False, raise DimensionKeyError if any relevant coord is not already a dimension.''',
    'missing_dims': '''str in ('ignore', 'warn', 'raise')
        what to do if any coord is not found:
            'ignore' --> do nothing.
            'warn' --> raise a warning.
            'raise' --> raise DimensionKeyError.''',
}

''' --------------------- Functions --------------------- '''

def is_iterable_dim(value, *, min_length=None):
    '''returns whether value represents multiple values (of a dimension).

    if value.ndim exists,
        return False if ndim==0,
        else True if ndim > 0,
        else raise DimensionValueError.
    # else, return whether iter(value) succeeds.  # <-- no longer used; use is_scalar from xr.
    else, return (not xr.core.utils.is_scalar(value))

    min_length: None or int
        if provided, before returning True, require that len(value) >= min_length.
    '''
    if hasattr(value, 'ndim'):
        ndim = value.ndim
        if ndim == 0:
            result = False
        elif ndim > 0:
            result = True
        else:
            raise DimensionValueError(f"expected ndim >= 0, but got ndim={ndim}.")
    else:
        # try:
        #     iter(value)
        # except TypeError:
        #     result = False
        # else:
        #     result = True
        result = (not xr.core.utils.is_scalar(value))
    if result and (min_length is not None):
        try:
            L = len(value)
        except TypeError:
            result = False  # couldn't determine length, so assume it's not long enough.
        else:
            result = result and (L >= min_length)
    return result

def take_along_dimension(dimension, array, at=None, *, i=None, default=UNSET, drop_labels=False, as_dict=False, item=False):
    '''returns something like: [array.sel({dimension: val}) for val in ``at``]
    i.e., list of taking these values along this dimension of array.

    at: None or list-like of values in this dimension
        take at these values. None --> use values from array.coords[dimension]
    i: None or indices.
        (if provided) take only at these indices; use isel.
    default: UNSET or any value
        if provided, use this value for any at[i] not in array.coords[dimension].
        if not already an xarray.DataArray, convert it, and set coords[dimension]=at[i].
            (e.g. take_along_dimension('component', arr, at=['x'], default=0),
            if arr doesn't have 'component'=='x', will give xarray.DataArray(0, coords={'component': 'x'}))
    drop_labels: bool, default False
        if True, drop the labels along the taken dimension.
        E.g., if dimension=='component' and labels=['x', 'y'],
            by default, result[0].component=='x' and result[1].component=='y'
            but if drop_labels then result[0] and result[1] will not have .component at all.
    as_dict: bool, default False
        if True, return dict of {dim value: array value at this dim}
            (instead of a list of array value at each dim value)
    item: bool
        if True, convert arrays to single values via array.item().

    if array is 0-d along dimension,
        returns [array] if labels corresponds to the one label in this dimension.
    '''
    if i is not None:
        if at is not None:
            raise InputConflictError('cannot provide both "at" and "i".')
        iseled = array.isel({dimension: i})
        return take_along_dimension(dimension, iseled, drop_labels=drop_labels, as_dict=as_dict)
    # else, i is None
    coords = array.coords[dimension]
    # 0d coords
    if coords.ndim == 0:
        coord = coords.item()
        if at is None:
            result = [array]
            used_at = [coord]
        else:
            if all(val == coord for val in at):
                result = [array] * len(at)  # list multiplication
                used_at = at
            else:
                errmsg = (f'provided value for "at" is incompatible with 0-d {dimension!r} values; '
                          f'\ncoords={coords};\nat={at}')
                raise DimensionalityError(errmsg)
    # 1d coords
    elif coords.ndim == 1:
        if at is None:
            # use all of them.
            result = [array.isel({dimension: i_}) for i_ in range(len(coords))]
            used_at = [val.item() for val in coords]
        else:
            # use only some of them.
            # [TODO] xarray.sel doesn't really like DimensionValue... why not?
            #   (using another way to do it, in the meantime.)
            result = []
            for val in at:
                i_ = np.nonzero((coords == val).values)[0]
                if len(i_) == 0:
                    if default is UNSET:
                        raise DimensionValueError(f'no match for val={val!r} in coords={coords}')
                    else:
                        if isinstance(default, xr.DataArray):
                            result.append(default)
                        else:
                            result.append(xr.DataArray(default, coords={dimension: val}))
                elif len(i_) == 1:
                    result.append(array.isel({dimension: i_[0]}))
                else:
                    raise DimensionValueError(f'expected 1 match, but got {len(i_)} matches for val={val!r}')
            used_at = at
    # 2d+ coords
    else:
        raise NotImplementedError(f'take_along_dimension {dimension!r} with ndim={coords.ndim}')
    # postprocessing / bookkeping
    if drop_labels:
        result = [array.drop_vars(dimension) for array in result]
    if item:
        result = [array.item() for array in result]
    if as_dict:
        result = {val: array for val, array in zip(used_at, result)}
    return result

@pcAccessor.register
def take_along_dimensions(array, dimensions):
    '''returns result of taking array along each of these dimensions, in order.
    result will be a numpy array with dtype=object, shape=(d0, d1, ...),
        where di = len(array.coords[dimensions[i]]).
    each element of result will be an xarray.DataArray.

    any dimension can be None --> result shape will be 1 at that dimension, and nothing will be taken.
        E.g. take_along_dimensions(array, [None, 'fluid']) gives array of shape (1, len(fluids)).
    '''
    shape = tuple((1 if dim is None else len(array.coords[dim])) for dim in dimensions)
    result = np.empty(shape, dtype=object)
    for idx, coord in np.ndenumerate(result):
        selecting = {dim: array.coords[dim][i] for dim, i in zip(dimensions, idx) if dim is not None}
        result[idx] = array.sel(selecting)
    return result

def join_along_dimension(dimension, arrays, labels=None, *, coords='minimal', **kw_xarray_concat):
    '''returns xr.concat(arrays, dimension). if len(arrays) == 1, instead return arrays[0], unchanged.
    if labels is provided, set result[dimension] = labels
    '''
    if len(arrays) == 1:
        return arrays[0]
    result = xr.concat(arrays, dimension, coords=coords, **kw_xarray_concat)
    if labels is not None:
        result[dimension] = labels
    return result

@pcAccessor.register('differentiate')
def xarray_differentiate(array, coord, *, keep_attrs=True, **kw__differentiate):
    '''differentiate array along coord, treating array like it is an xarray.DataArray.
    more lenient than xarray.DataArray.differentiate;
        returns 0 if can't differentiate along coord (due to coord having size 1 or not existing.)

    keep_attrs: bool
        whether to copy attrs from array into the result. Default True.

    requires that array.coords and array.differentiate exist, otherwise raises AttributeError.
    '''
    coords = array.coords
    try:
        coords_x = coords[coord]
    except KeyError:
        return xr.zeros_like(array)
    size_x = np.size(coords_x)
    if size_x <= 1:
        return xr.zeros_like(array)
    else:
        result = array.differentiate(coord, **kw__differentiate)
        if keep_attrs:
            result = result.assign_attrs(array.attrs.copy())
        return result

@pcAccessor.register('rename')
def xarray_rename(array, names=None, **more_names):
    '''return array.rename(names, **more_names), but skip any names not found in array.coords.
    names should be a dict, if provided.
    '''
    if names is not None:
        more_names.update(names)
    apply_names = {name: val for name, val in more_names.items() if name in array.coords}
    return array.rename(apply_names)

@pcAccessor.register('assign')
def xarray_assign(array, coords=None, attrs=None, *, overwrite=None):
    '''array.assign_coords(coords).assign_attrs(attrs).
    
    coords: None or dict of {dim: coord}
        each coord must be "non-iterable", as per is_iterable_dim().
    attrs: None or dict
        assign these attrs. dict of arbitrary values.
    overwrite: None or bool
        whether to overwrite an existing value for coord in array.
        (note - array will never be altered here; only the result might be altered.)
        If any coord already in array.coords, behavior depends on overwrite:
            None --> crash with DimensionKeyError.
            True --> overwrite the coord using the new value.
            False --> return array, unchanged.
    '''
    if 'tottime' not in xarray_assign.__dict__:
        xarray_assign.tottime = 0
    import time
    starttime = time.time()
    array0 = array  # helps with debugging
    if coords is not None:
        for dim, val in coords.items():
            if is_iterable_dim(val):
                errmsg = (f'cannot assign iterable coord; dim={dim!r}, val={val!r}')
                raise DimensionValueError(errmsg)
        if not overwrite:
            coords_already_assigned = set(array.coords).intersection(coords)
            if coords_already_assigned:
                if overwrite is None:
                    errmsg = (f'cannot assign already-assigned coords: {coords_already_assigned}, '
                              f'when overwrite=None.\nTo disable this error, use '
                              f'overwrite=True to update existing coords, or False to skip existing coords.')
                    raise DimensionKeyError(errmsg)
                else:
                    coords = {dim: val for dim, val in coords.items() if dim not in coords_already_assigned}
        if len(coords) > 0:
            array = array.assign_coords(coords)
    if attrs is not None:
        array = array.assign_attrs(attrs)
    xarray_assign.tottime += time.time() - starttime
    return array

@pcAccessor.register('promote_dim')
def xarray_promote_dim(array, coord):
    '''Promote this coord to be a dimension, if it isn't already.
    
    coord: str
        name of coord to promote.
        if already in array.dims, do nothing.
        if 0D, array.expand_dims(coord).
                (This occurs when coord has no associated dimension, in array.)
        if 1D, array.swap_dims(dict(dim=coord)),
                where dim is the dimension associated with coord.
        if 2D+, crash with DimensionalityError.

    returns array, or a copy of array where coord is one of the dimensions.
    '''
    if coord in array.dims:
        return array
    c = array.coords[coord]
    cdims = c.dims
    if len(cdims) == 0:
        return array.expand_dims(coord)
    elif len(cdims) == 1:
        return array.swap_dims({cdims[0]: coord})
    # else:  # len(cdims) >= 2
    errmsg = (f'cannot promote coord={coord!r} to dimension, because it has ndim={len(cdims)} > 1; '
                f'cdims={cdims}')
    raise DimensionalityError(errmsg)

@pcAccessor.register('promote_dims')
@format_docstring(**_paramdocs_ensure_dims)
def xarray_ensure_dims(array, coords, *,
                       promote_dims_if_needed=True, missing_dims='raise',
                       assert_1d=False, return_existing_dims=False):
    '''return array but ensure these coords are dimensions.

    coords: str or iterable of strings
        coords to ensure are dimensions.
    promote_dims_if_needed: {promote_dims_if_needed}
            0D coord --> array.expand_dims(coord)
            1D coord --> array.swap_dims(dict(dim=coord)) for associated dim
            2D+ coord --> crash with DimensionalityError.
    missing_dims: {missing_dims}
    assert_1d: bool, default False
        whether to assert that each of these coords is 1D (after promoting if needed).
    return_existing_dims: bool, default False
        True --> returns [array, set of dims (from input coords) which actually exist]
        probably only useful if missing_dims != 'raise'.
    '''
    if isinstance(coords, str):
        coords = [coords]
    found_missing_dims = set()
    # promote coords
    for cname in coords:
        if promote_dims_if_needed and cname in array.coords:
            array = xarray_promote_dim(array, cname)
        if cname not in array.dims:
            found_missing_dims.add(cname)
            continue
        if assert_1d:
            c = array.coords[cname]
            if c.ndim != 1:
                errmsg = f'ensure_dims expected 1D coord={cname!r}, but got ndim={c.ndim}.'
                raise AssertionError(errmsg)
    # handle missing dims
    if len(found_missing_dims) > 0:
        if missing_dims not in ('ignore', 'warn', 'raise'):
            errmsg = f'invalid missing_dims={missing_dims!r}. Expected "ignore", "warn" or "raise".'
            raise InputError(errmsg)
        if missing_dims =='raise' or missing_dims == 'warn':  # define the error message
            c_or_d = 'coords' if promote_dims_if_needed else 'dims'
            errmsg = (f'Dimensions {found_missing_dims} not found in '
                      f'array.{c_or_d}={set(getattr(array, c_or_d))},\n'
                      f'and missing_dims={missing_dims!r} (using "ignore" would ignore this instead).')
            if missing_dims == 'raise':
                raise DimensionKeyError(errmsg)
            elif missing_dims == 'warn':
                warnings.warn(errmsg)
    # return result
    if return_existing_dims:
        existing_dims = set(coords) - found_missing_dims
        return array, existing_dims
    else:
        return array

@pcAccessor.register
def nondim_coord_values(array, *, scalars_only=False):
    '''returns dict of {coord name: coord.values} for all non-dimension coords (not in array.dims).
    if scalars_only, only return coord.values with ndim==0.
    '''
    result = {cname: coord.values for cname, coord in array.coords.items() if cname not in array.dims}
    if scalars_only:
        result = {cname: val for cname, val in result.items() if np.ndim(val) == 0}
    return result

@pcAccessor.register('dims_coords')
def xarray_dims_coords(array, *, include_dims_as_coords=True):
    '''returns dict of {dim name: [coord name for all coords with this dim]}.
    result[()] will be list of all scalar coords (ndim=0 so no associated dims).
    coords associated with multiple dims will appear in multiple places in the result.

    include_dims_as_coords: bool
        whether to include dims as coord names in the result.
        Dims with no same-named coord will appear in appropriate place in result.
    '''
    result = dict()
    unused_dims = set(array.dims)
    for cname, coord in array.coords.items():
        unused_dims -= set([cname])
        if len(coord.dims) == 0:
            result.setdefault((), []).append(cname)
        for dim in coord.dims:
            result.setdefault(dim, []).append(cname)
    if include_dims_as_coords and unused_dims:
        for dim in unused_dims:
            result.setdefault(dim, []).append(dim)
    return result

@pcAccessor.register('fill_coords')
def xarray_fill_coords(array):
    '''return copy of array with coords filled for all dims.
    E.g. array with dim_1 length 50 but no coords
        --> result is just like array but has dim_1 coords = np.arange(50)
    '''
    for dim in array.dims:
        if dim not in array.coords:
            array = array.assign_coords({dim: array[dim]})
    return array

@pcAccessor.register('scale_coords')
def xarray_scale_coords(array, scale=None, *, missing_ok=True, **scale_as_kw):
    '''return copy of array with coords multiplied by scale.
    scale: None, number, or dict of {coord: scale}
        dict --> multiply each coord by the corresponding number.
        None --> provide as kwargs (scale_as_kw) instead.
    scale_as_kw: if scale is None, can provide scale dict as kwargs instead.
    missing_ok: bool
        whether it is okay if some coords are missing (if yes, skip missing coords).
    '''
    if scale is None and len(scale_as_kw) == 0:
        raise InputMissingError('must provide either "scale" or "scale_as_kw".')
    if scale is not None and len(scale_as_kw) > 0:
        raise InputConflictError('cannot provide both "scale" and "scale_as_kw".')
    if scale is None:
        scale = scale_as_kw
    assign_coords = {}
    for cname, cscale in scale.items():
        try:
            cvals = array.coords[cname]
        except KeyError:
            if not missing_ok:
                raise DimensionKeyError(f'coord={cname!r} not found in array.coords.') from None
            continue
        assign_coords[cname] = cvals * cscale
    return array.assign_coords(assign_coords)

@pcAccessor.register('shift_coords')
def xarray_shift_coords(array, shift=None, *, missing_ok=True, **shift_as_kw):
    '''return copy of array with coords shifted by shift.
    shift: None, number, or dict of {coord: shift}
        dict --> shift each coord by the corresponding number.
        None --> provide as kwargs (shift_as_kw) instead.
    shift_as_kw: if shift is None, can provide shift dict as kwargs instead.
    missing_ok: bool
        whether it is okay if some coords are missing (if yes, skip missing coords).
    '''
    if shift is None and len(shift_as_kw) == 0:
        raise InputMissingError('must provide either "shift" or "shift_as_kw".')
    if shift is not None and len(shift_as_kw) > 0:
        raise InputConflictError('cannot provide both "shift" and "shift_as_kw".')
    if shift is None:
        shift = shift_as_kw
    assign_coords = {}
    for cname, cshift in shift.items():
        try:
            cvals = array.coords[cname]
        except KeyError:
            if not missing_ok:
                raise DimensionKeyError(f'coord={cname!r} not found in array.coords.') from None
            continue
        assign_coords[cname] = cvals + cshift
    return array.assign_coords(assign_coords)

@pcArrayAccessor.register('is_sorted')
def xarray_is_sorted(array, *, increasing=True):
    '''returns whether array is sorted; array must be 1D.

    increasing: bool
        True --> check for increasing order. vals[i] <= vals[i+1]
        False --> check for decreasing order. vals[i] >= vals [i+1]
    '''
    if array.ndim != 1:
        raise DimensionalityError('is_sorted expects 1D array.')
    vals = array.data
    if increasing:
        return np.all(vals[:-1] <= vals[1:])
    else:
        return np.all(vals[:-1] >= vals[1:])

@pcAccessor.register('where_finite')
def xarray_where_finite(array):
    '''returns array, masked with NaNs anywhere that the values are not finite.'''
    return array.where(np.isfinite(array))

@pcAccessor.register('get_dx_along')
def xarray_get_dx_along(array, coord, *, atol=0, rtol=1e-5, float_rounding=False):
    '''returns number equal to the diff along array.coords[coord], after checking that it is constant.
    result will be a single number, equal to array.coords[coord].diff(coord)[0].item().

    (Technically, also promotes coord to dim during calculations if coord was a non-dimension coordinate.)
    
    before returning result, ensure that np.allclose(array.diff(dim), atol=atol, rtol=rtol);
        if that fails, raise DimensionValueError.

    float_rounding: bool
        if True, re-create floating point result if it seems to be wrong by only a small amount,
        e.g. 0.20000000001 --> float(0.2); 0.39999999999 --> float(0.4); 0.123456781234 --> unchanged
        This sometimes improves "exact" float comparisons, if float was input from a string.
        See tools.float_rounding for more details.
    '''
    carr = array.coords[coord]
    carr = xarray_promote_dim(carr, coord)
    diff = carr.diff(coord)
    if len(diff) == 0:
        raise DimensionValueError(f'expected non-empty diff({coord!r})')
    result = diff[0].item()
    if not np.allclose(diff, result, atol=atol, rtol=rtol):
        errmsg = f'expected evenly-spaced coordinates along coord {coord!r}, but got diff={diff}'
        raise DimensionValueError(errmsg)
    if float_rounding:
        result = math_float_rounding(result)
    return result

_isel_doc = xr.DataArray.isel.__doc__
if 'Examples\n' in _isel_doc:  # gives docstring with Examples removed
    _isel_doc = _isel_doc[:_isel_doc.index('Examples\n')].rstrip()
if 'Returns\n' in _isel_doc:  # gives docstring with Returns removed
    _isel_doc = _isel_doc[:_isel_doc.index('Returns\n')].rstrip()

@pcAccessor.register('isel')
@format_docstring(isel_doc=_isel_doc, fractional_indexing_doc=interprets_fractional_indexing.__doc__, sub_ntab=1)
def xarray_isel(array, indexers=None, *, promote_dims_if_needed=True,
                drop=False, missing_dims='raise', rounding='round', **indexers_as_kwargs):
    '''array.isel(...) which can also interpret fractional indexes between -1 and 1, and promotes non-dim coords.

    behaves just like xarray.DataArray.isel, but:
        - indexers also allow fractional indexes.
        - if any dim with index provided refers to a non-dimension coordinate, first promote it via swap_dims.
    In particular, for {{cname: index}}:
        - fractional indexes:
            if index is a slice, int, or iterable of ints, use it as is.
            if index contains any values between -1 and 1 (excluding -1, 0, and 1):
                treat that value as a fraction of L=len(array[cname]).
                E.g. 0.25 --> int(L * 0.25);
                    -0.1  --> -int(L * 0.1).
                This is equivalent to interprets_fractional_indexing(index, L)
        - non-dimension coordinates:
            if cname is a non-dimension coordinate, use xarray_promote_dim(array, cname).

    promote_dims_if_needed: bool
        whether to promote non-dimension coords to dimensions.
        if False, raise DimensionKeyError if any relevant coord is not already a dimension.
    drop, missing_dims: passed to array.isel; see below for details.
    rounding: passed to interprets_fractional_indexing; see below for details.

    xarray.DataArray.isel docs copied below:
    ----------------------------------------
        {isel_doc}

    interprets_fractional_indexing docs copied below:
    -------------------------------------------------
        {fractional_indexing_doc}
    '''
    if indexers is None:
        indexers = indexers_as_kwargs
    else:
        indexers = {**indexers, **indexers_as_kwargs}
    indexers_input = indexers
    array_input = array  # <-- helps with debugging in case of crash.
    # interpret fractional indexes, and promote coords to dims as necessary.
    indexers = dict()  # <-- not overwriting the originally-input value, this is a new dict.

    kw_ensure_dims = dict(promote_dims_if_needed=promote_dims_if_needed, missing_dims=missing_dims,
                          assert_1d=True,  # because here doesn't implement any way to index 2D+ dims.
                          return_existing_dims=True,  # so we can avoid indexing any missing dims!
                          )
    array, existing_dims = xarray_ensure_dims(array, list(indexers_input.keys()), **kw_ensure_dims)
    for cname in existing_dims:
        index = indexers_input[cname]
        coord = array.coords[cname]
        indexers[cname] = interprets_fractional_indexing(index, L=len(coord), rounding=rounding)
    # call isel
    return array.isel(indexers, drop=drop, missing_dims=missing_dims)

@pcAccessor.register('map')
@format_docstring(**_paramdocs_ensure_dims)
def xarray_map(array, f, *args_f, axis=None, axes=None,
                     promote_dims_if_needed=True, missing_dims='raise', **kw_f):
    '''func(array, *args_f, **kw_f), but axis/axes can be provided as strings!

    Mainly useful if trying to apply f which expects unlabeled array & int axes inputs.
    E.g. numpy.mean can use axis kwarg as iterable of ints,
        but here can provide axis as a dim name str or list of dim names.
    Probably not super useful for mean, since xarray provides xr.mean,
        but may be useful for other functions e.g. scipy.ndimage.gaussian_filter,
        which might not have an existing equivalent in xarray.

    array: xarray.DataArray or Dataset
        apply f to this array, or each array in this Dataset
    f: callable
        will be called as f(array, *args_f, **kw_f),
        possibly will also be passed a value for axis or axes, if provided here
    axis, axes: None, str, or iterable of strs
        if provided, convert to axes positions in dataarray, and pass to f as int(s).
        Also promotes these coords to dims if necessary.
    promote_dims_if_needed: {promote_dims_if_needed}
    missing_dims: {missing_dims}
    '''
    # if Dataset, just apply this to each array.
    if isinstance(array, xr.Dataset):
        ds = array
        result = ds.copy()
        for name, arr in ds.data_vars.items():
            result[name] = xarray_map(arr, f, *args_f, axis=axis, axes=axes,
                                      promote_dims_if_needed=promote_dims_if_needed,
                                      missing_dims=missing_dims, **kw_f)
        return result
    # bookkeeping on 'axis' & 'axes' inputs:
    if axis is None and axes is None:  # simplest case; will just apply f to entire array.
        coords = None
        kw_ax = dict()
    elif axis is not None:  # and axes is None
        coords = axis
        ax_key = 'axis'
    elif axes is not None:  # and axis is None
        coords = axes
        ax_key = 'axes'
    else:  # both axis and axes were provided
        raise InputConflictError('cannot provide both "axis" and "axes".')
    if coords is not None:
        if isinstance(coords, str):
            coords = [coords]
        # ensure the coords exist:
        array, existing_dims = xarray_ensure_dims(array, coords,
                                                  promote_dims_if_needed=promote_dims_if_needed,
                                                  missing_dims=missing_dims, return_existing_dims=True)
        # convert coords to ax nums:
        ax_nums = array.get_axis_num(existing_dims)
        kw_ax = {ax_key: ax_nums}
    # call f but use xarray.Dataset.map functionality to preserve coords/attrs/etc.
    array_name = array.name
    _data_var_name = next_unique_name('_internal_variable', [*array.coords, *array.dims])
    ds = array.to_dataset(name=_data_var_name)
    ds_result = ds.map(f, args=args_f, **kw_f, **kw_ax)
    result = ds_result[_data_var_name]
    result.name = array_name
    return result


''' --------------------- Stats --------------------- '''

@pcArrayAccessor.register('stats')  # ArrayAccessor because this fails for Datasets
def xarray_stats(array, dim=None, *, keep=None):
    '''returns Dataset of stats for array: min, mean, max, ....

    dim: None, str, or iterable of strs
        apply stats along these dimensions
    keep: None, str, or iterable of strs
        apply stats along all except for these dimensions.
        cannot provide keep_dim if also provided dim.

    [TODO] finite=True option which allows to ignore NaNs and infs
    '''
    if dim is not None and keep is not None:
        raise InputConflictError('cannot provide both "dim" and "keep".')
    if keep is not None:
        keep = set([keep]) if isinstance(keep, str) else set(keep)
        dim = set(array.dims) - keep
    results = dict()
    results['min'] = array.min(dim)
    results['mean'] = array.mean(dim)
    results['median'] = array.median(dim)
    results['max'] = array.max(dim)
    results['std'] = array.std(dim)
    results['rms'] = (array**2).mean(dim)**0.5
    return xr.Dataset(results)


''' --------------------- Gaussian Filter --------------------- '''

@pcAccessor.register('gaussian_filter', aliases=['blur'])
@format_docstring(**_paramdocs_ensure_dims, default_sigma=DEFAULTS.GAUSSIAN_FILTER_SIGMA)
def xarray_gaussian_filter(array, dim=None, sigma=None, *,
                           promote_dims_if_needed=True, missing_dims='raise',
                           **kw_scipy_gaussian_filter):
    '''returns array after applying scipy.ndimage.gaussian_filter to it.

    array: xarray.DataArray or Dataset
        filters this array, or each data_var in a dataset.
    dim: None or str or iterable of strs
        dimensions to filter along.
        if None, filter along all dims.
    sigma: None, number, or iterable of numbers
        standard deviation for Gaussian kernel.
        if iterable, must have same length as dim.
        if None, will use DEFAULTS.GAUSSIAN_FILTER_SIGMA (default: {default_sigma}).
    promote_dims_if_needed: {promote_dims_if_needed}
    missing_dims: {missing_dims}

    additional kwargs go to scipy.ndimage.gaussian_filter.
    '''
    if sigma is None:
        sigma = DEFAULTS.GAUSSIAN_FILTER_SIGMA
    return xarray_map(array, scipy_ndimage.gaussian_filter, sigma, axes=dim,
                      promote_dims_if_needed=promote_dims_if_needed,
                      missing_dims=missing_dims, **kw_scipy_gaussian_filter)


''' --------------------- coarsen / windowing --------------------- '''

_coarsen_doc = xr.DataArray.coarsen.__doc__
_construct_doc = DataArrayCoarsen.construct.__doc__
if 'Examples\n' in _coarsen_doc:  # gives docstring with Examples removed
    _coarsen_doc = _coarsen_doc[:_coarsen_doc.index('Examples\n')].rstrip()
if 'Examples\n' in _construct_doc:  # gives docstring with Examples removed
    _construct_doc = _construct_doc[:_construct_doc.index('Examples\n')].rstrip()

@pcAccessor.register('coarsened')
@format_docstring(coarsen_doc=_coarsen_doc, construct_doc=_construct_doc)
def xarray_coarsened(array, dim, window_len, dim_coarse='window', dim_fine=None, *,
                     assign_coarse_coords=False,
                     # kw for coarsen:
                     boundary=UNSET, side=UNSET,
                     # kw for construct:
                     stride=UNSET, fill_value=UNSET, keep_attrs=UNSET,
                     ):
    '''construct a coarsened version of array, where dim is coarsened by window_len,
    and becomes two dims: dim_coarse and dim_fine.
    Original dim coords will be associated with dim_coarse and dim_fine in the new array.

    dim: str
        dimension to coarsen.
        if a non-dimension coordinate, will attempt to promote it to a dimension (e.g. via swap_dims).
    window_len: int
        length of the window to coarsen over.
    dim_coarse: str, default 'window'
        name of coarse dimension; the i'th value here corresponds to the i'th window.
    dim_fine: None or str
        name of fine dimension; the j'th value here corresponds to the j'th element within a window.
        if None, use '_'+dim, e.g. dim='t' --> dim_fine='_t'.
    assign_coarse_coords: bool or coords
        coords to assign along the dim_coarse dimension.
        True --> use np.arange.
        False --> don't assign coords.
    boundary, side: UNSET or value
        if provided (not UNSET), pass this value to coarsen().
        boundary should be 'exact', 'trim', or 'pad'.
        side should be 'left' or 'right'.
    stride, fill_value, keep_attrs: UNSET or value
        if provided (not UNSET), pass this value to construct().
    
    docs for coarsen and construct are copied below, for convenience:

    xarray.DataArray.coarsen
    ------------------------
    {coarsen_doc}


    xr.core.rolling.DataArrayRolling.construct
    ------------------------------------------
    {construct_doc}
    '''
    # bookkeeping
    kw_coarsen = dict(boundary=boundary, side=side)
    kw_construct = dict(stride=stride, fill_value=fill_value, keep_attrs=keep_attrs)
    for kw in kw_coarsen, kw_construct:
        for key, val in tuple(kw.items()):
            if val is UNSET:
                del kw[key]
    if dim_fine is None:
        dim_fine = f'_{dim}'
    # promote non-coordinate dim if necessary, else returns array unchanged.
    arr = xarray_promote_dim(array, dim)
    # coarsen & reconstruct
    coarse = arr.coarsen({dim: window_len}, **kw_coarsen)
    result = coarse.construct({dim: (dim_coarse, dim_fine)}, **kw_construct)
    # bookkeeping
    if assign_coarse_coords is not False:
        if assign_coarse_coords is True:
            assign_coarse_coords = np.arange(len(result[dim_coarse]))
        result = result.assign_coords({dim_coarse: assign_coarse_coords})
    return result


''' --------------------- polyfit --------------------- '''

@pcAccessor.register('polyfit')
@format_docstring(xr_polyfit_docs=xr.DataArray.polyfit.__doc__)
def xarray_polyfit(array, coord, degree, *, stddev=False, full=False, cov=False, **kw_polyfit):
    '''returns array.polyfit(coord, degree, **kw_polyfit), after swapping coord to be a dimension, if needed.
    E.g. for an array with dimension 'snap' and associated non-dimension coordinate 't',
        xarray_polyfit(array, 't', 1) is equivalent to array.swap_dims(dict(snap='t')).polyfit('t', 1).

    stddev: bool
        whether to also return the standard deviations of each coefficient in the fit.
        if True, assign the variable 'polyfit_stddev' = diagonal(polyfit_covariance)**0.5,
            mapping the diagonal (across 'cov_i', 'cov_j') to the dimension 'degree'.
            if cov False when stddev True, do not keep_cov in the result.
        Not compatible with full=True.
    full: bool
        passed into polyfit; see below.
    cov: bool
        passed into polyfit; see below.
        Note: if stddev=True when cov=False, still use cov=True during array.polyfit,
            however then remove polyfit_covariance & polyfit_residuals from result.

    Docs for xr.DataArray.polyfit copied below:
    -------------------------------------------
    {xr_polyfit_docs}
    '''
    array = xarray_promote_dim(array, coord)
    if stddev and full:
        raise InputConflictError('stddev=True incompatible with full=True.')
    cov_input = cov
    if stddev:
        cov = True
    result = array.polyfit(coord, degree, full=full, cov=cov, **kw_polyfit)
    if stddev:
        result = xarray_assign_polyfit_stddev(result, keep_cov=cov_input)
    return result

@pcDatasetAccessor.register
def xarray_assign_polyfit_stddev(dataset, *, keep_cov=True):
    '''assign polyfit stddev to dataset['polyfit_stddev'], treating dataset like a result of polyfit.
    These provide some measure of "goodness of fit"; smaller stddev means better fit.

    Specifically, stddev[k] = (covariance matrix)[k,k]**0.5 for k in range(len(dataset['degree']));
        one might quote +-stddev[k] as the error bar for the coefficient at degree=dataset['degree'][k].

    dataset: xarray.Dataset
        dataset to use for calculating polyfit_stderr and in which to assign the result.
        must contain variable 'polyfit_covariance' and dimension 'degree'.
    keep_cov: bool
        whether to keep the 'polyfit_covariance' and 'polyfit_residuals' vars in the result.

    The original dataset will not be altered; a new dataset will be returned.
    '''
    cov = dataset['polyfit_covariance']
    degree = dataset['degree']
    ndeg = len(degree)
    stddev = [cov.isel(cov_i=k, cov_j=k)**0.5 for k in range(ndeg)]
    stddev = xr.concat(stddev, 'degree').assign_coords({'degree': degree})
    result = dataset.assign(polyfit_stddev=stddev)
    if not keep_cov:
        result = result.drop_vars(['polyfit_covariance', 'polyfit_residuals'])
    return result

@pcAccessor.register('coarsened_polyfit')
@format_docstring(xr_polyfit_docs=xr.DataArray.polyfit.__doc__)
def xarray_coarsened_polyfit(array, coord, degree, window_len, *,
                             dim_coarse='window', keep_coord='middle',
                             assign_coarse_coords=True,
                             boundary=UNSET, side=UNSET,
                             stride=UNSET, fill_value=UNSET, keep_attrs=UNSET,
                             **kw_polyfit
                             ):
    '''returns result of coarsening array, then polyfitting along the fine dimension, in each window.
    E.g., make windows of length 10 along 't', then polyfit each window along 't',
    then concat the results from each window, along dim_coarse (default: 'window').

    coord: str
        coordinate to polyfit along.
    degree: int
        degree of polynomial to fit.
    window_len: int or None
        length of window to coarsen over.
        None --> polyfit without coarsening; equivalent to window_len = len(array.coords[coord])
    dim_coarse: str, default 'window'
        name of coarse dimension; the i'th value here corresponds to the i'th window.
    keep_coord: False or str in ('left', 'right', 'middle')
        along the dim_coarse dimension, also provide some of the original coord values.
        'left' --> provide the left-most value in each window.
        'middle' --> provide the middle value in each window.
        'right' --> provide the right-most value in each window.
        False --> don't provide any of the original coord values.
        if not False, result will swap dims such that coord is a dimension instead of dim_coarse.
    assign_coarse_coords: bool or coords
        coords to assign along the dim_coarse dimension.
        True --> use np.arange.
        False --> don't assign coords.
    boundary, side: UNSET or value
        if provided (not UNSET), pass this value to coarsen().
    stride, fill_value, keep_attrs: UNSET or value
        if provided (not UNSET), pass this value to construct().

    additional **kw are passed to polyfit.

    Docs for xr.DataArray.polyfit copied below:
    -------------------------------------------
    {xr_polyfit_docs}
    '''
    # bookkeeping
    if keep_coord not in ('left', 'middle', 'right', False):
        raise InputError(f'invalid keep_coord={keep_coord!r}; expected "left", "middle", "right", or False.')
    # if window_len is None or <1, don't coarsen at all.
    if window_len is None:
        return xarray_polyfit(array, coord, degree, **kw_polyfit)
    # coarsen
    coarsened = xarray_coarsened(array, coord, window_len,
                                dim_coarse=dim_coarse,
                                assign_coarse_coords=assign_coarse_coords,
                                boundary=boundary, side=side,
                                stride=stride, fill_value=fill_value, keep_attrs=keep_attrs)
    # bookkeeping
    n_windows = len(coarsened[dim_coarse])
    if n_windows < 1:
        errmsg = f'coarsened array has n_windows={n_windows} < 1; cannot polyfit.'
        raise DimensionValueError(errmsg)
    # polyfitting
    promoted = []
    for i_window in range(n_windows):
        prom = xarray_promote_dim(coarsened.isel({dim_coarse: i_window}), coord)
        promoted.append(prom)
    polyfits = []
    for arr in promoted:
        pfit = xarray_polyfit(arr, coord, degree, **kw_polyfit)
        polyfits.append(pfit)
    if keep_coord:
        results = []
        for i_window, (arr, prom) in enumerate(zip(polyfits, promoted)):  # i_window just for debugging
            i_keep = {'left': 0, 'middle': 0.5, 'right': -1}[keep_coord]
            # isel from coords[coord] instead of prom, to ensure associated coords are included too,
            #   e.g. t & snap are associated --> this will keep t & snap in the result.
            # if i_keep = 0.5, it is handled by xarray_isel fractional indexing.
            keep = xarray_isel(prom.coords[coord], {coord: i_keep})
            here = arr.assign_coords({coord: keep})
            results.append(here)
    else:
        results = polyfits
    result = xr.concat(results, dim_coarse)
    if keep_coord:
        result = xarray_promote_dim(result, coord)
    return result

