"""
File Purpose: tools for iterables
"""
import functools
import operator

import numpy as np

from .properties import simple_setdefault_property, simple_setdefaultvia_property, alias
from .sentinels import UNSET
from ..errors import InputConflictError
from ..defaults import DEFAULTS


''' ----------------------------- Misc ----------------------------- '''

def is_iterable(x):
    '''returns True if x is iterable, False otherwise.'''
    try:
        iter(x)
        return True
    except TypeError:
        return False

def is_dictlike(x):
    '''returns True if x is dict-like, False otherwise.
    returns x.is_dictlike if it exists,
    else returns whether x has keys() and __getitem__.
    '''
    try:
        x_is_dictlike = x.is_dictlike
    except AttributeError:
        return hasattr(x, 'keys') and hasattr(x, '__getitem__')
    else:
        return x_is_dictlike()

def argmax(iterable):
    '''returns first occurence of maximum value in iterable.
    converts iterable to tuple before beginning search.
    [EFF] might not be efficient for large iterables, but it's probably fine.
    '''
    l = tuple(iterable)
    return l.index(max(l))

def rargmax(iterable):
    '''returns first occurence of maximum value in iterable, starting search from the end.
    converts iterable to tuple before beginning search.
    [EFF] might not be efficient for large iterables, but it's probably fine.
    '''
    l = tuple(iterable)
    return len(l) - 1 - l[::-1].index(max(l))


''' ----------------------------- custom Dictlike ----------------------------- '''

class DictlikeFromKeysAndGetitem():
    '''Dict-like object, assuming keys() and __getitem__ are defined.'''
    def __getitem__(self, key):
        '''get value for this key'''
        raise NotImplementedError(f'{type(self).__name__}.__getitem__')

    def keys(self):
        '''return tuple of keys in self.'''
        raise NotImplementedError(f'{type(self).__name__}.keys()')

    def __iter__(self):
        '''raises TypeError; use .keys(), .values(), or .items() instead.'''
        raise TypeError(f'{type(self).__name__} is not iterable; use .keys(), .values(), or .items() instead.')

    def values(self):
        '''return tuple of values corresponding to self.keys().'''
        return tuple(self[key] for key in self.keys())

    def items(self):
        '''return tuple of (key, value) pairs corresponding to self.keys() and self.values().'''
        return tuple(zip(self.keys(), self.values()))

    def get(self, key, default=UNSET):
        '''return self[key]. if default is provided and self[key] doesn't exist, return default.'''
        try:
            return self[key]
        except KeyError:
            if default is UNSET:
                raise
            return default


''' ----------------------------- partitioning stuff ----------------------------- '''

class Partition(DictlikeFromKeysAndGetitem):
    '''(ordered) dict of lists partitioned by category.
    (assumes python >= 3.7, i.e. dict order is guaranteed to be insertion order)
    self assumes it will remain unchanged after originally being created.

    self.partition stores {key: list of elements in category}
    self.idx stores {key: list of indices of elements in original}
    self.flat stores all elements in category order, in a single list.
    self.idx_flat concatenates self.idx.values().
    self.ridx stores {key: [i such that self.flat[i] == x for x in this category]}
    self.ridx_flat stores [i such that self.flat[i] == x for x in original]

    iterating through self yields (key, value) pairs.

    original: list-like
        the original iterable, to be partitioned.
    f: callable
        maps original elements to category keys. categories must be hashable.
        Will call f(x) for x in original, to determine categories.
    keys: ordered list of categories
        use these as known categories if provided.
    '''
    def __init__(self, original, f, *, keys=[]):
        self.original = original
        self.f = f
        partition = dict()
        idx = dict()
        for key in keys:
            partition[key] = []
            idx[key] = []
        for i, x in enumerate(self.original):
            key = f(x)
            partition.setdefault(key, []).append(x)
            idx.setdefault(key, []).append(i)
        self.partition = partition
        self.idx = idx
        self.init_flat()
        self.init_ridx()

    def init_flat(self):
        '''create self.flat and self.idx_flat.
        self.flat stores all elements in order of categories, in a single list.
        self.idx_flat stores the indices of all elements in self.flat.
        '''
        flat = []
        for key in self.keys():
            flat.extend(self.partition[key])
        self.flat = flat
        idx_flat = []
        for key in self.keys():
            idx_flat.extend(self.idx[key])
        self.idx_flat = idx_flat

    def init_ridx(self):
        '''create self.ridx and self.ridx_flat.
        self.ridx stores {key: [i such that self.flat[i] == x for x in this category]}
        self.ridx_flat stores [i such that self.flat[i] == x for x in original]
        '''
        ridx_flat = []
        for i, x in enumerate(self.flat):
            ridx_flat.append(self.idx_flat.index(i))
        self.ridx_flat = ridx_flat
        ridx = dict()
        istart = 0
        for key in self.keys():
            cat_len = len(self.partition[key])
            ridx[key] = ridx_flat[istart:istart+cat_len]
            istart = istart + cat_len
        self.ridx = ridx

    def __getitem__(self, key):
        return self.partition[key]

    def keys(self):
        return list(self.partition.keys())

    # intentionally does not define __setitem__; expects to remain unchanged after __init__.

    def __iter__(self):
        '''iterate through (key, val) pairs.'''
        return iter(self.partition.items())

    def __contains__(self, key):
        '''tells whether key is in self.partition'''
        return key in self.partition

    # # # DISPLAY # # #
    def __repr__(self):
        return f'{type(self).__name__}({self.partition})'


''' ----------------------------- Generic Containers ----------------------------- '''

class Container():
    '''a container for multiple objects, & rules for enumerating & indexing.
    Here, implements self.__getitem__ so that self[i]=self.data[i],
        and self.enumerate which yields (i, self[i]) pairs.
    subclass should implement __init__, _enumerate_all, and new_empty.
    '''
    # # # THINGS THAT SUBCLASS SHOULD IMPLEMENT # # #
    def __init__(self, stuff):
        '''should set self.data = something related to stuff.'''
        raise NotImplementedError(f'{self.__class__.__name__}.__init__')

    def _enumerate_all(self):
        '''iterate through all objs in self, yielding (i, self[i]) pairs.
        Equivalent to self.enumerate(idx=None).
        The implementation will depend on the container type; subclass should implement.
        '''
        raise NotImplementedError(f'{self.__class__.__name__}._enumerate_all')

    def new_empty(self, fill=UNSET):
        '''return a new container of the same shape as self, filled with the value fill.
        The implementation will depend on the container type; subclass should implement.
        '''
        raise NotImplementedError(f'{self.__class__.__name__}.new_empty')

    def _size_all(self):
        '''return the number of objects in the container.
        The implementation will depend on the container type; subclass should implement.
        '''
        raise NotImplementedError(f'{self.__class__.__name__}.size_all')

    # # # GETITEM & ENUMERATE # # #
    def __getitem__(self, idx):
        return self.data[idx]

    def enumerate(self, idx=None):
        '''iterate through i in idx, yielding (i, self[i]) pairs.
        If idx is None, iterate through all objs in self (see self._enumerate_all).
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        if idx is None:
            for i, selfi in self._enumerate_all():
                yield (i, selfi)
        else:
            for i in idx:
                yield (i, self[i])

    def size(self, idx=None):
        '''return the number of objects in the container, or in idx if provided.'''
        if idx is None:
            return self._size_all()
        return len(idx)

    # # # DISPLAY # # #
    def __repr__(self):
        return f'{self.__class__.__name__}({self.data})'


class ContainerOfList(Container):
    '''a list-like container.'''
    def __init__(self, objs):
        self.data = [o for o in objs]

    def _enumerate_all(self):
        '''iterate through all objs in self, yielding (i, self[i]) pairs.'''
        return enumerate(self.data)

    def new_empty(self, fill=UNSET):
        '''return a new list of the same shape as self, filled with the value fill.'''
        return [fill for _ in self.data]

    def _size_all(self):
        '''the number of objects in this container. == len(self.data)'''
        return len(self.data)


class ContainerOfArray(Container):
    '''a numpy-array-like container.'''
    def __init__(self, arr):
        self.data = np.asanyarray(arr)

    def _enumerate_all(self):
        '''iterate through all objs in self, yielding (i, self[i]) pairs.'''
        return np.ndenumerate(self.data)

    def new_empty(self, fill=UNSET):
        '''return a new array of the same shape as self, filled with the value fill.'''
        return np.full_like(self.data, fill, dtype=object)

    def _size_all(self):
        '''the number of objects in this container. == self.data.size'''
        return self.data.size


class ContainerOfDict(Container):
    '''a dict-like container.'''
    def __init__(self, d):
        self.data = dict(d)  # copy the dict (and ensure dict-like)

    def _enumerate_all(self):
        '''iterate through all objs in self, yielding (i, self[i]) pairs.'''
        return self.data.items()

    def new_empty(self, fill=UNSET):
        '''return a new dict of the same shape as self, filled with the value fill.'''
        return {k: fill for k in self.data.keys()}

    def _size_all(self):
        '''the number of objects in this container. == len(self.data)'''
        return len(self.data)


''' ----------------------------- Bijection ----------------------------- '''

class Bijection(dict):
    '''stores forward and backward mapping.
    behaves like forward mapping, but self.inverse is the reverse mapping.
    '''
    inverse = simple_setdefault_property('_inverse', dict,
        doc='''reverse mapping. {value: key} for all items in this bijection.''')

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.inverse[value] = key

    def __getitem__(self, key):
        result = super().__getitem__(key)
        return result

    def __delitem__(self, key):
        value = self.pop(key)

    def clear(self):
        '''clear all items from this bijection.'''
        super().clear()
        self.inverse.clear()

    def pop(self, key, default=UNSET):
        '''pop the value for this key, and return it.'''
        value = super().pop(key, default)
        if value is not UNSET:
            del self.inverse[value]
        return value

    def popitem(self):
        '''pop an item from this bijection, and return it.'''
        key, value = super().popitem()
        del self.inverse[value]
        return key, value

    def update(self, *args, **kw):
        '''update this bijection with new items.'''
        super().update(*args, **kw)
        self.inverse.update({v: k for k, v in self.items()})

    def __repr__(self):
        return f'{type(self).__name__}({super().__repr__()})'


class BijectiveMemory(Bijection):
    '''bijection which also stores the next key to use. Keys should be numbers.
    self.nextkey is never decremented (don't "fill in gaps" after deleting keys)
    '''
    nextkey = simple_setdefaultvia_property('_nextkey', '_default_nextkey',
        doc='''next key for self.key(value) if new value.
        nextkey >= max(self.keys(), default=-1) + 1.''')
    def _default_nextkey(self):
        return max(self.keys(), default=-1) + 1

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.nextkey = max(self.nextkey, key) + 1

    def update(self, *args, **kw):
        super().update(*args, **kw)
        self.nextkey = max([self.nextkey-1, *self.keys()]) + 1

    def key(self, value):
        '''return the key associated with this value; store the value if not already stored.'''
        if value in self.inverse:
            return self.inverse[value]
        else:
            key = self.nextkey
            self[key] = value
            return key


''' ----------------------------- SymmetricPairMapping ----------------------------- '''

class SymmetricPairMapping():
    '''mapping with keys pairs, where order of the pair doesn't matter.

    mapping: dict of {(obj1, obj2): value}

    The keys (obj2, obj1) and (obj1, obj2) will be treated the same way,
        when getting/setting/deleting items, and when checking if key in self.
        [EFF] For efficiency, only stores one of these pairs (the one where obj1 <= obj2).
    '''
    def __init__(self, mapping=dict()):
        self.mapping = dict()
        for key, value in mapping.items():
            self[key] = value

    def _sanitize_key(self, key):
        '''return sanitized key (obj1, obj2) such that obj1 <= obj2.'''
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError(f'key={key!r} must be a tuple of 2 objs')
        if key[1] < key[0]:
            key = (key[1], key[0])
        return key
    
    def __setitem__(self, key, value):
        key = self._sanitize_key(key)
        self.mapping[key] = value

    def __getitem__(self, key):
        key = self._sanitize_key(key)
        return self.mapping[key]

    def __delitem__(self, key):
        key = self._sanitize_key(key)
        del self.mapping[key]

    def __contains__(self, key):
        key = self._sanitize_key(key)
        return key in self.mapping

    def update(self, other):
        '''update self with other.
        other: dict of {(obj1, obj2): value}
        '''
        for key, value in other.items():
            self[key] = value

    def clear(self):
        '''remove all known items from self.'''
        self.mapping.clear()

    def pop(self, key, default):
        '''remove self[key], and return its value. if key not in self, return default.'''
        key = self._sanitize_key(key)
        return self.mapping.pop(key, default)

    def __len__(self):
        return len(self.mapping)
    def values(self):
        return self.mapping.values()
    def items(self):
        return self.mapping.items()
    def keys(self):
        return self.mapping.keys()

    def __iter__(self):
        '''iterate over self.items (not self.keys).'''
        return iter(self.items())

    def copy(self):
        '''return a shallow copy of self.'''
        return type(self)(self.mapping)

    # # # DISPLAY # # #
    _repr_newlines = False  # whether to put newlines between keys in repr.

    def __repr__(self):
        if self._repr_newlines:
            SEP = f'\n{DEFAULTS.TAB}'
            JOINSEP = f',{SEP}'
            contents = [f'{k}: {v!r}' for k, v in self.mapping.items()]
            STARTSEP = SEP if len(contents) > 1 else ''
            ENDSEP = f'\n' if len(contents) > 3 else ''
            return f'{type(self).__name__}({STARTSEP}{JOINSEP.join(contents)}{ENDSEP})'
        else:
            return f'{type(self).__name__}({self.mapping!r})'


''' ----------------------------- DictOfSimilar ----------------------------- '''

class DictOfSimilar(dict):
    '''dict of similar objects with similar attributes.
    similar attributes list stored in SIMILAR_ATTRS.

    In many ways, simply broadcasts operations to all values in the dict.
    '''
    REPR_ITEM_MAXLEN = 50  # max length for repr for a single item; abbreviate if longer.
    SIMILAR_ATTRS = []
    cls_new = None  # if provided, use this to create new objects instead of type(self).

    def _new(self, *args, **kw):
        '''return a new ListOfSimilar of the same type as self.'''
        cls = type(self) if self.cls_new is None else self.cls_new
        return cls(*args, **kw)

    def apply(self, func, *args, **kw):
        '''return func(obj, *args, **kw) for each object in self.'''
        result = dict()
        for k, obj in self.items():
            result[k] = func(obj, *args, **kw)
        return self._new(result)

    do = alias('apply')

    gi = alias('getitems')
    si = alias('setitems')
    ga = alias('getattrs')
    sa = alias('setattrs')
    ca = alias('callattrs')

    def getitems(self, i):
        '''get obj[i] for each object in self.'''
        result = dict()
        for k, obj in self.items():
            result[k] = obj[i]
        return self._new(result)

    def setitems(self, i, value):
        '''set obj[i] = value for each object in self.'''
        for obj in self.values():
            obj[i] = value

    def getattrs(self, attr, default=UNSET):
        '''get obj.attr for each object in self.'''
        result = dict()
        for k, obj in self.items():
            if default is UNSET:
                result[k] = getattr(obj, attr)
            else:
                result[k] = getattr(obj, attr, default)
        return self._new(result)

    def setattrs(self, attr, value):
        '''set obj.attr = value for each object in self.'''
        for obj in self.values():
            setattr(obj, attr, value)

    def callattrs(self, attr, *args, **kw):
        '''call obj.attr(*args, **kw) for each object in self.'''
        result = dict()
        for k, obj in self.items():
            result[k] = getattr(obj, attr)(*args, **kw)
        return self._new(result)

    def __call__(self, *args, **kw):
        '''call obj(*args, **kw) for each object in self.'''
        result = dict()
        for k, obj in self.items():
            result[k] = obj(*args, **kw)
        return self._new(result)

    # # # SIMILAR ATTRS BEHAVIOR # # #
    def __getattr__(self, attr):
        '''self.getattrs(attr) if attr in SIMILAR_ATTRS. Else raise AttributeError.
        (Only invoked when object.__getattr__(self, attr) fails.)
        '''
        if attr in self.SIMILAR_ATTRS:
            return self.getattrs(attr)
        else:
            raise AttributeError(f'{type(self).__name__} object has no attribute {attr!r}')

    def __setattr__(self, attr, value):
        '''self.setattrs(attr, value) if attr in SIMILAR_ATTRS, otherwise super().__setattr__.'''
        if attr in self.SIMILAR_ATTRS:
            return self.setattrs(attr, value)
        else:
            return super().__setattr__(attr, value)

    def __getitem__(self, i):
        '''self[i[0]].getitems(i[1]) if i tuple and i[0] in SIMILAR_ATTRS.
            (e.g. self['snap', 0] returns self['snap'].getitems(0)
        otherwise, try super().__getitem__.
        if that fails, try to return list(self.values())[i]
            (e.g., self[3] will return 3rd object, unless 3 in self.keys())
        '''
        if isinstance(i, tuple) and i[0] in self.SIMILAR_ATTRS:
            return self.getattrs(i[0]).getitems(i[1])
        else:
            try:
                return super().__getitem__(i)
            except KeyError:
                return list(self.values())[i]

    def __setitem__(self, i, value):
        '''self.setitems(i[1], value) if i tuple and i[0] in SIMILAR_ATTRS. otherwise super().__setitem__.'''
        if isinstance(i, tuple) and i[0] in self.SIMILAR_ATTRS:
            return self.getattrs(i[0]).setitems(i[1], value)
        else:
            return super().__setitem__(i, value)

    # # # ARITHMETIC APPLIES ACROSS ALL VALUES # # #
    def _math_op(self, other, op):
        '''apply op to self and other. If other is a dict, apply op to self[k] and other[k] for each k.
        Otherwise, apply op to each value in self and other.
        '''
        if is_dictlike(other):
            return self._new({k: op(self[k], other[k]) for k in self})
        else:
            return self.apply(op, other)

    def __add__(self, other):
        '''self + other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.add)

    def __radd__(self, other):
        '''other + self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y + x)

    def __sub__(self, other):
        '''self - other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.sub)

    def __rsub__(self, other):
        '''other - self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y - x)

    def __mul__(self, other):
        '''self * other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.mul)

    def __rmul__(self, other):
        '''other * self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y * x)

    def __truediv__(self, other):
        '''self / other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.truediv)

    def __rtruediv__(self, other):
        '''other / self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y / x)

    def __floordiv__(self, other):
        '''self // other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.floordiv)

    def __rfloordiv__(self, other):
        '''other // self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y // x)

    def __mod__(self, other):
        '''self % other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.mod)

    def __rmod__(self, other):
        '''other % self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y % x)

    def __pow__(self, other):
        '''self ** other. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, operator.pow)

    def __rpow__(self, other):
        '''other ** self. At each key if other is a dict, else apply to each value in self.'''
        return self._math_op(other, lambda x, y: y ** x)

    def __pos__(self):
        '''+self. Apply to each value in self.'''
        return self.apply(operator.pos)

    def __neg__(self):
        '''-self. Apply to each value in self.'''
        return self.apply(operator.neg)

    # # # DISPLAY # # #
    def __repr__(self):
        MAXLEN = self.REPR_ITEM_MAXLEN
        orig_reprs = {k: repr(v) for k, v in self.items()}
        short_reprs = dict()
        for k, v in orig_reprs.items():
            if len(v) > MAXLEN:
                short_reprs[k] = f'<{v[:MAXLEN]}...>'.replace('\n', '  ')
            else:
                short_reprs[k] = v
        contents = [f'{k!r}: {v}' for k, v in short_reprs.items()]
        return f'{type(self).__name__}({{{", ".join(contents)}}})'

    def __str__(self):
        '''like repr but never abbreviate. Also, use str of objs.'''
        orig = {k: str(v) for k, v in self.items()}
        contents = [f'{k!r}: {v}' for k, v in orig.items()]
        content_str = ",\n".join(contents)
        return f'{type(self).__name__}({{{content_str}}})'
