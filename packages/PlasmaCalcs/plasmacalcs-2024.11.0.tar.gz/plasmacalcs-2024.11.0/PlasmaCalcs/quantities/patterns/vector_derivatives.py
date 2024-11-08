"""
File Purpose: vector derivatives (e.g. curl, div, grad)
"""
from ..quantity_loader import QuantityLoader
from ...dimensions import YZ_FROM_X
from ...tools import xarray_differentiate

class VectorDerivativeLoader(QuantityLoader):
    '''vector derivatives (e.g. curl, div, grad).
    E.g. div_u --> div(u), i.e. du_x/dx + du_y/dy + du_z/dz.
    '''
    # div_{var}; optional "__{axes}"
    @known_pattern(r'div_(.*?[^_]+?)(__[xyz]{1,3})?', deps=[0], ignores_dims=['component'])
    def get_div(self, var, *, _match=None):
        '''divergence. 'div_{var}' --> div(var), i.e. du_x/dx + du_y/dy + du_z/dz.
        if component(s) is provided, only include that component(s) during the calculation.
            e.g. div_u__xy --> du_x/dx + du_y/dy.
        '''
        var, axes = _match.groups()
        axes = 'xyz' if (axes is None) else axes[len('__'):]  # remove '__'. e.g. '__x' --> 'x'
        value = self(f'{var}_{axes}')   # [EFF] get all components at once, instead of one at a time.
        comps = self.take_components(value, drop_labels=True)  # e.g. [var_x, var_y, var_z]
        return sum(xarray_differentiate(val, str(x)) for val, x in zip(comps, axes))

    # grad_{var}
    @known_pattern(r'grad_(.+)', deps=[0])
    def get_grad(self, var, *, _match=None):
        '''gradient. 'grad_{var}' --> grad(var), i.e. (dn/dx, dn/dy, dn/dz).
        returned components are determined by self.component.
            (see also: the get_xyz pattern. E.g., 'grad_n_x' --> x component of grad(n).
            to get grad of a vector's component instead, use parentheses, e.g. 'grad_(u_x)')
        '''
        var, = _match.groups()
        value = self(var)   # for grad, var is a scalar.
        result = []
        with self.maintaining('component'):  # restore original component afterwards.
            for x in self.iter_component():
                dval = xarray_differentiate(value, str(x))
                result.append(self.assign_component_coord(dval, x))
        return self.join_components(result)

    def curl_component(self, v, x, *, yz=None):
        '''return x component of curl(v).

        x: int, str, or Component
            tells component to get. if int or str, use self.components to get corresponding Component
        v: xarray.DataArray
            vector to take curl of.
            spatial derivatives will apply to dimensions ('x', 'y', 'z') (if they exist, else give 0).
            must include 'components' dimension including coordinates y and z.
        yz: None or iterable of two (int, str, or Component) objects
            the other two components; (x,y,z) should form a right-handed coordinate system.
            if not provided, infer from x.
        '''
        if yz is None: yz = YZ_FROM_X[x]
        y, z = yz
        vy, vz = self.take_components(v, yz)
        ddy_vz = xarray_differentiate(vz, str(y))
        ddz_vy = xarray_differentiate(vy, str(z))
        return self.assign_component_coord(ddy_vz - ddz_vy, x)

    # curl_{var}
    @known_pattern(r'curl_(.+)', deps=[0])
    def get_curl(self, var, *, _match=None):
        '''curl. 'curl_{var}' --> curl(var), i.e. (du_z/dy - du_y/dz, du_x/dz - du_z/dx, du_y/dx - du_x/dy).
        returned components are determined by self.component.
            (see also: the get_xyz pattern. E.g., curl_u_x --> x component of curl(u))
        '''
        var, = _match.groups()
        if not self.component_is_iterable():  # single component of result,
            # so we only need some of the components of var
            x = self.component
            y, z = yz = YZ_FROM_X[x]
            v = self(f'{var}_{y}{z}')
            return self.curl_component(v, x, yz=yz)
        # else: multiple components of result -- we do need all the components of var.
        v = self(f'{var}_xyz')
        result = [self.curl_component(v, x) for x in self.component]
        return self.join_components(result)
