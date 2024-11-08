"""
File Purpose: Component, ComponentList, ComponentDimension, ComponentHaver
"""
from .dimension_tools import (
    DimensionValue, DimensionValueList, string_int_lookup,
    Dimension, DimensionHaver,
)
from ..errors import ComponentKeyError, ComponentValueError
from ..tools import (
    take_along_dimension, join_along_dimension,
)

''' --------------------- Component & ComponentList --------------------- '''

class Component(DimensionValue):
    '''a single vector component coordinate (e.g. x, y, or z).
    Knows how to be converted to str and int. e.g. 'y' or 1.

    s: string or None
        str(self) --> s. if None, cannot convert to str.
    i: int or None
        int(self) --> i. if None, cannot convert to int.

    Note: not related to "coordinates", e.g. location in space.
    '''
    def __init__(self, s=None, i=None):
        super().__init__(s, i)


class ComponentList(DimensionValueList):
    '''list of vector component coordinates.'''
    _dimension_key_error = ComponentKeyError

    @classmethod
    def from_strings(cls, strings):
        '''return ComponentList from iterable of strings. (i will be determined automatically.)'''
        return cls(Component(s, i) for i, s in enumerate(strings))
        

XYZ = ComponentList.from_strings('xyz')
X, Y, Z = XYZ
YZ_FROM_X = string_int_lookup({X:(Y,Z), Y:(Z,X), Z:(X,Y)})  # right-handed coord system x,y,z given x.


''' --------------------- ComponentDimension, ComponentHaver --------------------- '''

class ComponentDimension(Dimension, name='component', plural='components',
                     value_error_type=ComponentValueError, key_error_type=ComponentKeyError):
    '''component dimension, representing current value AND list of all possible values.
    Also has various helpful methods for working with this Dimension.
    '''
    pass  # behavior inherited from Dimension.


@ComponentDimension.setup_haver
class ComponentHaver(DimensionHaver, dimension='component', dim_plural='components'):
    '''class which "has" a ComponentDimension. (ComponentDimension instance will be at self.component_dim)
    self.component stores the current vector component (possibly multiple). If None, use self.components instead.
    self.components stores "all possible vector components" for the ComponentHaver.
    Additionally, has various helpful methods for working with the ComponentDimension,
        e.g. current_n_component, iter_components, take_component.
        See ComponentDimension.setup_haver for details.

    components defaults to XYZ (==ComponentList.from_strings('xyz'))
    '''
    def __init__(self, *, component=None, components=XYZ, **kw):
        super().__init__(**kw)
        if components is not None: self.components = components
        self.component = component
