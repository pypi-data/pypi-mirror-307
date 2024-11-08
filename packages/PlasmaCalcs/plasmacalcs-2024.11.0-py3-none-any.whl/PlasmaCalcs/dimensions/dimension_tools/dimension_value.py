"""
File Purpose: DimensionValue, DimensionValueList, UniqueDimensionValue
"""

from ...errors import DimensionValueError, DimensionKeyError
from ...tools import (
    elementwise_property, alias,
    repr_simple,
    Sentinel, UNSET, ATTR_UNSET,
    is_iterable,
    is_integer, interprets_fractional_indexing,
)
from ...defaults import DEFAULTS


''' --------------------- DimensionValue --------------------- '''

class DimensionValue():
    '''value of a dimension. E.g., a single Fluid or a single Snap.
    Also may know how to be converted to str and int.

    s: string or None
        str(self) --> s. if None, cannot convert to str.
    i: nonnegative int, or None
        int(self) --> i. if None, cannot convert to int.
        Must be nonnegative; negative ints are reserved for "index from end of list".

    CAUTION: intended to be immutable (but not strictly enforced)!
        changing the values of s or i after initialization might cause unexpected behavior.
        E.g., DimensionValueList.get utilizes caching and expects s & i to not change.

    testing equality shows that DimensionValue == s or i,
        e.g. val1=DimensionValue('H', 0) --> val1 == 'H' and val1 == 0.
        However when comparing to another DimensionValue, s and i must both be equal,
            e.g. val2=DimensionValue('C', 0) --> val2 != val1.
            (result also depends on DimensionValue types, if subclasses are involved.)
    '''
    # attrs "defining" this DimensionValue, & which can be provided as kwargs in __init__
    _kw_def = {'s', 'i'}

    def __init__(self, s=None, i=None):
        self.s = s
        self.i = i
        if (i is not None) and (i < 0):
            raise DimensionValueError(f"negative i not allowed, but got i={i}.")
    def __str__(self):
        return f'{type(self).__name__}_{self.i}' if self.s is None else self.s
    def __int__(self):
        return self.i

    def __eq__(self, v):
        '''return self==v. Equal if:
            - v is an instance of type(self), and
                all kw from both self._kw_def and v._kw_def have the same values.
                    (any kw missing attrs will be treated as UNSET.)
                For DimensionValue, just compares self.s==v.s and self.i==v.i.
                    Subclasses may add more kwargs to compare by altering _kw_def.
            - self.s == v or self.i == v, and v is not another DimensionValue
        Not equal if v is a DimensionValue but not an instance of type(self),
            e.g. class Fluid(DimensionValue):...; class Snap(DimensionValue):...;
                Fluid('H', 0) != Snap('H', 0).
        '''
        if isinstance(v, type(self)):
            kw_compare = self._kw_def.union(v._kw_def)
            for key in kw_compare:
                if getattr(self, key, UNSET) != getattr(v, key, UNSET):
                    return False
            return True
        elif isinstance(v, DimensionValue):
            if DEFAULTS.DEBUG >= 4:
                print('DimensionValue comparison of incompatible subclasses: ',
                      type(self), type(v), '--- returning False.')
            return False
        else:
            return (self.s == v) or (self.i == v)

    def equal_except_i(self, v):
        '''returns whether self == v (another DimensionValue), ignoring i.
        equal if v is an instance of type(self) and
            all kw from both self._kw_def and v._kw_def have the same values.
            (any kw missing attrs will be treated as UNSET.)
            For DimensionValue: self.s==v.s and self.i==v.i. Subclasses may add more.
        '''
        if not isinstance(v, type(self)):
            return False
        kw_compare = self._kw_def.union(v._kw_def)
        for key in kw_compare:
            if key == 'i': continue
            if getattr(self, key, UNSET) != getattr(v, key, UNSET):
                return False
        return True

    def __hash__(self):
        return hash((type(self), *(getattr(self, k, ATTR_UNSET) for k in self._kw_def)))

    def copy(self, **kw_init):
        '''return a copy of self. Can provide new kwargs here to override old values in result.
        E.g. self.copy(i=7) makes a copy of self but with i=7 instead of self.i.
        '''
        for key in self._kw_def:
            kw_init.setdefault(key, getattr(self, key))
        return type(self)(**kw_init)

    def with_i(self, i):
        '''return copy of self with i=i, or self if self.i==i already.'''
        if self.i == i:
            return self
        return self.copy(i=i)

    # # # DISPLAY # # #
    def __repr__(self):
        return f'{type(self).__name__}({self.s!r}, {self.i!r})'

    def _repr_simple(self):
        '''return simple repr for self: Classname(s, i).
        if s is None, use Classname(i) instead.
        if i is None, use Classname(s, i=None) instead.
        Called when using PlasmaCalcs.tools.repr_simple.
        '''
        if self.s is None:
            return f'{type(self).__name__}({self.i!r})'
        elif self.i is None:
            return f'{type(self).__name__}({self.s!r}, i=None)'
        else:
            return f'{type(self).__name__}({self.s!r}, {self.i!r})'

    # ndim = 0 is useful for achieving desired behavior,
    #  of being treated as "a single value of a dimension",
    #  while still allowing subclasses to implement __iter__.
    # ndim = 0 is checked by:
    #  - DimensionHaver, when checking dim_is_iterable() for an instance of this class.
    #  - xarray, when attempting to use an instance of this class as a coordinate.
    ndim = 0

    # size = 1 is also useful.
    size = 1

    # sometimes it's convenient to have an ordering for the values...
    def __lt__(self, other):
        if isinstance(other, type(self)): return (self.i, self.s) < (other.i, other.s)
        else: return NotImplemented
    def __le__(self, other):
        if isinstance(other, type(self)): return (self.i, self.s) <= (other.i, other.s)
        else: return NotImplemented
    def __gt__(self, other):
        if isinstance(other, type(self)): return (self.i, self.s) > (other.i, other.s)
        else: return NotImplemented
    def __ge__(self, other):
        if isinstance(other, type(self)): return (self.i, self.s) >= (other.i, other.s)
        else: return NotImplemented

    # # # SERIALIZING # # #
    SERIAL_TYPES = {}  # dict of {serialization name: cls} for serializable subclasses

    def __init_subclass__(cls, *, _serial_typename=None, **kw):
        '''register cls as a subclass of DimensionValue, for serialization purposes.

        _serial_typename: None or str
            name to use for this type, for serialization purposes.
            None --> use cls.__name__.

        This method will set cls._serial_typename to _serial_typename.
        '''
        super().__init_subclass__(**kw)
        DimensionValue.register_type(cls, _serial_typename=_serial_typename)

    @staticmethod
    def register_type(cls_to_register, _serial_typename=None):
        '''register cls_to_register as a serializable type of DimensionValue.
        _serial_typename: str or None
            name to use for serialization. if None, use cls_to_register.__name__.
        '''
        cls = cls_to_register
        if _serial_typename is None: _serial_typename = cls.__name__
        # ensure uniqueness:
        if _serial_typename in DimensionValue.SERIAL_TYPES:
            errmsg = (f"cannot register {cls} as {_serial_typename!r} because that name is already in use.")
            raise DimensionKeyError(errmsg)
        # register cls!
        cls._serial_typename = _serial_typename
        DimensionValue.SERIAL_TYPES[cls._serial_typename] = cls

    def to_dict(self):
        '''returns dictionary of info about self, including "s" and "i".'''
        return {"s": self.s, "i": self.i}

    @classmethod
    def from_dict(cls, d):
        '''return cls from dict d. d should NOT have 'typename' key.
        Use cls.deserialize(d) instead if d has 'typename' key.
        Example: Fluid.from_dict(fluid0.to_dict()) == fluid0, assuming fluid0 is a Fluid object.

        Subclasses will probably override this method instead of deserialize.
        '''
        return cls(**d)

    def serialize(self):
        '''return serialization of self, including 'typename' key.'''
        try:
            typename = self._serial_typename
        except AttributeError:
            errmsg = (f"{type(self).__name__}._serial_typename undefined --> cannot serialize.")
            raise DimensionKeyError(errmsg) from None
        self_dict = self.to_dict()
        return {"typename": typename, **self_dict}

    @staticmethod
    def deserialize(serial):
        '''creates a DimensionValue object from a serialized representation of a DimensionValue.

        serial: dict
            dictionary, must contain 'typename' key.

        The output here will be an instance of DimensionValue.SERIAL_TYPES[typename].
        '''
        _serial_input = serial  # for reference. Helps with debugging.
        serial = serial.copy()
        try:
            typename = serial.pop('typename')
        except KeyError:
            errmsg = (f"expected 'typename' key in input serial, but got {serial.keys()}.\n"
                      "consider using cls.from_dict, to proceed without typename.")
            raise DimensionKeyError(errmsg) from None
        cls_to_make = DimensionValue.SERIAL_TYPES[typename]
        return cls_to_make.from_dict(serial)

DimensionValue.register_type(DimensionValue)


''' --------------------- DimensionValueList --------------------- '''

class SliceableList(list):
    '''list that returns a new instance of type(self) when sliced.
    Also permits slicing by an iterable (take one element for each index in the iterable).
    '''
    def __getitem__(self, ii):
        '''return self[ii], giving element from self if int(ii) possible, else new instance of type(self).'''
        try:
            i = int(ii)
        except TypeError:
            pass  # handled after 'else' block
        else:
            return super().__getitem__(i)
        cls = type(self)
        if isinstance(ii, slice):
            return cls(super().__getitem__(ii))
        else:
            return cls([super(SliceableList, self).__getitem__(i) for i in ii])

    size = property(lambda self: len(self), '''alias to len(self).''')

    # # # DISPLAY # # #
    def _display_contents(self, f, *, nmax=3):
        '''return str to display self's contents, using f(element) for each element.
        if len(self) > nmax, instead include len(self), self[0], and self[-1], only.
        '''
        if len(self) <= nmax:
            contents = ', '.join(f(el) for el in self)
        else:
            contents = f'len={len(self)}; {f(self[0])}, ..., {f(self[-1])}'
        return contents

    def __repr__(self):
        contents = self._display_contents(repr, nmax=3)
        return f'{type(self).__name__}({contents})'

    def _repr_simple(self):
        '''return simple repr for self; includes type, len, and a repr_simple for a few elements.
        if less than 4 elements, just uses repr_simple for the elements (doesn't include len).
        '''
        contents = self._display_contents(repr_simple, nmax=3)
        return f'{type(self).__name__}({contents})'
    
    def __str__(self):
        contents = self._display_contents(str, nmax=3)
        return f'{type(self).__name__}({contents})'

    def _short_repr(self):
        '''return a shorter repr of self; just includes type & len.'''
        return f'{type(self).__name__}(with length {len(self)})'


def string_int_lookup(dict_):
    '''return dict_ but with DimensionValue, str, and int keys. dict_ keys should be DimensionValue objects.
    if any keys can't be converted to str or int, skip converting those keys to that type.
    '''
    result = dict()
    for key, val in dict_.items():
        result[key] = val
        try:
            result[str(key)] = val
        except TypeError:
            pass
        try:
            result[int(key)] = val
        except TypeError:
            pass
    return result

def string_int_index(list_):
    '''return dict mapping DimensionValue, str, and int keys to the indices of corresponding DimensionValue values.'''
    return {k: i for i, val in enumerate(list_) for k in (val, str(val), int(val))}

class DimensionValueList(SliceableList):
    '''SliceableList of DimensionValue elements. Also provides get() and lookup_dict() methods,
    which allow to get values based on int or string (or slice, or tuple or int or strings).
    Those methods use caching (assume int(element) & str(element) never changes for any element).

    istart: None or int
        if provided, reindex elements with new i values, starting from istart.
        E.g. istart=0 --> result.i == 0, 1, 2, ....
        elements which already have correct i will remain unchanged.
    '''
    _dimension_key_error = DimensionKeyError
    value_type = DimensionValue

    ndim = 1  # primary use: to distinguish between this and DimensionValue.

    s = elementwise_property('s')

    # # # CREATION OPTIONS # # #
    def __init__(self, *args_list, istart=None, **kw_list):
        if istart is None:
            super().__init__(*args_list, **kw_list)
        else:
            ll = list(*args_list, **kw_list)
            for i, el in enumerate(ll):
                ll[i] = el.with_i(i=istart+i)
            super().__init__(ll)

    @classmethod
    def from_strings(cls, strings):
        '''return cls instance from iterable of strings. (i will be determined automatically.)
        Equivalent to cls(cls.value_type(s, i) for i, s in enumerate(strings)).
        '''
        return cls(cls.value_type(s, i) for i, s in enumerate(strings))

    @classmethod
    def from_infos(cls, infos, **common_info):
        '''return cls instance from iterable of dicts. (i will be determined automatically.)
        dicts may contain any kwargs to pass to __init__ except for 'i'.

        values will all be instances of type cls.value_type.

        infos: iterable of dicts
            each one corresponds to one (cls.value_type) object in result.
        '''
        for info in infos:
            assert 'i' not in infos, 'i is determined automatically when using from_infos'
        return cls(cls.value_type(**info, i=i, **common_info) for i, info in enumerate(infos))

    @classmethod
    def from_dict(cls, int_to_element):
        '''return DimensionValueList from dict of {i: element}.'''
        result = cls(el for i, el in sorted(int_to_element.items()))
        for i, el in enumerate(result):
            if (i != el.i) and (el.i is not None):
                raise ValueError(f"expected i and element.i to match. i={i}, element.i={el.i}. (element={el})")
        return result
        
    @classmethod
    def unique_from(cls, elements, *elements_as_args, istart=None):
        '''return DimensionValueList of unique elements from elements.
        equality checked via element.equal_except_i, i.e. ignore index.

        elements: iterable of DimensionValue of cls.value_type.
            or, single DimensionValue, in which case treat it as first arg,
            and can provide more elements as additional args.
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        # bookkeeping
        if elements_as_args:
            elements = (elements,) + elements_as_args
        else:
            ndim = getattr(elements, 'ndim', None)
            if ndim is None:
                ndim = 1 if is_iterable(elements) else 0
            if ndim == 0:
                elements = (elements,)
        # getting result
        result = []
        for e in elements:
            for r in result:
                if e.equal_except_i(r):
                    break
            else:  # did not break, i.e. element not found
                result.append(e)
        return cls(result, istart=istart)

    def unique(self, *, istart=None):
        '''return DimensionValueList of unique elements from self.
        equality checked via element.equal_except_i, i.e. ignore index.
        (if all elements are unique, return self, else return new DimensionValueList.)
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        result = []
        for e in self:
            for r in result:
                if e.equal_except_i(r):
                    break
            else:  # did not break, i.e. element not found
                result.append(e)
        cls = type(self)
        if len(result) == len(self):
            result = self.with_istart(istart)
        else:
            result = cls(result, istart=istart)
        return result

    # # # REINDEXING / MANIPULATING # # #
    reindexed = alias('with_istart')

    def with_istart(self, istart=0):
        '''return new DimensionValueList with elements reindexed, starting from istart.
        elements with incorrect i will be replaced with copies.
        if istart is None, just return self, unchanged.
        '''
        if istart is None:
            return self
        return type(self)(el.with_i(i=istart+i) for i, el in enumerate(self))

    # # # LOOKUPS / GETTING ELEMENTS # # #
    def lookup_dict(self):
        '''return dict for looking up elements given int or str (or element) in self.
        uses caching; assumes int(element) & str(element) never changes for any element.
        '''
        # [TODO] Doesn't work when changing distribution names using fluids[N].s = Name.
        try:
            lookup = self._lookup
        except AttributeError:
            lookup = string_int_lookup({element: element for element in self})
            self._lookup = lookup
        return lookup

    def lookup(self, key, *, unique_missing_ok=False):
        '''return element given int, str, or element in self. raise DimensionKeyError if key not in self.
        unique_missing_ok: bool
            whether it is okay for self to be missing key if key is a UniqueDimensionValue.
            if True and key is a UniqueDimensionValue, return key instead of raising error.
        '''
        if unique_missing_ok and isinstance(key, UniqueDimensionValue):
            return key
        try:
            return self.lookup_dict()[key]
        except KeyError:
            raise self._dimension_key_error(key) from None

    def get(self, key):
        '''return element(s) corresponding to key.
        key: None, int, str, element, range, slice, or tuple/list (of int, str, or element in self)
            Some keys will look up and return corresponding element(s):
                nonnegative int, str, or element --> return corresponding element.
                tuple --> return tuple(self.get(k) for k in key)
                list --> return list(self.get(k) for k in key)
                range --> return type(self)(self.get(k) for k in key).
            Other keys will index self using the usual list-like indexing rules:
                None --> return self, unchanged.
                negative int --> return self[key], i.e. the key'th element, counting from end.
                slice --> return self[key], i.e. apply this slice to self.
                        Note that the result will have the same type as self.
                        Note that this supports interprets_fractional_indexing,
                          e.g. slice(0.3, 0.7) will slice(len(self) * 0.3, len(self) * 0.7).
            if any element in a tuple or list is not in self,
                keep it unchanged if it is a UniqueDimensionValue,
                else raise DimensionKeyError.
        Note that the result will always be single element, a tuple, a list, or a DimensionValueList.
        '''
        if key is None:
            return self
        # index self like it is a list:
        elif isinstance(key, slice):
            key = interprets_fractional_indexing(key, len(self))
            return self[key]
        elif is_integer(key) and key < 0:
            return self[key]
        # index by looking up key(s) in self:
        elif isinstance(key, (tuple, list)):
            return type(key)(self.lookup(k, unique_missing_ok=True) for k in key)
        elif isinstance(key, range):
            return type(self)(self.lookup(k) for k in key)
        else:
            return self.lookup(key, unique_missing_ok=False)

    # # # SERIALIZING # # #
    def to_dict(self):
        '''returns a list of dictionaries,
        each dictionary corresponds to each DimensionValue in the DimensionValueList.
        '''
        # [TODO][EFF] use dimension_value.to_dict(include_typename=False) for all except the first.
        result_list = []
        for dimension_value in self:
            result_list.append(dimension_value.to_dict())
        return result_list

    def serialize(self):
        '''return serialization of self, into a list of dictionaries.'''
        # [TODO][EFF] use dimension_value.to_dict(include_typename=False) for all except the first.
        result_list = []
        for dimension_value in self:
            result_list.append(dimension_value.to_dict())
        return result_list


''' --------------------- DimensionValueSetter --------------------- '''

class DimensionValueSetter():
    '''when dim.v = DimensionValueSetter instance dvs, use dim.v = dvs.value_to_set(dim) instead.
    
    value_to_set: callable
        dim -> any value to set dim.v = value.
    '''
    def __init__(self, value_to_set):
        self.value_to_set = value_to_set

    def __repr__(self):
        return f'{type(self).__name__}({self.value_to_set})'


''' --------------------- UniqueDimensionValue --------------------- '''

class UniqueDimensionValue(Sentinel, DimensionValue, DimensionValueSetter):
    '''a unique dimension value, not corresponding to a usual value from a DimensionValueList.
    E.g., INPUT_SNAP (defined in snaps.py) is the UniqueDimensionValue for the snap corresponding to the input deck.

    Cannot provide any args or kwargs to __init__.
    Equality with other dimension values only holds if the other value is a UniqueDimensionValue of the same type.
    str(UniqueDimensionValue) will return the type name.
    int(UniqueDimensionValue) will return None.
    '''
    def __init__(self, *args__None, **kw__None):
        pass  # do nothing (instead of super().__init__)

    i = None
    s = alias('_name')  # from Sentinel

    def __hash__(self):
        return super().__hash__()  # we need to do this since we define __eq__ here...

    def __eq__(self, other):
        return type(self) == type(other)

    def copy(self, **kw__None):
        '''return self; self is a Sentinel so there is only 1 instance.'''
        return self

    def value_to_set(self, dim):
        '''when dim.v = UniqueDimensionValue instance, set dim.v to this value instead.'''
        return self
