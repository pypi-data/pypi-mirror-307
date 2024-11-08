"""
File Purpose: xarray attribute accessors.
accessing stuff via xr.DataArray.pc.{attr}, e.g. xr.DataArray.pc.differentiate(...)
"""
import functools
import warnings

import xarray as xr

from .properties import alias
from .pytools import format_docstring, help_str
from ..defaults import DEFAULTS

''' --------------------- As accessors, on xarrays --------------------- '''
# access via xr.DataArray.pc.{attr}, e.g. xr.DataArray.pc.differentiate(...)

def xarray_register_dataarray_accessor_cls(name, *, warn_if_clsname_match=False):
    '''return class decorator which registers cls as an accessor for xarray.DataArray,
    as per xr.register_dataarray_accessor(name).

    warn_if_clsname_match: bool, default False
        whether to suppress AccessorRegistrationWarning,
            when xr.DataArray.name already exists AND cls.__name__ == xr.DataArray.name.

        This solves the issue that when doing pc=pc.reload(pc),
            (or otherwise using importlib.reload to reload the code attaching the accessor,)
            the code to attach the accessor would be run again, causing a warning.
            But that warning is confusing;
            it's almost certainly just overwriting the name defined by that code originally.
            Using warn_if_clsname_match=False will suppress the warning in that case.
    '''
    def decorated_register_dataaray_accessor(cls):
        with warnings.catch_warnings():  # <-- restore original warnings filter after this.
            if not warn_if_clsname_match:
                try:
                    xr_accessor = getattr(xr.DataArray, name)
                except AttributeError:
                    pass  # that's fine, we'll register cls as an accessor.
                else:
                    if xr_accessor.__name__ == cls.__name__:
                        # suppressing AccessorRegistrationWarning (from xr.register_dataarray_accessor(name))
                        warnings.filterwarnings('ignore', category=xr.core.extensions.AccessorRegistrationWarning)
            return xr.register_dataarray_accessor(name)(cls)
    return decorated_register_dataaray_accessor

# similar to above, but for dataset:
def xarray_register_dataset_accessor_cls(name, *, warn_if_clsname_match=False):
    '''return class decorator which registers cls as an accessor for xarray.Dataset,
    as per xr.register_dataset_accessor(name).

    warn_if_clsname_match: bool, default False
        whether to suppress AccessorRegistrationWarning,
            when xr.Dataset.name already exists AND cls.__name__ == xr.Dataset.name.
    '''
    def decorated_register_dataset_accessor(cls):
        with warnings.catch_warnings():  # <-- restore original warnings filter after this.
            if not warn_if_clsname_match:
                try:
                    xr_accessor = getattr(xr.Dataset, name)
                except AttributeError:
                    pass  # that's fine, we'll register cls as an accessor.
                else:
                    if xr_accessor.__name__ == cls.__name__:
                        # suppressing AccessorRegistrationWarning (from xr.register_dataset_accessor(name))
                        warnings.filterwarnings('ignore', category=xr.core.extensions.AccessorRegistrationWarning)
            return xr.register_dataset_accessor(name)(cls)
    return decorated_register_dataset_accessor


class _BoundObjCaller():
    '''remembers f & instance. calls f(instance.obj, *args, **kw).
    
    Helper class for pcAccessor so that the methods can be compatible with multiprocessing.
    '''
    def __init__(self, f, instance):
        self.f = f
        self.instance = instance
        self.__doc__ = f'caller of {help_str(f, blankline=True)}'
        #functools.update_wrapper(self, f)

    def __call__(self, *args, **kw):   # maybe self, instance, *args, **kw ?
        '''returns self.f(self.instance.obj, *args, **kw).'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        return self.f(self.instance.obj, *args, **kw)

    def __repr__(self):
        obj = self.instance.obj
        obj_info = f'{type(obj).__name__} at {hex(id(obj))}'
        f_info = f'{type(self.f).__name__} {self.f.__name__}'
        return f'<{type(self).__name__} of {f_info} for {obj_info}>'


class _ObjCaller():
    '''behaves like a bound method but calls f(self.obj, ...) instead of f(self, ...)'''
    def __init__(self, f):
        self.f = f
        self.__doc__ = f'caller of {help_str(f, blankline=True)}'

    def __get__(self, instance, owner):
        if instance is None:  # called on class, not instance
            return self
        else:
            return _BoundObjCaller(self.f, instance)

    def __repr__(self):
        f_info = f'{type(self.f).__name__} {self.f.__name__}'
        return f'<{type(self).__name__} of {f_info}>'


class pcAccessor():
    '''access attributes of DataArrays or Datasets e.g. xr.DataArray.pc.differentiate(...).

    This is the base class inherited by pcArrayAccessor and pcDatasetAccessor.
    When deciding where to attach a method, think:
        pcAccessor if it applies to DataArrays and Datasets the same way,
        pcArrayAccessor if it applies to DataArrays only,
        pcDatasetAccessor if it applies to Datasets only.
    '''
    # internal pc code should prefer to import the relevant methods from tools.xarrays,
    #   for improved compatibility with non-xarray objects.
    # however, scripts should prefer to use the method attached to the array, since it's easier.
    
    def __init__(self, xarray_obj):
        self.obj = xarray_obj

    # obj = weakref_property_simple('_obj', doc='''the xarray this object is attached to.''')
    # weakref actually not desireable.. if using it:
    #   e.g. xr.DataArray(0).pc.obj would be None; the array isn't stored so the weakref dies.
    #   meanwhile, arr=xr.DataArray(0); arr.pc.obj would be arr; the weakref didn't die.
    # [TODO][EFF] do xarray data accessors prevent original array from being garbage-collected?

    registry = {}  # {name: (cls, f)} for all registered methods.

    @classmethod
    def register(cls, f_or_name, *, aliases=[], _name=None):
        '''attaches method which applies f(self.obj, *args, **kw) to xr.DataArray.pc.{name}, then returns f.

        This ensures f can be accessed via xr.DataArray.pc.{name} or xr.Dataset.pc.{name}.
            pcAccessor.register --> available on both DataArrays and Datasets.
            pcArrayAccessor.register --> available on DataArrays only.
            pcDatasetAccessor.register --> available on Datasets only.

        f_or_name: str or callable
            str --> returns a function: f -> register(f, name=f_or_name)
            callable --> register this function then return it.
                        will be registered at _name if provided, else at f.__name__.
            This enables this method to be used directly as a decorator, or as a decorator factory.
            Examples:
                @pcAccessor.register
                def my_method(xarray_object, arg1):
                    print(arg1)
                    print(xarray_obj)
                # --> can later do:
                xr.DataArray(data).pc.my_method(7)   # prints 7 then prints DataArray(data).
                
                @pcDatasetAccessor.register(name='size')
                def xarray_dataset_get_size(ds):
                    # computes number of elements in dataset
                    return sum(arr.size for arr in ds.values())
                # --> can later do:
                xr.Dataset(...).pc.get_size()
        _name: str, optional
            name to register f at. If not provided, use f.__name__.
            Not intended to be provided directly.
        aliases: list of str
            aliases for f. Create alias property for each of these.
        '''
        if isinstance(f_or_name, str):
            name = f_or_name
            return lambda f: cls.register(f, _name=name, aliases=aliases)
        else:
            f = f_or_name
            name = _name or f.__name__
            caller = _ObjCaller(f)
            setattr(cls, name, caller)
            # bookkeeping:
            cls.registry[name] = (cls, f)
            # handle aliases if provided:
            for alias_ in aliases:
                setattr(cls, alias_, alias(name))
            return f

    # # # FUN STUFF FOR CONVENIENCE HERE # # #
    nMbytes = property(lambda self: self.obj.nbytes/1024**2, doc='''size of array in Mbytes''')


@xarray_register_dataarray_accessor_cls('pc')
class pcArrayAccessor(pcAccessor):
    '''access attributes of DataArrays e.g. xr.DataArray.pc.differentiate(...).
    for more help see help(xr.DataArray.pc).
    '''
    # # # FUN STUFF FOR CONVENIENCE HERE # # #
    size = property(lambda self: self.obj.size,
        doc='''total number of elements in the DataArray. Equivalent to array.size.
        Provided for consistent interface for DataArray or Dataset size: use obj.pc.size.''')


@xarray_register_dataset_accessor_cls('pc')
class pcDatasetAccessor(pcAccessor):
    '''access attributes of Datasets e.g. xr.Dataset.pc.differentiate(...).
    for more help see help(xr.Dataset.pc).
    '''
    # # # FUN STUFF FOR CONVENIENCE HERE # # #
    size = property(lambda self: sum(v.size for v in self.obj.values()),
            doc='''total number of elements across all values in the Dataset''')
