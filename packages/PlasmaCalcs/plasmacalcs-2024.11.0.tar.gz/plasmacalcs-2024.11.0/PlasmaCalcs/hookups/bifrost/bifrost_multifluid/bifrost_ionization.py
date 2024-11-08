"""
File Purpose: ionization-related quantities (e.g. ionization fraction)
This includes an implementation of the saha ionization equation.
"""

import numpy as np
import xarray as xr

from .bifrost_species import Specie
from ..bifrost_elements import Element
from ....dimensions import SINGLE_FLUID
from ....errors import (
    FluidValueError, FluidKeyError,
    InputError, FormulaMissingError,
)
from ....quantities import QuantityLoader
from ....tools import (
    UNSET,
    format_docstring,
    Partition,
)


''' --------------------- Ionization Helper Methods --------------------- '''

_paramdocs_saha = {
    'ne': '''number or array
        number density of electrons.''',
    'T': '''number or array
        temperature.''',
    'xi': '''number
        first ionization potential.''',
    'g1g0': '''number
        ratio of element's g (degeneracy of states) for g1 (ions) to g0 (neutrals).''',
    'u': '''None or UnitsManager
        units to use; determines expected units system for input & output.
        Also will grab relevant physical constants (such as kB) directly from u.
        None --> make new UnitsManager with SI units.''',
    'saha_equation': ''''(n1/n0) = (1/ne) * (2.0 / lde^3) * (g1 / g0) * exp(-xi / (kB * T))
        where the terms are defined as follows:
            T : temperature
            ne: electron number density
            n1: number density of element's once-ionized ions.
            n0: number density of element's neutrals.
            g1: "degeneracy of states" for element's once-ionized ions.
            g0: "degeneracy of states" for element's neutrals.
            xi: element's first ionization energy.
            lde: electron thermal deBroglie wavelength:
                lde^2 = hplanck^2 / (2 pi me kB T)''',
}

# note: saha_n1n0 not used internally... provided for reference / possible convenience.
@format_docstring(**_paramdocs_saha)
def saha_n1n0(*, ne, T, xi, g1g0, u=None):
    '''return (n1/n0) for an element, via saha equation.

    ne: {ne}
    T: {T}
    xi: {xi}
    g1g0: {g1g0}
    u: {u}

    SAHA_EQUATION:
        {saha_equation}
    '''
    if u is None:
        u = UnitsManager()
    # [EFF] calculate (2.0 / lde^3) ignoring T, to avoid extra array multiplications.
    ldebroge_constant = 2.0 / (u('hplanck')**2 / (2 * np.pi * u('me') * u('kB')))**(3/2)
    ldebroge_factor = ldebroge_constant * T**(3/2)
    result = (ldebroge_factor / ne) * (g1g0 * np.exp(-xi / (u('kB') * T)))
    return result


''' --------------------- BifrostIonizationLoader --------------------- '''

class BifrostIonizationLoader(QuantityLoader):
    '''ionization-related quantities (e.g. ionization fraction)
    Includes an implementation of the saha ionization equation.
    [TODO] include more ionization-related quantities, such as rates?
    '''
    @known_var(deps=['T'])
    def get_ldebroge(self):
        '''electron thermal deBroglie wavelength.
        lde^2 = hplanck^2 / (2 pi me kB T)
        '''
        T = self('T')
        const = np.sqrt(self.u('hplanck')**2 / (2 * np.pi * self.u('me') * self.u('kB')))
        return const / np.sqrt(T)

    # # # SAHA IONIZATION EQUATION # # #
    @known_var(deps=['T'], ignores_dims=['fluid'])
    def get_saha_factor_ldebroge(self, *, _T=None):
        '''(2.0 / lde^3) for saha equation. (See help(self.get_saha_n1n0) for full saha equation.)
        [EFF] computed "efficiently", i.e. combine all constants before including T contribution.
        [EFF] for efficiency, can provide (single fluid) T if already known.
        '''
        ldebroge_constant = 2.0 / (self.u('hplanck')**2 / (2 * np.pi * self.u('me') * self.u('kB')))**(3/2)
        T = self('T', fluid=SINGLE_FLUID) if _T is None else _T
        return ldebroge_constant * T**(3/2)

    @known_var(deps=['ne', 'saha_factor_ldebroge'])
    def get_saha_factor_ldebroge_ne(self, *, _T=None):
        '''(ldebroge_factor / ne) for saha equation. (See help(self.get_saha_n1n0) for full saha equation.)
        [EFF] for efficiency, can provide (single fluid) T if already known.
        '''
        return self('saha_factor_ldebroge', _T=_T) / self('ne')

    @known_var(load_across_dims=['fluid'])
    def get_saha_g1g0(self):
        '''ratio of self.fluid element's g (degeneracy of states) for g1 (ions) to g0 (neutrals).'''
        f = self.fluid
        if f is SINGLE_FLUID:
            raise FluidValueError('get_saha_g1g0 requires self.fluid correspond to element(s), not SINGLE_FLUID.')
        elif isinstance(f, (Element, Specie)):
            return xr.DataArray(f.get_element().saha_g1g0)
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_saha_g1g0.')

    @known_var(load_across_dims=['fluid'], aliases=['first_ionization_energy'])
    def get_ionize_energy(self):
        '''self.fluid element's first ionization energy.'''
        f = self.fluid
        if f is SINGLE_FLUID:
            raise FluidValueError('get_ionize_energy requires self.fluid correspond to element(s), not SINGLE_FLUID.')
        elif isinstance(f, (Element, Specie)):
            return xr.DataArray(f.get_element().ionize_ev * self.u('eV'))
        else:
            raise NotImplementedError(f'fluid of type {type(f)} not yet supported for get_ionize_energy.')

    @known_var(deps=['ionize_energy', 'T'])
    def get_saha_factor_exp(self, *, _T=None):
        '''exp(-xi / (kB * T)) for saha equation. (See help(self.get_saha_n1n0) for full saha equation.)
        xi = first ionization energy.
        [EFF] for efficiency, can provide (single fluid) T if already known.
        '''
        T = self('T', fluid=SINGLE_FLUID) if _T is None else _T
        return np.exp(-self('ionize_energy') / (self.u('kB') * T))

    @known_var(deps=['saha_factor_ldebroge_ne', 'saha_g1g0', 'saha_factor_exp'])
    @format_docstring(**_paramdocs_saha, sub_ntab=1)
    def get_saha_n1n0(self):
        '''(n1/n0) for an element, via saha equation:
            {saha_equation}
        '''
        T = self('T', fluid=SINGLE_FLUID)
        f_ldebroge_ne = self('saha_factor_ldebroge_ne', _T=T)
        f_g1g0 = self('saha_g1g0')
        f_exp = self('saha_factor_exp', _T=T)
        return f_ldebroge_ne * f_g1g0 * f_exp

    def _ionfrac_deps(self=UNSET):
        '''returns the list of variables which are used to calculate ionfrac,
        based on self.fluid.
        '''
        if self is UNSET:
            errmsg = ('Cannot determine deps for var="ionfrac" when called as a classmethod. '
                      'ionfrac depends on the present value of self.fluid.')
            raise InputError(errmsg)
        result = set()
        for f in self.fluid_list():
            if f is SINGLE_FLUID:
                result.update(['ne', 'SF_n'])
            elif isinstance(f, (Element, Specie)):
                result.update(['saha_n1n0'])
            else:
                raise NotImplementedError(f'fluid of type {type(f)} not yet supported for ionfrac.')
        return list(result)

    @known_var(deps=[lambda ql, var, groups: ql._ionfrac_deps()], aliases=['ionization_fraction'])
    def get_ionfrac(self):
        '''ionization fraction(s) of element(s) of self.fluid
        if SINGLE_FLUID, return ne / n.
            where ne = electron number density, n = total number density for all elements, excluding electrons.
            assumes quasineutrality, and that only once-ionized ions are relevant --> sum_ions(nion) = ne.
        otherwise, return 1 / (1 + 1/saha_n1n0).
            Equivalent: n1 / (n1 + n0), where n1 & n0 = number density for element's ions (n1) & neutrals (n0).
            assumes only once-ionized ions are relevant (i.e., n0 + n1 = element's total number density).
        '''
        # [TODO] handle: some SINGLE_FLUID, some Element, some Specie, some electron...
        f = self.fluid
        if f is SINGLE_FLUID:
            return self('ne') / self('n')  # <-- SF_n. but we already know self.fluid is SINGLE_FLUID here.
        else:
            # [TODO] some day, might have a better way to calculate ionfrac, but keep saha as an option.
            # in that case, would need to adjust this part of the code to check self's ionfrac mode.
            return 1 / (1 + 1 / self('saha_n1n0'))

    @known_var(deps=['ionfrac', 'n_elem'], aliases=['nII'])
    def get_saha_n1(self):
        '''number density of once-ionized species of element(s) of self.fluid. n1 = n * ionfrac
        see help(self.get_saha_n1n0) and help(self.get_ionfrac) for more details.
        assumes only once-ionized ions are relevant (ignore twice+ ionized ions).
        '''
        return self('ionfrac') * self('n_elem')

    @known_var(deps=['ionfrac', 'n_elem'], aliases=['nI'])
    def get_saha_n0(self):
        '''number density of neutral species of element(s) of self.fluid. n0 = n * (1 - ionfrac)
        see help(self.get_saha_n1n0) and help(self.get_ionfrac) for more details.
        assumes only once-ionized ions are relevant (ignore twice+ ionized ions).
        '''
        return (1 - self('ionfrac')) * self('n_elem')
