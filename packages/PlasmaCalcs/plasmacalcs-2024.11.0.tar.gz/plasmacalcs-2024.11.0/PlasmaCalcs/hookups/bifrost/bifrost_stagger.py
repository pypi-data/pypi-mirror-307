"""
File Purpose: Bifrost Stagger (align inputs to grid)

STAGGER ORDERS DEFINED HERE:
    1 - "simplest" method available.
            good enough, for most uses. ~20% faster than order=5
    5 - improved 5th order scheme.
            the improvement refers to improved precision for "shift" operations.

The implementations here use numpy.
Future implementations may use numba if numpy is too slow
    helita has numba implementation but numba can make installation more challenging;
    if adding numba here be sure to make it optional, not a requirement for PlasmaCalcs.

TESTED:
    seems to give same results as helita implementation, for 5th order numpy scheme.
    seems to take roughly the same amount of time as helita implementation
        (maybe 5 to 10% faster for shifts. Within 5% speed for derivatives.)
"""

import collections
import os

import numpy as np

from ...defaults import DEFAULTS
from ...errors import (
    InputError, InputMissingError,
    DimensionalityError, DimensionSizeError,
)
from ...tools import (
    alias, alias_child, simple_property, simple_setdefaultvia_property, 
)
from ...quantities import QuantityLoader


''' --------------------- Stagger Constants --------------------- '''

XYZ_TO_INT = {'x': 0, 'y': 1, 'z': 2}
PAD_PERIODIC = 'wrap'     # how to pad periodic dimensions
PAD_NONPERIODIC = 'reflect'  # how to pad nonperiodic dimensions

StaggerConstants = collections.namedtuple('StaggerConstants', ('a', 'b', 'c'))

# # FIRST ORDER SCHEME # #
STAGGER_ABC_DERIV_o1 = StaggerConstants(1.0, 0, 0)
STAGGER_ABC_SHIFT_o1 = StaggerConstants(0.5, 0, 0)

# # FIFTH ORDER SCHEME # #
# derivatives
c = (-1 + (3**5 - 3) / (3**3 - 3)) / (5**5 - 5 - 5 * (3**5 - 3))
b = (-1 - 120*c) / 24
a = (1 - 3*b - 5*c)
STAGGER_ABC_DERIV_o5 = StaggerConstants(a, b, c)

# shifts (i.e. not a derivative)
c = 3.0 / 256.0
b = -25.0 / 256.0
a = 0.5 - b - c
STAGGER_ABC_SHIFT_o5 = StaggerConstants(a, b, c)

# remove temporary variables from the module namespace
del c, b, a


''' --------------------- Stagger Tools --------------------- '''

def transpose_to_0(array, x):
    '''move x (int) axis to the front of array (numpy array), by swapping with 0th axis.
    
    Note this is its own inverse, i.e. transpose_to_0(transpose_to_0(array, x), x) == array.
    '''
    tup = transpose_to_0_tuple(array.ndim, x)
    return np.transpose(array, tup)

def transpose_to_0_tuple(ndim, x):
    '''return tuple to pass to np.transpose to swap axis 0 with axis x (int).

    T = np.transpose(array, result) gives array with x axis swapped with 0th axis.
    np.transpose(T, result) swaps them back.
    '''
    if x < 0:
        x = x + ndim  # e.g. (ndim=3, x=-1) --> x=2
    if x >= ndim:
        raise DimensionalityError(f'axis x={x} is out of bounds for ndim={ndim}')
    result = list(range(ndim))
    result[x] = 0
    result[0] = x
    return tuple(result)

def simple_slice(start_shift, end_shift):
    '''return slice(start_shift, end_shift), but if end_shift is 0 use None instead.'''
    return slice(start_shift, None if end_shift == 0 else end_shift)


''' --------------------- Staggerer --------------------- '''

class Staggerer():
    '''class to do staggering along an axis.
    internally, staggering will transpose, stagger along 0th axis, then transpose back.
    
    x: int or str
        the axis to take the derivative along.
        str --> 'x', 'y', or 'z', corresponding to 0, 1, 2.
        internally stored as int.
    periodic: bool
        whether to treat the array as periodic along x.
        True --> use pad='wrap' to fill values for stagger at edges of array.
        False --> use pad='reflect' to fill values for stagger at edges of array.
    dx: None, number, or 1D array
        spacing along this axis. relevant for deriv but not shift.
        None --> deriv methods will crash.
    order: 1 or 5.
        order of the scheme to use, by default.
    mode: str
        method for stagger calculations. Right now, only supports 'numpy_improved'.
        Eventually might support 'numpy', 'numba', and 'numba_improved'.
    short_ok: bool
        whether it is okay for arrays to be too short along x axis.
        True --> if too short: for shift, return as-is; for derivative, return zeros.
        False --> if too short: raise DimensionSizeError
    assert_ndim: None or int
        if provided, assert ndim(array) equals this value, before staggering.
        e.g. if expecting all arrays to be 3D, use assert_ndim=3.
    '''
    def __init__(self, x, *, periodic, dx=None, order=5, mode='numpy_improved',
                 short_ok=True, assert_ndim=None):
        self.x = XYZ_TO_INT.get(x, x)  # convert to int if str
        self.periodic = periodic
        self.order = order
        self.dx = dx
        self.mode = mode
        if mode != 'numpy_improved':
            raise NotImplementedError(f'mode={mode!r}. Only implemented mode="numpy_improved" so far.')
        self.short_ok = short_ok
        self.assert_ndim = assert_ndim

    # # # PROPERTIES # # #
    dx = simple_property('_dx',
            doc='''spacing along this axis. relevant for deriv but not shift.
            if None, getting self.dx will raise InputMissingError.''')
    @dx.getter
    def dx(self):
        result = getattr(self, '_dx', None)
        if result is None:
            raise InputMissingError('dx is None, but dx required for derivatives.')
        return result

    # # # SIZE CHECK # # #
    def size_x(self, array):
        '''returns size of array along x axis.'''
        return array.shape[self.x]

    def at_least_size_x(self, array, size, *, short_ok=None):
        '''returns whether array has at least this size along x axis.
        short_ok: None or bool
            whether it is okay for arrays to be too short along x axis.
            None --> use self.short_ok.
            False --> raise DimensionSizeError if too short.
        '''
        if short_ok is None:
            short_ok = self.short_ok
        size_x = self.size_x(array)
        if size_x < size:
            if short_ok:
                return False
            else:
                errmsg = f'array too short in axis {self.x}: got {size_x}; expected >= {size}.'
                raise DimensionSizeError(errmsg)
        else:
            return True

    # # # STAGGER PREP & POST # # #
    def pad_amount(self, *, up):
        '''amount of padding required at (start, end) of arrays.
        up=True (up) or False (down)
        '''
        if up:
            return (2, 3)
        else:
            return (3, 2)

    def pad(self, transposed_array, *, up):
        '''pad array along 0th axis as appropriate, to prepare it for staggering computations.
        up=True (up) or False (down)
        '''
        pad_amount = self.pad_amount(up=up)
        pad_mode = PAD_PERIODIC if self.periodic else PAD_NONPERIODIC
        # pad_amount applies to 0th axis; all other axes padded by (0, 0).
        padding = [pad_amount] + [(0, 0)] * (transposed_array.ndim - 1)
        return np.pad(transposed_array, padding, mode=pad_mode)

    def transpose(self, array):
        '''swap axis self.x with axis 0.
        Note, this is its own inverse, i.e. transpose(transpose(array)) == array.
        '''
        return transpose_to_0(array, self.x)

    def _pre_stagger_prep(self, array, *, up):
        '''return array prepped for staggering.
        i.e., transpose to put x axis at front, then pad appropriately.
        Also ensure array ndim == self.assert_ndim if provided.
        '''
        if self.assert_ndim is not None:
            if array.ndim != self.assert_ndim:
                errmsg = f'array ndim ({array.ndim}) != assert_ndim ({self.assert_ndim})'
                raise DimensionalityError(errmsg)
        array_transpose = self.transpose(array)
        return self.pad(array_transpose, up=up)

    def _post_stagger(self, array):
        '''return array converted back to original format, post-staggering.
        i.e., transpose to put x axis from front back to original position.
        '''
        return self.transpose(array)

    # # # SHIFTS # # #
    def shift(self, array, *, up):
        '''shift array along x axis, staggering as appropriate.
        up=True (up) or False (down)
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        order = self.order
        if order == 1:
            return self.shift_o1(array, up=up)
        elif order == 5:
            return self.shift_o5(array, up=up)
        else:
            raise InputError(f'order={order} not supported; must be 1 or 5')

    def shift_o1(self, array, *, up):
        '''first order shift, staggering up.'''
        raise NotImplementedError('[TODO]')  # could use 

    def shift_o5(self, array, *, up):
        '''fifth order shift, staggering as appropriate.'''
        if not self.at_least_size_x(array, 5):
            return array
        f = self._pre_stagger_prep(array, up=up)
        A, B, C = STAGGER_ABC_SHIFT_o5
        upshift = 1 if up else 0
        Pstart, Pend = self.pad_amount(up=up)
        start = Pstart + upshift
        end = -Pend + upshift
        i00 = simple_slice(start + 0, end + 0)
        i1p = simple_slice(start + 1, end + 1)
        i2p = simple_slice(start + 2, end + 2)
        i1m = simple_slice(start - 1, end - 1)
        i2m = simple_slice(start - 2, end - 2)
        i3m = simple_slice(start - 3, end - 3)
        f0 = f[i00]
        out = f0 + (A * (            f[i1m]-f0) +
                    B * (f[i1p]-f0 + f[i2m]-f0) +
                    C * (f[i2p]-f0 + f[i3m]-f0))
        result = self._post_stagger(out)
        return result

    # # # DERIVATIVES # # #
    def deriv(self, array, *, up):
        '''take derivative of array along x axis, staggering as appropriate.
        up=True (up) or False (down)
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        order = self.order
        if order == 1:
            return self.deriv_o1(array, up=up)
        elif order == 5:
            return self.deriv_o5(array, up=up)
        else:
            raise InputError(f'order={order} not supported; must be 1 or 5')

    def deriv_o1(self, array, *, up):
        '''first order derivative, staggering up.'''
        raise NotImplementedError('[TODO]')

    def deriv_o5(self, array, *, up):
        '''fifth order derivative, staggering as appropriate.'''
        if not self.at_least_size_x(array, 5):
            return np.zeros_like(array)
        dx = self.dx
        if 0 < np.ndim(dx) < np.ndim(array):  # add enough np.newaxis for dx dims if needed.
            dx = np.expand_dims(dx, tuple(range(np.ndim(dx), np.ndim(array))))
        f = self._pre_stagger_prep(array, up=up)
        A, B, C = STAGGER_ABC_DERIV_o5
        upshift = 1 if up else 0
        Pstart, Pend = self.pad_amount(up=up)
        start = Pstart + upshift
        end = -Pend + upshift
        i00 = simple_slice(start + 0, end + 0)
        i1p = simple_slice(start + 1, end + 1)
        i2p = simple_slice(start + 2, end + 2)
        i1m = simple_slice(start - 1, end - 1)
        i2m = simple_slice(start - 2, end - 2)
        i3m = simple_slice(start - 3, end - 3)
        out = dx * (A * (f[i00] - f[i1m]) + 
                    B * (f[i1p] - f[i2m]) +
                    C * (f[i2p] - f[i3m]))
        result = self._post_stagger(out)
        return result

    # # # SHORTHANDS # # #
    def shift_up(self, array):
        '''shift array up. Equivalent: shift(array, up=True)'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        return self.shift(array, up=True)

    def shift_dn(self, array):
        '''shift array down. Equivalent: shift(array, up=False)'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        return self.shift(array, up=False)

    def deriv_up(self, array):
        '''take derivative of array up. Equivalent: deriv(array, up=True)'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        return self.deriv(array, up=True)

    def deriv_dn(self, array):
        '''take derivative of array down. Equivalent: deriv(array, up=False)'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        return self.deriv(array, up=False)

    up = alias('shift_up')
    dn = alias('shift_dn')
    ddup = alias('deriv_up')
    dddn = alias('deriv_dn')

    # # # DISPLAY # # #
    def __repr__(self):
        contents = [f'x={self.x!r}',
                    f'periodic={self.periodic}',
                    f'order={self.order}'
                    ]
        if self.dx is None:
            contents.append('dx=None')
        if self.mode != 'numpy_improved':
            contents.append(f'mode={self.mode!r}')
        return f'{type(self).__name__}({", ".join(contents)})'


''' --------------------- Stagger Interface 3D --------------------- '''

class StaggerInterface3D():
    '''class to do staggering along 'x', 'y', or 'z', axes.
    Call self(array, opstr) to do the operation(s) implied by opstr (from left to right)
        E.g. self(array, 'xup ddzdn') --> shift array up x, then take z derivative down.

    periodic_x, periodix_y, periodic_z: bool
        whether to treat arrays as periodic along x, y, z axes.
        True --> use pad='wrap' to fill values for stagger at edges of array.
        False --> use pad='reflect' to fill values for stagger at edges of array.
    dx, dy, dz: None, number, or 1D array
        spacing along each axis. relevant for deriv but not shift.
        None --> deriv methods will crash.
    order: 1 or 5.
        order of the scheme to use, by default.
    mode: str
        method for stagger calculations. Right now, only supports 'numpy_improved'.
        Eventually might support 'numpy', 'numba', and 'numba_improved'.

    self.x, self.y, self.z store Staggerer objects for each axis.
    '''
    staggerer_cls = Staggerer

    def __init__(self, *,
                 periodic_x, periodic_y, periodic_z,
                 dx=None, dy=None, dz=None,
                 order=5, mode='numpy_improved'):
        kw_shared = dict(order=order, mode=mode, assert_ndim=3)
        self.x = self.staggerer_cls('x', periodic=periodic_x, dx=dx, **kw_shared)
        self.y = self.staggerer_cls('y', periodic=periodic_y, dx=dy, **kw_shared)
        self.z = self.staggerer_cls('z', periodic=periodic_z, dx=dz, **kw_shared)

    # # # ALIASES - ORDER AND MODE # # #
    order = alias_child('x', 'order')
    @order.setter
    def order(self, value):
        self.x.order = value
        self.y.order = value
        self.z.order = value

    mode = alias_child('x', 'mode')
    @mode.setter
    def mode(self, value):
        self.x.mode = value
        self.y.mode = value
        self.z.mode = value

    # # # ALIASES - OPERATIONS # # #
    xup = alias_child('x', 'shift_up')
    xdn = alias_child('x', 'shift_dn')
    yup = alias_child('y', 'shift_up')
    ydn = alias_child('y', 'shift_dn')
    zup = alias_child('z', 'shift_up')
    zdn = alias_child('z', 'shift_dn')

    ddxup = alias_child('x', 'deriv_up')
    ddxdn = alias_child('x', 'deriv_dn')
    ddyup = alias_child('y', 'deriv_up')
    ddydn = alias_child('y', 'deriv_dn')
    ddzup = alias_child('z', 'deriv_up')
    ddzdn = alias_child('z', 'deriv_dn')

    # # # DO / CALL # # #
    def do(self, array, opstr, left_first=True):
        '''do the operation(s) implied by opstr.

        opstr: str
            string of operations to do, separated by whitespace.
            each operation must be one of:
                'xup',   'xdn',   'yup',   'ydn',   'zup',   'zdn',
                'ddxup', 'ddxdn', 'ddyup', 'ddydn', 'ddzup', 'ddzdn'.
        left_first: bool
            when multiple operations, tells order in which to apply them.
            True --> apply operations from left to right.
                    E.g. 'xup ddzdn' --> first shift x up, then take z derivative down.
            False --> apply operations from right to left.
                    E.g. 'xup ddzdn' --> first take z derivative down, then shift x up.
        '''
        ops = opstr.split()
        if not left_first:
            ops = ops[::-1]
        for op in ops:
            xup = getattr(self, op)  # one of the ops, e.g. self.xup or self.ddzdn
            array = xup(array)
        return array

    __call__ = alias('do')

    # # # DISPLAY # # #
    def __repr__(self):
        contents = [f'periodic_x={self.x.periodic}',
                    f'periodic_y={self.y.periodic}',
                    f'periodic_z={self.z.periodic}',
                    f'order={self.order}'
                    ]
        if self.x.dx is None:
            contents.append('dx=None')
        if self.y.dx is None:
            contents.append('dy=None')
        if self.z.dx is None:
            contents.append('dz=None')
        if self.mode != 'numpy_improved':
            contents.append(f'mode={self.x.mode!r}')
        return f'{type(self).__name__}({", ".join(contents)})'


''' --------------------- Stagger Interface 3D Haver --------------------- '''

class BifrostStaggerable(QuantityLoader):
    '''manages stagger stuff for BifrostCalculator'''
    stagger_interface_cls = StaggerInterface3D

    stagger = simple_setdefaultvia_property('_stagger', '_create_stagger_interface',
            doc='''stagger interface object, for doing staggering operations.
            BifrostCalculator staggers values to grid cell centers upon loading, by default.
            When all values are at cell centers, can proceed without any more staggering.''')

    def _create_stagger_interface(self):
        '''create stagger interface based on self.params'''
        params = self.params
        kw = {}
        kw['periodic_x'] = params['periodic_x']
        kw['periodic_y'] = params['periodic_y']
        kw['periodic_z'] = params['periodic_z']
        if os.path.isfile(params['meshfile']):
            mesh_coords = self.load_mesh_coords()
            kw['dx'] = mesh_coords['dx']
            kw['dy'] = mesh_coords['dy']
            kw['dz'] = mesh_coords['dz']
        else:
            kw['dz'] = params['dx']
            kw['dy'] = params['dy']
            kw['dz'] = params['dz']  # might crash... but that's ok;
            # PlasmaCalcs doesn't yet know how to handle different dz for each snapshot.
        return self.stagger_interface_cls(**kw)

    # # # BEHAVIOR ATTRS # # #
    stagger_order = alias_child('stagger', 'order')
    stagger_mode = alias_child('stagger', 'mode')

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['stagger_order', 'stagger_mode'], plus any behavior_attrs from super().
        '''
        return ['stagger_order', 'stagger_mode'] + list(getattr(super(), 'behavior_attrs', []))

    # # # VARS # # #
    @known_pattern(r'([xyz])(up|dn)_(.+)', deps=[2])  # e.g. xup_r
    def get_stagger_shift(self, var, *, _match=None):
        '''stagger shift of var up or down by half grid cell along indicated axis.
        E.g. xup_r --> shift r up along x axis.
        '''
        x, up, var = _match.groups()
        unstaggered = self(var)
        return self.stagger(var, f'{x}{up}')

    @known_pattern(r'dd([xyz])(up|dn)_(.+)', deps=[2])  # e.g. ddxup_r
    def get_stagger_deriv(self, var, *, _match=None):
        '''stagger derivative of var up or down along indicated axis.
        result will be located half grid cell away from var.
        E.g. ddxup_r --> take x derivative of r up along x axis.
        '''
        x, up, var = _match.groups()
        unstaggered = self(var)
        return self.stagger(var, f'dd{x}{up}')
