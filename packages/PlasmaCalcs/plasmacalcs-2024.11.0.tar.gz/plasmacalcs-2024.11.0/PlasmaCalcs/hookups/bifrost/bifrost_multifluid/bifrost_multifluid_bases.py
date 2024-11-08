"""
File Purpose: base quantities for BifrostMultifluidCalculator
"""
import numpy as np
import xarray as xr

from .bifrost_species import Specie
from ..bifrost_elements import Element
from ..bifrost_bases import BifrostBasesLoader
from ....dimensions import SINGLE_FLUID
from ....errors import (
    InputError, InputMissingError, FormulaMissingError,
    FluidValueError, FluidKeyError,
)
from ....tools import (
    simple_property,
    UNSET,
    format_docstring,
    Partition,
)


class BifrostMultifluidBasesLoader(BifrostBasesLoader):
    '''base quantities based on Bifrost output & inferred fluid.
    if self.fluid is SINGLE_FLUID, results are equivalent to BifrostCalculator results.
    '''
    @known_var(load_across_dims=['fluid'])
    def get_q(self):
        '''charge of fluid particle. fluid.q [converted to self.units] if it exists.
        if fluid.q is None, give nan. If fluid.q does not exist, crash.
        '''
        f = self.fluid
        if hasattr(f, 'q'):
            q = f.q if f.q is None else (f.q * self.u('qe'))
            return xr.DataArray(q, attrs=self.units_meta())
        else:
            raise FormulaMissingError(f'charge q for fluid {f} without fluid.q attribute.')

    @known_var(load_across_dims=['fluid'])
    def get_m(self):
        '''average mass of fluid particle.
        if SINGLE_FLUID, m computed as abundance-weighted average mass:
            m = self.elements.mtot() * (mass of 1 atomic mass unit).
            The "abundance-weighting" is as follows:
                m = sum_x(mx ax) / sum_x(ax), where ax = nx / nH, and x is any elem from self.elements.
                note: ax is related to abundance Ax via Ax = 12 + log10(ax).
            see help(self.elements.mtot) for more details, including a proof that mtot = rtot / ntot.
        if Element or Specie, return fluid.m, converted from [amu] to self.units unit system.
        '''
        f = self.fluid
        if f is SINGLE_FLUID:
            m_amu = super().get_m()
        else:
            m_amu = f.m * self.u('amu')
        return xr.DataArray(m_amu, attrs=dict(units=self.units))

    # # # FROM ELEMENT ABUNDANCES # # #
    @known_var(load_across_dims=['fluid'], aliases=['r_elem_per_rtot'])
    def get_rfrac_elem(self):
        '''mass density of element(s) for self.fluid, divided by total mass density.'''
        f = self.fluid
        if f is SINGLE_FLUID:
            return xr.DataArray(1)
        elif isinstance(f, (Element, Specie)):
            return xr.DataArray(f.get_element().r_per_nH() / self.elements.rtot_per_nH())
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_rfrac_elem')

    @known_var(load_across_dims=['fluid'], aliases=['n_elem_per_ntot'])
    def get_nfrac_elem(self):
        '''number density of element(s) for self.fluid, divided by total number density.'''
        f = self.fluid
        if f is SINGLE_FLUID:
            return xr.DataArray(1)
        elif isinstance(f, (Element, Specie)):
            return xr.DataArray(f.get_element().n_per_nH() / self.elements.ntot_per_nH())
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_nfrac_elem')

    @known_var(deps=['rfrac_elem', 'SF_r'])
    def get_r_elem(self):
        '''mass density of element(s) for self.fluid. r_elem = rfrac_elem * SF_r.'''
        return self('rfrac_elem') * self('SF_r')

    @known_var(deps=['nfrac_elem', 'SF_n'])
    def get_n_elem(self):
        '''number density of element(s) for self.fluid. n_elem = nfrac_elem * SF_n.'''
        return self('nfrac_elem') * self('SF_n')

    # # DENSITIES # #
    # for number densities, see BifrostNumberDensityLoader.
    @known_var(load_across_dims=['fluid'])  # [TODO] deps
    def get_r(self):
        '''mass density.
        if SINGLE_FLUID, r directly from Bifrost;
        if Element, r inferred from SINGLE_FLUID r and abundances;
        if Species, r = n * m.
        '''
        # [TODO] improve efficiency by allowing to group species;
        #    self('n') * self('m') will get a good speedup if group instead of load_across_dims.
        f = self.fluid
        if f is SINGLE_FLUID:
            return super().get_r()
        elif isinstance(f, Element):
            return self('r_elem')
        elif isinstance(f, Specie):
            return self('n') * self('m')
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_r')

    # # # BOOKKEEPING FOR VALUES WHICH ASSUME SINGLE FLUID # # #
    @known_pattern(r'(SF|SINGLE_FLUID)_(.+)',  # SF_{var} or SINGLE_FLUID_{var}
                   deps=[lambda ql, var, groups: ql._single_fluid_var_deps(var=groups[1])],
                   ignores_dims=['fluid'])
    def get_single_fluid_var(self, var, *, _match=None):
        '''SF_{var} (or SINGLE_FLUID_{var}) --> {var} using self.fluid=SINGLE_FLUID.'''
        _sf, here, = _match.groups()
        with self.using(fluid=SINGLE_FLUID):
            result = self(here)
        return result

    def _single_fluid_var_deps(self=UNSET, var=UNSET):
        '''returns the list of variables which are used to calculate var in SINGLE_FLUID mode.
        Temporarily self.fluid=SINGLE_FLUID, computes deps, then restores original self.fluid.
        [TODO] include var in list of deps too. e.g. now SF_r quant_tree shows SF_r but not get_r.
            (however, would need a way to avoid restoring self.fluid when finding var deps...)
        '''
        if self is UNSET:
            errmsg = (f'Cannot determine deps for var={var!r} when called as a classmethod. '
                      f'{var!r} deps depend on whether self.fluid is SINGLE_FLUID.')
            raise InputError(errmsg)
        if var is UNSET:
            raise InputMissingError("_single_fluid_var_deps expects 'var' to be provided, but got var=UNSET.")
        with self.using(fluid=SINGLE_FLUID):
            matched = self.match_var(var)
            result = matched.dep_vars(self)
        return result

    # # # NEUTRALS # # #
    @known_var(deps=['m'], ignores_dims=['fluid'], aliases=['m_n'])
    def get_m_neutral(self):
        '''mass, of a "single neutral particle". Equivalent to self('m') for neutral fluid.
        Only works if self.fluids (or self.jfluids) contains exactly 1 neutral Specie.
        '''
        return self.get_neutral('m')

    @known_var(deps=['n'], ignores_dims=['fluid'], aliases=['n_n'])
    def get_n_neutral(self):
        '''number density of neutral fluid. Equivalent to self('n') for neutral fluid.
        Only works if self.fluids (or self.jfluids) contains exactly 1 neutral Specie.
        '''
        return self.get_neutral('n')

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['assume_un'], plus any behavior_attrs from super().
        '''
        return ['assume_un'] + list(getattr(super(), 'behavior_attrs', []))

    assume_un = simple_property('_assume_un', default=None,
        doc='''None, 'u', or xarray.DataArray to assume for u_neutral.
        value to assume for u_neutral (used when calculating u_neutral or E_un0).
        None --> cannot determine u_n (crash if trying to get it).
        'u' --> assume u_n = self('u'). Maybe reasonable for weakly-ionized plasma.
                in this case, E_un0 = E_u0, i.e. E(u=0 frame) == E(u_n=0 frame).
        xarray.DataArray --> assume these values for u_n.
                Should have 'x', 'y', 'z' components.''')

    @known_var(aliases=['u_n'])
    def get_u_neutral(self):
        '''velocity of neutral fluid. Depends on self.assume_un:
            None --> cannot get value; raise FormulaMissingError.
            'u' --> assume u_n == self('SINGLE_FLUID_u')
            else --> return self.assume_un
        '''
        assume_un = self.assume_un
        if assume_un is None:
            raise FormulaMissingError('u_neutral, when self.assume_un not provided (=None).')
        elif assume_un == 'u':
            return self('SINGLE_FLUID_u')
        else:
            return assume_un  # [TODO] handle assume_un components != self.component
