"""
File Purpose: derivatives (in one dimension at a time).
"""
import numpy as np
import xarray as xr

from ..quantity_loader import QuantityLoader
from ...errors import QuantCalcError
from ...tools import xarray_differentiate

DVARS = 'xyzt'  # one-letter string coordinate name options for differentiation.

class BasicDerivativeLoader(QuantityLoader):
    '''derivatives (in one dimension at a time).
    E.g. 'ddx_n' --> derivative of n with respect to x
    '''
    @known_pattern(fr'dd([{DVARS}])_(.+)', deps=[1])  # 'dd{x}_{var}'
    def get_derivative(self, var, *, _match=None):
        '''derivative. dd{x}_{var} --> d{var}/d{x}.
        self(var) must return an object with {x} in its coordinates.
            E.g. for x='y', self(var).coords['y'] are required.
        '''
        x, var = _match.groups()
        val0 = self(var)
        return xarray_differentiate(val0, x)
