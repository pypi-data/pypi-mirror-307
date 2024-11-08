"""
File Purpose: BifrostMultifluidCalculator
"""

from .bifrost_ionization import BifrostIonizationLoader
from .bifrost_multifluid_bases import BifrostMultifluidBasesLoader
from .bifrost_number_densities import BifrostNumberDensityLoader
from .bifrost_species import SpecieList
from ..bifrost_calculator import BifrostCalculator
from ..bifrost_elements import ElementList
from ....dimensions import SINGLE_FLUID
from ....plasma_calculator import MultifluidPlasmaCalculator
from ....tools import (
    alias,
    format_docstring,
)

@format_docstring(bifrost_calculator_docs=BifrostCalculator.__doc__, sub_ntab=1)
class BifrostMultifluidCalculator(BifrostIonizationLoader, BifrostNumberDensityLoader,
                                  BifrostMultifluidBasesLoader,
                                  MultifluidPlasmaCalculator, BifrostCalculator):
    '''MultifluidPlasmaCalculator for Bifrost outputs.
    various possible ways to infer fluids.
        One possibility is to use abundances + saha ionization equation.
        [TODO] explain this in more detail.
        [TODO] allow to enter fluids as list of strings during init.

    set self.fluid=SINGLE_FLUID to get single-fluid values,
        otherwise will get inferred multifluid values.

    --- Docstring from BifrostCalculator copied below ---
        {bifrost_calculator_docs}
    '''
    # parent class ordering notes:
    # - IonizationLoader must go before MultifluidBasesLoader,
    #     because MultifluidBasesLoader parent BasesLoader defines get_ionfrac too;
    #     this affects known_var results... (maybe it's a bug in known_var code?)
    #     with this ordering, KNOWN_VARS['ionfrac'].cls_where_defined is IonizationLoader;
    #     without this ordering, it is BasesLoader instead, which gives wrong deps.

    SINGLE_FLUID = SINGLE_FLUID  # convenient reference to SINGLE_FLUID. Subclass should NEVER override.
    element_list_cls = ElementList

    def __init__(self, snapname=None, *, units='si', **kw_super):
        super().__init__(snapname=snapname, units=units, **kw_super)
        self.init_fluids()

    # # # FLUIDS # # #
    def init_fluids(self):
        '''initialize self.fluid and self.jfluid.'''
        self.fluids = self.chromo_fluid_list()
        self.jfluids = self.fluids
        self.jfluid = self.jfluids.neutrals()

    @property
    def elements(self):
        '''ElementList of unique elements found in any of self.fluids.
        To alter self.elements, adjust self.fluids; will infer new self.elements automatically.
        Default: self.tabin.make_element_list(), which comes from self.params['tabinputfile'].
        '''
        return self.element_list_cls.unique_from_element_havers(self.fluids, istart=0)

    def chromo_fluid_list(self):
        '''SpecieList of species relevant to the chromosphere, maybe.
        currently, just produces list of [electron, H_I, H_II, *other_once_ionized_ions]
            also includes He_III (after He_II) if self.params['do_helium'].
        '''
        elements = self.tabin.elements
        if (elements[0] != 'H') or (elements[1] != 'He'):
            raise NotImplementedError('[TODO] chromo_fluid_list for other elements list?')
        H = elements.get('H')
        He = elements.get('He')
        other = elements[2:]
        result = [SpecieList.value_type.electron(),
                  H.neutral(),
                  H.ion(1),
                  He.ion(1),
                  ]
        if self.params.get('do_helium', False):
            result.append(He.ion(2))  # include He_III
        result.extend(other.ion_list(q=1))
        return SpecieList(result, istart=0)  # istart=0 --> renumber for this list.

    # # # COLLISIONS # # #
    # aliases to check during set_collisions_crosstab_defaults
    #    (which gets called the first time self.collisions_cross_mapping is accessed).
    # override from super() to avoid 'H' and 'He' aliases to avoid ambiguity with Element fluids.
    _COLLISIONS_CROSSTAB_DEFAULT_FLUIDS_ALIASES = \
        MultifluidPlasmaCalculator._COLLISIONS_CROSSTAB_DEFAULT_FLUIDS_ALIASES.copy()
    _COLLISIONS_CROSSTAB_DEFAULT_FLUIDS_ALIASES.update({
        'H_I'   : ['H_I',    'H I'],  # exclude 'H', since 'H' might be an Element.
        'He_I'  : ['He_I',   'He I'], # exclude 'He', since 'He' might be an Element.
        })
