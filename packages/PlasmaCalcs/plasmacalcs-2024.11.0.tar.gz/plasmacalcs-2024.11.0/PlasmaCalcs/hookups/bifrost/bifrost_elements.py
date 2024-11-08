"""
File Purpose: elements in Bifrost
BifrostCalculator can later infer element densities via abundances, ionization via saha.
"""

from ...defaults import DEFAULTS
from ...dimensions import Fluid, FluidList
from ...errors import FluidKeyError, InputConflictError
from ...tools import (
    alias, elementwise_property,
    identity,
)


''' --------------------- ElementHaver & ElementHaverList --------------------- '''

class ElementHaver(Fluid):
    '''fluid which may "have" an element. E.g. Element or Specie.
    (Useful for behavior shared by Element and Specie class in multifluid case.)

    name: None or str
        name of this fluid. None --> name unknown.
    i: None or int
        index of this fluid (within an ElementHaverList)
    element: None, or Element
        the element which this ElementHaver "has"
    '''
    def __init__(self, name=None, i=None, *, element=None, **other_info):
        super().__init__(name=name, i=i, **other_info)
        if (element is not None) or (not hasattr(self, 'element')):
            self.element = element

    def get_element(self):
        '''return self.element if provided (not None), else crash with FluidKeyError.'''
        if self.element is None:
            raise FluidKeyError(f'get_element() fails when self.element=None. (self={self!r})')
        return self.element


class ElementHaverList(FluidList):
    '''list of ElementHaver objects.'''
    element_list_cls = NotImplemented  # defined at bottom of this file. Subclass might override.

    element = elementwise_property('element')
    elements = alias('element')

    @classmethod
    def unique_from_element_havers(cls, element_havers, istart=0):
        '''return ElementList (cls.element_list_cls) composed of unique elements from element_havers.
        element_havers: iterable of (probably) ElementHaver objects.
                objects without obj.element (or with element=None) will be ignored.
        istart: start index for the ElementList. Index affects conversion to int.
        '''
        elements = [h.element for h in element_havers if getattr(h, 'element', None) is not None]
        return cls.element_list_cls.unique_from(elements, istart=istart)

    def unique_elements(self, *, istart=None):
        '''return ElementList composed of unique elements from self.
        istart: None or int. int --> use result[k].with_i(istart + k) for all k.
        '''
        elements = [s.element for s in self if getattr(s, 'element', None) is not None]
        return self.element_list_cls.unique_from(elements, istart=istart)


''' --------------------- Element & ElementList --------------------- '''

class Element(ElementHaver):
    '''Fluid corresponding to an element, including ions AND neutrals.

    CAUTION: some code assumes (without checking) that Element objects are immutable.
        Changing an Element after creating it could lead to unexpected behavior.
    
    name: None or str
        name of this element. None --> name unknown.
        defaults assume names will be title-case element symbol, e.g. 'H', 'He';
            using different names is allowed but will prevent default lookups.
    i: None or int
        index of this element (within an ElementList). None --> index unknown.
    m: None or number
        mass, in atomic mass units. E.g., ~1 for H.
    ionize_ev: None or number
        first ionization potential [eV]. E.g., ~13.6 for H.
    saha_g1g0: None or number
        ratio of g (degeneracy of states) for g1 (ions) to g0 (neutrals). E.g., 0.5 for H.
    abundance: None or number
        abundance of this element relative to H:
            A(elem) = 12 + log10(n(elem) / n(H)), n = number density.
        if not provided, trying to get abundance-related quantities will crash.

    internally, q=None always, because elements have no charge info.
    '''
    # attrs "defining" this DimensionValue, & which can be provided as kwargs in __init__
    _kw_def = {'name', 'i', 'm', 'ionize_ev', 'saha_g1g0', 'abundance'}

    def __init__(self, name=None, i=None, *, m=None,
                 ionize_ev=None, saha_g1g0=None, abundance=None, **other_info):
        super().__init__(name=name, i=i, m=m, **other_info)
        self.ionize_ev = ionize_ev
        self.saha_g1g0 = saha_g1g0
        self.abundance = abundance

    element = property(identity,
        doc='''alias to self. because self (an Element) is the element corresponding to self.''')

    # # # ABUNDANCE STUFF # # #
    def n_per_nH(self):
        '''return n(elem)/n(H) for this element. n = number density'''
        return 10**(self.abundance - 12)
    def r_per_nH(self):
        '''return r(elem)/n(H) for this element. r = mass density'''
        return self.m * self.n_per_nH()

    # # # DISPLAY # # #
    def __repr__(self):
        contents = [repr(val) for val in [self.name, self.i] if val is not None]
        if self.m is not None:
            contents.append(f'm={self.m:.3f}')
        if self.q is not None:  # <-- expect q=None always, though...
            contents.append(f'q={self.q}')
        if self.ionize_ev is not None:
            contents.append(f'ionize_ev={self.ionize_ev:.1f}')
        if self.saha_g1g0 is not None:
            contents.append(f'saha_g1g0={self.saha_g1g0:.1f}')
        if self.abundance is not None:
            contents.append(f'abundance={self.abundance:.1f}')
        return f'{type(self).__name__}({", ".join(contents)})'


class ElementList(ElementHaverList):
    '''List of Element objects.
    
    cls.DEFAULTS provides defaults for infotypes: 'm', 'ionize_ev', 'saha_g1g0', 'abundance'
        dict of {infotype: {defaultname: {elementname: value of this infotype}}}
        e.g. {'m': {'physical': {'H': 1, 'He': 4}},
              'ionize_ev': {'physical': {'H': 13.6, 'He': 24.6}},
              'saha_g1g0': {'physical': {'H': 0.5, 'He': 2.0}},
              'abundance': {'photospheric_v0': {'H': 12, 'He': 10.93},
                            'photospheric_v1': {'H': 12, 'He': 11.00}}
        the default for 'physical' for m and ionize_ev are in PlasmaCalcs.DEFAULTS.

    defaults assume names will be title-case element symbol, e.g. 'H', 'He';
        using different names is allowed but will prevent default lookups.
    '''
    value_type = Element

    DEFAULTS = {
        'm':         {'physical': DEFAULTS.PHYSICAL.M_AMU},
        'ionize_ev': {'physical': DEFAULTS.PHYSICAL.IONIZE_EV},
        'saha_g1g0': {'physical': DEFAULTS.PHYSICAL.SAHA_G1G0},
        'abundance': {},
        }

    ionize_ev = elementwise_property('ionize_ev')
    saha_g1g0 = elementwise_property('saha_g1g0')
    abundance = elementwise_property('abundance')

    # # # CREATION OPTIONS # # #
    @classmethod
    def from_names(cls, names=None, *names_as_args,
                   m='physical', ionize_ev='physical', saha_g1g0='physical', abundance={},
                   missing_ok=True, **common_info):
        '''create ElementList from names and dicts of info about each element.

        names: None or list of str
            names of elements.
            None --> use keys of other dicts.
            list --> use these names in this order.
            defaults assume names will be title-case element symbol, e.g. 'H', 'He';
                using different names is allowed but will prevent default lookups.
        names_as_args: additional names
            only allowed if names is a string; can list extra strings here.
            from_dicts('H', 'He', ...) equivalent to from_dicts(['H', 'He', ...]).
        m: str or dict
            masses of elements, in atomic mass units. E.g., {'H': 1}.
            str --> use cls.DEFAULTS['m'][m].
        ionize_ev: str or dict
            first ionization potentials of elements [eV]. E.g., {'H': 13.6}.
            str --> use cls.DEFAULTS['ionize_ev'][ionize_ev]
        saha_g1g0: str or dict
            ratio of g (degeneracy of states) for g1 (ions) to g0 (neutrals). E.g., {'H': 0.5}.
            str --> use cls.DEFAULTS['saha_g1g0'][saha_g1g0]
        abundance: str or dict
            abundances of elements relative to H. E.g., {'H': 12}.
            A(elem) = 12 + log10(n(elem) / n(H)), n = number density.
            str --> use cls.DEFAULTS['abundance'][abundance]
        missing_ok: bool
            whether to allow missing values for m, ionize_ev, or abundance.
            if False, missing values (i.e., None) will cause crash with FluidKeyError.
        additional kwargs passed to Element.__init__ for every element.
        '''
        # bookkeeping
        if isinstance(m, str):
            m = cls.DEFAULTS['m'][m]
        if isinstance(ionize_ev, str):
            ionize_ev = cls.DEFAULTS['ionize_ev'][ionize_ev]
        if isinstance(saha_g1g0, str):
            saha_g1g0 = cls.DEFAULTS['saha_g1g0'][saha_g1g0]
        if isinstance(abundance, str):
            abundance = cls.DEFAULTS['abundance'][abundance]
        if len(names_as_args) > 0:
            if not isinstance(names, str):
                raise InputConflictError('names_as_args only allowed if names is a string')
        if names is None:  # names = set union of all other keys, but maintain ordering.
            names = list(m.keys())
            names.extend(k for k in ionize_ev if k not in names)
            names.extend(k for k in abundance if k not in names)
        elif isinstance(names, str):
            names = [names]
            names.extend(names_as_args)
        # getting info for each Element
        infos = []
        for name in names:
            info = {
                'name': name,
                'm': m.get(name, None),
                'ionize_ev': ionize_ev.get(name, None),
                'saha_g1g0': saha_g1g0.get(name, None),
                'abundance': abundance.get(name, None),
            }
            if not missing_ok:
                for k in ('m', 'ionize_ev', 'saha_g1g0', 'abundance'):
                    if info[k] is None:
                        raise FluidKeyError(f'{k}.get({name!r}, None) is None, when missing_ok=False')
            infos.append(info)
        # create & return ElementList
        return cls.from_infos(infos, **common_info)

    @classmethod
    def register_default(cls, infotype, defaultname, element2value):
        '''register a default lookup table for an infotype.
        e.g. cls.register_default('abundance', 'photospheric_v0', {'H': 12, 'He': 10.93})
        '''
        cls.DEFAULTS[infotype][defaultname] = element2value

    # [TODO] option to make ElementList with subset of elements but adjust abundances to get same total n.

    # # # ABUNDANCE STUFF # # #
    def n_per_nH(self, elem=None):
        '''n(elem)/n(H) for self.get(elem) (all elems in self if None).'''
        ee = self.get(elem)
        return 10**(ee.abundance - 12)
    def r_per_nH(self, elem=None):
        '''r(elem)/n(H) for self.get(elem) (all elems in self if None).'''
        ee = self.get(elem)
        return ee.m * ee.n_per_nH()

    def ntot_per_nH(self):
        '''sum(n(elem)/n(H)) == n(total)/n(H). Summed across all elems in self.'''
        return sum(self.n_per_nH())
    def rtot_per_nH(self):
        '''sum(r(elem)/n(H)) == r(total)/n(H). Summed across all elems in self.'''
        return sum(self.r_per_nH())

    def n_per_ntot(self, elem=None):
        '''n(elem)/n(total) for self.get(elem) (all elems in self if None).'''
        return self.n_per_nH(elem) / self.ntot_per_nH()
    def r_per_rtot(self, elem=None):
        '''r(elem)/r(total) for self.get(elem) (all elems in self if None).'''
        return self.r_per_nH(elem) / self.rtot_per_nH()

    def mtot(self):
        '''return "average" mass of all elements in self, weighted by n (implied by abundances).
        mtot = sum_x(mx ax) / sum_x(ax), where ax = nx / nH, and x is an element in self.

        Note: mtot = rtot / ntot. This can be proven as follows:
            rtot = sum_x(rx) = sum_x(mx nx) = sum_x(mx ax nH) = sum_x(mx ax) nH
            ntot = sum_x(nx) = sum_x(ax nH) = sum_x(ax) nH
            --> rtot / ntot = sum_x(mx ax) / sum_x(ax)
        (note: ntot does not include electrons)
        '''
        mx = self.m
        ax = self.n_per_nH()
        return sum(mx * ax) / sum(ax)


''' --------------------- Update stuff about ElementHaver class(es) --------------------- '''

ElementHaverList.element_list_cls = ElementList
