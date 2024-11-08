"""
File Purpose: Behavior object
- like a dict, but with extra features.
- for describing the current behavior of a PlasmaCalculator
"""

import itertools
import sys

import xarray as xr

from ..errors import UnitsError
from ..tools import (
    simple_property,
    UNSET,
    repr_simple,
    format_docstring,
    xarray_assign, is_iterable_dim,
)
from ..defaults import DEFAULTS


class Behavior(dict):
    '''dict with 'compatible' method.

    __getitem__ altered to include values from self.dims, and 'dims' itself.
        e.g. self['dims'] == self.dims; self['fluid'] --> self.dims['fluid'], if possible.
    __contains__ altered to include values from self.dims.
        e.g. 'fluid' in self --> fluid in self.keys() or fluid in self.dims
    '''
    # # # CREATION / INITIALIZATION # # #
    def __init__(self, arg0=UNSET, dims=None, **kw):
        '''initialize Behavior.
        arg0: object
            first argument to pass to dict() constructor.
        dims: None or dict
            dict of dimension values for this behavior.
            if None, use empty dict.
        remaining **kw are passd to dict() constructor
        '''
        if arg0 is UNSET:
            super().__init__(**kw)
        else:
            super().__init__(arg0, **kw)
        self.dims = dict() if dims is None else dims

    def _new_with_dims(self, dims):
        '''return new Behavior like self but with dims instead of self.dims.'''
        return type(self)(super().copy(), dims=dims)

    # # # DICT-LIKE FOR 'dims' # # #
    def __getitem__(self, key):
        '''return self[key], or self.dims[key] if key is in self.dims.
        if key is 'dims', return self.dims.
        '''
        if key == 'dims':
            return self.dims
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.dims[key]

    def __contains__(self, key):
        '''return whether key is in self or self.dims.'''
        return super().__contains__(key) or key in self.dims

    def copy(self):
        '''return a copy of self, including a copy of self.dims'''
        copy_dims = self.dims.copy()
        copy_dict = super().copy()
        return type(self)(copy_dict, dims=copy_dims)

    # # # COMPARISON # # #
    def compatible(self, other, *, lenient=False, subdims=False):
        '''return whether self and other are compatible.
        'compatible' when self[key] == other[key] for all keys in self (and self.dims).
        only tests keys in self; other can have more keys than those in self.

        lenient: bool
            whether to only test keys which are in both self and other.
            if False, and other is missing any keys in self, return False.
        subdims: bool
            whether to be compatible if dim from self is a value within dim from other.
            when True, if only compatible due to subdims, return list of dims which are subdims.
            E.g., self = dict(fluid=1, snap=0), other = dict(fluid=[0,1,2,3], snap=0) -->
                subdims=True --> compatible; result will be ['fluid']
                subdims=False --> not compatible.
            To check whether other dim is a "list" of values, use is_iterable_dim(other_val)
        '''
        if not lenient:
            if not all(key in other for key in (*self, *self.dims)):
                return False  # other is missing key; cannot be compatible.
        # non-dims compatibility
        for key, val in self.items():
            try:
                other_val = other[key]
            except KeyError:  # skip this key, if lenient.
                assert lenient, f"coding error... other is missing {key!r}; should've already returned False"
            else:
                if val != other_val:
                    return False
        # dims compatibility
        subdims_result = []
        for key, val in self.dims.items():
            try:
                other_val = other[key]
            except KeyError:  # skip this key, if lenient.
                assert lenient, f"coding error... other is missing {key!r}; should've already returned False"
            else:
                if val != other_val:
                    if subdims and is_iterable_dim(other_val) and (val in other_val):
                        subdims_result.append(key)
                    else:
                        return False
        return True if len(subdims_result)==0 else subdims_result

    # # # CONVENIENCE # # #
    @format_docstring(DEFAULTS=DEFAULTS)
    def label_array(self, array, *, skip=UNSET):
        '''label array with coords from self.dims, attrs from self.items().
        Requires that values of self.dims are all non-iterable, according to is_iterable_dim().

        skip: None, UNSET, or list of strs
            skip these attrs, if provided.
            UNSET --> skip DEFAULTS.SKIP_BEHAVIOR_ARRAY_LABELS
                        (default {DEFAULTS.SKIP_BEHAVIOR_ARRAY_LABELS})
            None --> don't skip anything.
        '''
        coords = self.dims
        if skip is UNSET:
            skip = DEFAULTS.SKIP_BEHAVIOR_ARRAY_LABELS
        elif skip is None:
            skip = []
        attrs = {k: v for k, v in self.items() if k not in skip}
        return xarray_assign(array, coords=coords, attrs=attrs)

    # # # DISPLAY # # #
    def __repr__(self):
        contents = [f'{k}={repr_simple(v)}' for k, v in self.items()]
        contents.append(f'dims={repr_simple(self.dims)}')
        return f'{type(self).__name__}({", ".join(contents)})'

    def __str__(self):
        contents = [f'{k}={v!r}' for k, v in self.items()]
        contents.append(f'dims={self.dims}')
        return f"{type(self).__name__}({', '.join(contents)})"


class BehaviorQuantity():
    '''quantity, with value and associated behavior.
    behavior: dict or Behavior
        this BehaviorQuantity is relevant only when behavior.compatible(obj.behavior).
        E.g., behavior = dict(snap=0, units='si'),
            - relevant if obj.behavior = dict(snap=0, units='si', ...).
            - irrelevant if obj.behavior = dict(snap=1, ...).
            - irrelevant if obj.behavior = dict(units='raw', ...)
        note: if ukey is not None, and behavior is a Behavior,
            self will store a COPY of behavior, not the original object;
            this is to prevent popping 'units' from the original Behavior object.

    MB: None or number
        number of megabytes this BehaviorQuantity takes up in memory.
        if None, will be calculated from self.value, if possible.
    ukey: None, or str
        if provided (not None), pop 'units' from stored behavior, and store self.uinfo = (ukey, units).
        None --> don't pop 'units' from stored behavior.
        str --> value [any unit system] = self.value * u_convert, where
                    u_convert = UnitsHaver.u(self.uinfo[0], (that unit system), convert_from=self.uinfo[0])
                Note, for a dimensionless value, use ukey='' or ukey='1'.
        The benefit of using this is that 'units' won't be in self.behavior,
            so self.compatible(other_behavior) won't need to check units.
        (The downside is that you must be careful to properly handle the units. see also: self.get_value.)

    Every BehaviorQuantity has a unique identifier, self.id, which is a number.
    BehaviorQuantity.NEXT_UNIQUE_ID is the next number to be assigned.
    '''
    NEXT_UNIQUE_ID = 0

    # # # CREATION / INITIALIZATION # # #
    def __init__(self, value, behavior, *, MB=None, ukey=None, **kw__behavior):
        self.value = value
        if not isinstance(behavior, Behavior):
            behavior = Behavior(behavior, **kw__behavior)
        if ukey is not None:
            behavior = behavior.copy()
            self.uinfo = (ukey, behavior.pop('units', None))
        self.behavior = behavior
        self._entered_MB = MB
        self.n_used = 0  # counts number of times this value was loaded from cache.
                         # not updated by this class, but see e.g. VarCache.
        self.id = self.NEXT_UNIQUE_ID
        type(self).NEXT_UNIQUE_ID = self.id + 1  # [TODO] is this thread-safe?

    def _new_with_dims(self, dims, **kw_init):
        '''return new BehaviorQuantity like self but with dims instead of self.behavior.dims.'''
        kw_init.setdefault('MB', self.MB)
        return type(self)(self.value, self.behavior._new_with_dims(dims), **kw_init)

    # # # PROPERTIES # # #
    uinfo = simple_property('_uinfo', default=None,
            doc='''(ukey, units), indicating units of self.value;
            self.value [any unit system] = self.value * u_convert, where
                u_convert = UnitsHaver.u(ukey, (that unit system), convert_from=ukey)''')

    # # # GETTING VALUE # # #
    def get_value(self, units_manager=None):
        '''return self.value; if units_manager is provided return value in units_manager.units unit system.
        if self.uinfo[1] != units_manager.units, and value is an xarray with 'units' attr,
            result will have units attr assigned to units_manager.units.

        raise UnitsError if ALL of the following are True:
            - units_manager was provided
            - self.uinfo is None
            - units_manager.units!=self.behavior['units']
        '''
        u = units_manager
        if u is None:
            return self.value
        if self.uinfo is None:
            if self.behavior.get('units', None) != u.units:
                errmsg = (f"can't get value in units={u.units!r}, since self.uinfo is None, "
                          f"and self.behavior['units'] != {u.units!r}.")
                raise UnitsError(errmsg)
            else:
                return self.value
        else:
            value = self.value
            ukey, value_units = self.uinfo
            if value_units == u.units:
                result = value
            else:
                u_convert = u(ukey, convert_from=value_units)
                result = self.value * u_convert
                if isinstance(result, xr.DataArray) and result.attrs.get('units', None) != u.units:
                    result = result.assign_attrs(units=u.units)
            return result
        assert False, 'coding error if reached this line'

    # # # MATCHING OTHER BEHAVIORS # # #
    def compatible(self, behavior, *, lenient=False, subdims=False):
        '''tells whether this cached quantity is compatible to obj with this behavior.
        returns self.behavior.compatible(behavior, lenient=lenient, subdims=subdims)
        '''
        return self.behavior.compatible(behavior, lenient=lenient, subdims=subdims)

    def matches_behavior(self, behavior):
        '''tells whether this cached quantity matches this behavior.
        returns self.compatible(behavior, lenient=True, subdims=False).
        '''
        return self.compatible(behavior, lenient=True, subdims=False)

    def relevant(self, behavior):
        '''tells whether this cached quantity is relevant to this behavior.

        'relevant' when self[key] == other[key] for all keys in self,
            and self.dims[d] equals or is inside other.dims[d], for all d in self.dims.
        only tests keys in self; other can have more keys than those in self.

        returns self.compatible(behavior, lenient=True, subdims=True).
        '''
        return self.compatible(behavior, lenient=True, subdims=True)

    # # # LISTING POINTS # # #
    def list_points(self):
        '''returns a list of CachedQuantity objects, each with a single point (in dimension space) from self.
        dimension space includes dimensions but not maindims, e.g. fluid, snap, but not x,y,z.
        '''
        behavior = self.behavior
        keys, vals = zip(*behavior.dims.items())
        iterable = [is_iterable_dim(v, min_length=1) for v in vals]
        if not any(iterable):
            return [self]
        iters = [iter(v) if it_ else [v] for v, it_ in zip(vals, iterable)]
        # [TODO] <-- re-use the iter_dim_multi code from dimension_tools?
        result = []
        for vs_ in itertools.product(*iters):
            dims_point = dict(zip(keys, vs_))
            result.append(self._new_with_dims(dims_point))
            # [TODO] ^ that just copy-pastes the value from self, to each of the points.
            #    if the value is an xarray with dimension names as coords,
            #    then we should instead iterate over those coords too.
            #    e.g. if value has fluid=[0,1,2] and self.behavior.dims has fluid=[0,1,2],
            #      then the result should have 3 points, first with fluid 0, then fluid 1, then 2.
            #      right now, the result would be 3 points, each with fluid=[0,1,2].
        return result

    # # # MB # # #
    @property
    def MB(self):
        '''number of megabytes this cached quantity takes up in memory.
        if self._entered_MB is None, will be calculated from self.value.
        if self.value.nbytes is not available, will be 0.
        Saves value to self._MB to avoid recalculating.
        '''
        try:
            return self._MB
        except AttributeError:
            pass  # this is the first time getting MB; handle it below.
        if self._entered_MB is None:
            try:
                nbytes = self.value.nbytes
            except AttributeError:
                nbytes = sys.getsizeof(self.value)
            self._MB = nbytes / 1024**2
        else:
            self._MB = self._entered_MB
        return self._MB

    # # # DISPLAY # # #
    def __repr__(self):
        contents = self._repr_contents()
        return f'{type(self).__name__}({", ".join(contents)})'

    def _repr_contents(self):
        '''return list of contents to put in repr of self.'''
        val_str = repr(self.value)
        if len(val_str) > 20:
            val_str = val_str[:20] + '...'
        contents = [val_str, str(self.behavior)]
        if self.MB is not None:
            contents.append(f'MB={self.MB:.2e}')
        if self.uinfo is not None:
            contents.append(f'uinfo={self.uinfo}')
        return contents


class BehaviorHaver():
    '''object which has a behavior.'''
    behavior = property(lambda self: self.get_behavior(),
            doc='''dict of {attr: self.attr} for attr in self.behavior_attrs. Note dims are separate;
            dims go in behavior.dims. E.g. Behavior({'units':'si',...}, dims={'snap':0,...}).''')

    def get_behavior(self, keys=None):
        '''return value of self.behavior.
        keys: None or iterable
            if provided, only include these attrs.
            from nondim_behavior_attrs, or dims.
        '''
        attrs = self.nondim_behavior_attrs
        dims = getattr(self, 'dims', [])
        if keys is None:
            use_attrs = attrs
            use_dims = dims
        else:
            use_attrs = [key for key in keys if key in attrs]
            use_dims = [key for key in keys if key in dims]
        behavior_dict = {k: getattr(self, k) for k in use_attrs}
        self_dim_values = getattr(self, 'dim_values', None)
        dims_dict = None if self_dim_values is None else self_dim_values(use_dims)
        return Behavior(behavior_dict, dims_dict)

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        Here, returns an empty list. Subclasses should override.
        '''
        return []

    _dims_in_behavior_attrs = simple_property('_dims_in_behavior_attrs_', default=True,
            doc='''whether to include self.dimensions.keys() in self.behavior_attrs. default True.''')

    @property
    def nondim_behavior_attrs(self):
        '''list of attrs in self which control behavior of self, but which are NOT in self.dimensions.'''
        # 
        with self.using(_dims_in_behavior_attrs=False):
            return self.behavior_attrs
