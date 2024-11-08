"""
File Purpose: Specie in Bifrost. e.g. H_I, H_II, e, Fe_II
(code uses 'specie' as singular of 'species', to clarify singular vs plural.)
"""

from ..bifrost_elements import (
    ElementHaver, ElementHaverList,
    Element, ElementList,
)
from ....defaults import DEFAULTS
from ....dimensions import Fluid, FluidList
from ....errors import FluidValueError
from ....tools import (
    alias,
    UNSET,
    Binding,
    as_roman_numeral,
)
binding = Binding(locals())


''' --------------------- Species & SpeciesList --------------------- '''

class Specie(ElementHaver):
    '''Fluid corresponding to a specie, e.g. H_I, H_II, e, Fe_II.
    (code uses 'specie' as singular of 'species', to clarify singular vs plural.)

    CAUTION: some code assumes (without checking) that Specie objects are immutable.
        Changing a Specie after creating it could lead to unexpected behavior.

    species usually have a name. Every specie has a charge (possibly charge=0)
    non-electron species should also have an associated Element.

    name: UNSET, None, or str
        name of this specie.
        UNSET --> infer from element and q; None if no element.
                inferred name will be element name + roman numeral based on q,
                e.g. H_I for neutral H, H_II for H+.
        None --> cannot convert self to str.
    i: None or int
        the index of this specie (within a SpecieList).
        None --> cannot convert self to int.
    q: number
        charge, in elementary charge units (e.g. -1 for electrons, +1 for H_II)
    m: UNSET, None, or number
        mass, in atomic mass units (e.g. ~1 for H_I or H_II).
        UNSET --> use element.m.
        None --> cannot get self.m
    element: None or Element
        Element associated with this specie.
    '''
    _kw_def = {'name', 'i', 'q', 'm', 'element'}

    def __init__(self, name=UNSET, i=None, *, q, m=UNSET, element=None, **other_info):
        # bookkeeping
        if name is UNSET:
            name  = None if element is None else f'{element.name}_{as_roman_numeral(q+1)}'
        if m is UNSET:
            m     = None if element is None else element.m
        self.element = element
        super().__init__(name=name, i=i, m=m, q=q, **other_info)

    # # # CREATION OPTIONS # # #
    @classmethod
    def electron(cls, name='e', i=None, *, m=UNSET, **kw_init):
        '''create an electron Specie (with q=-1).
        m: if UNSET, use physical value: DEFAULTS.PHYSICAL.CONSTANTS_SI['me amu-1']
        '''
        if m is UNSET: m = DEFAULTS.PHYSICAL.CONSTANTS_SI['me amu-1']
        return cls(name=name, i=i, q=-1, m=m, **kw_init)

    @classmethod
    def from_element(cls, element, i=None, *, q, **kw_init):
        '''create a Specie from this Element (& charge q [elementary charge units]).
        name and m inferred from element and q, unless provided explicitly here.
        '''
        return cls(i=i, q=q, element=element, **kw_init)

    @classmethod
    def neutral(cls, element, i=None, **kw_init):
        '''create a neutral Specie (with q=0) from element.
        element: Element object. Used to infer name and m, by default.
        '''
        return cls.from_element(element, i=i, q=0, **kw_init)

    @classmethod
    def ion(cls, element, i=None, *, q=1, **kw_init):
        '''create an ion Specie from element and q [elementary charge units]
        element: Element object. Used to infer name and m, by default.
        '''
        if q <= 0:
            raise FluidValueError(f'q must be positive for ions, but got q={q}')
        return cls.from_element(element, i=i, q=q, **kw_init)

    # # # DISPLAY # # #
    def __repr__(self):
        contents = [repr(val) for val in [self.name, self.i] if val is not None]
        contents.append(f'q={self.q}')
        if (self.m is not None) and ((self.element is None) or (self.m != self.element.m)):
            contents.append(f'm={self.m:{".1e" if self.m < 1e-3 else ".3f"}}')
        if self.element is not None:
            contents.append(f'element={self.element.name}')
        return f'{type(self).__name__}({", ".join(contents)})'


class SpecieList(ElementHaverList):
    '''list of Specie objects.'''
    value_type = Specie
    element_list_cls = ElementList

    def prepend_electron(self, *, electron=UNSET, istart=0, **kw_specie):
        '''return SpecieList like self but prepend electron to result.
        electron: UNSET or Specie
            UNSET --> make new electron Specie via Specie.electron().
            Specie --> assert is_electron() then prepend this specie to result.
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        if electron is UNSET:
            electron = self.value_type.electron()
        elif not electron.is_electron():
            raise FluidValueError(f'cannot prepend non-electron specie {electron} to list of species')
        return type(self)([electron] + list(self), istart=istart)


''' --------------------- Binding Methods To ElementHavers --------------------- '''

with binding.to(ElementHaver):
    ElementHaver.specie_cls = Specie
    ElementHaver.specie_list_cls = SpecieList

    @binding
    def neutral(self, **kw_specie):
        '''return neutral Specie of this fluid's element.'''
        return self.specie_cls.neutral(self.element, **kw_specie)

    @binding
    def ion(self, q=1, **kw_specie):
        '''return ionized Specie of this fluid's element.
        q: charge in elementary charge units. (default: +1)
        '''
        return self.specie_cls.ion(self.element, q=q, **kw_specie)

    ElementHaver.get_I = alias('neutral')
    ElementHaver.get_II = alias('ion')

    @binding
    def saha_list(self, *, istart=0, **kw_specie):
        '''return SpecieList of neutral & once-ionized ions of this fluid's element.
        istart: start index for the SpecieList. Index affects conversion to int.
        '''
        return self.specie_list_cls([self.neutral(**kw_specie), self.ion(**kw_specie)], istart=istart)


with binding.to(ElementHaverList):
    ElementHaverList.specie_list_cls = SpecieList

    @binding
    def neutral_list(self, *, istart=0, **kw_specie):
        '''return SpecieList of neutral species for elements of fluids in self.
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        with_electron: bool or Specie. if provided, prepend electron specie to result.
        '''
        result = [ehaver.element.neutral(**kw_specie) for ehaver in self]
        return self.specie_list_cls(result, istart=istart)

    @binding
    def ion_list(self, *, q=1, istart=0, **kw_specie):
        '''return SpecieList of once-ionized ion for elements of fluids in self.
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        result = [ehaver.element.ion(q=q, **kw_specie) for ehaver in self]
        return self.specie_list_cls(result, istart=istart)

    @binding
    def saha_list(self, *, istart=0, **kw_specie):
        '''return SpecieList of neutral & once-ionized ion for elements of fluids in self.
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        result = []
        for i, h in enumerate(self):
            result.extend(h.element.saha_list(**kw_specie))
        return self.specie_list_cls(result, istart=istart)

    @binding
    def one_neutral_many_ions(self, *, q=1, istart=0, **kw_specie):
        '''return SpecieList of self[0].neutral() then self.ion_list(q=q).
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        neutral = self[0].neutral(**kw_specie)
        ions = self.ion_list(q=q, **kw_specie)
        return self.specie_list_cls([neutral] + ions, istart=istart)
