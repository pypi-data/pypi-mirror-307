"""
File Purpose: base & simple derived quantities.

The way to load BASE_QUANTS should be defined in hookups,
    as they will depend on the kind of input data being loaded.

The way to load SIMPLE_DERIVED_QUANTS is defined in this file,
    as they depend only on BASE_QUANTS.
    However, they are decently likely to be overwritten, depending on kind of input.
        E.g. Ebysus saves 'r' and 'm', not 'n'.
            Since 'n' is a base quant, EbysusCalculator needs to overwrite it anyways,
                however it will use something like n = r / m, rather than n = number density from file.
            Meanwhile, EbysusCalculator reads 'r' from file, rather than r = n * m.

Other parts of PlasmaCalcs may assume it is possible to load BASE_QUANTS and SIMPLE_DERIVED_QUANTS.
    PlasmaCalcs will fail with LoadingNotImplementedError when the way to load the quant
    hasn't been defined yet, for the kind of input data being loaded.
"""
import numpy as np

from .quantity_loader import QuantityLoader
from ..errors import LoadingNotImplementedError

# -- this dict is purely for documentation purposes, and not used by the code --
BASE_QUANTS = {
    # -- non-plasma quantities --
    'ds': 'vector(spatial scale), e.g. [dx, dy, dz]',
    # -- fluid constant quantities --
    'm': 'mass',    # of a "single particle". for protons, ~= +1 atomic mass unit
    'q': 'charge',  # of a "single particle". for protons, == +1 elementary charge
    'gamma': 'adiabatic index',
    # -- fluid quantities --
    'n': 'number density',
    'u': 'velocity',    # vector quantity (depends on self.component)
    'u_neutral': 'velocity of neutral fluid(s)',   # vector quantity.
    'T': 'temperature', # "maxwellian" temperature (classical T in thermodynamics)
    'nusj': 'collision frequency',  # for a single particle of s to collide with any of j
    # -- global electromagnetic quantities --
    'E': 'electric field',
    'B': 'magnetic field',
}

# -- this dict is purely for documentation purposes, and not used by the code --
SIMPLE_DERIVED_QUANTS = {
    # -- non-E&M quantities --
    'r': 'mass density', 
    'p': 'momentum density',  # note - lowercase
    'P': 'pressure ("isotropic/maxwellian")',      # note - uppercase
    'Tjoule': 'temperature ("isotropic/maxwellian"), in energy units (multipled by kB). Joules if SI units',
    'e': 'energy density',
    'nusn': 'collision frequency with neutrals',  # for a single particle of s to collide with any neutral
    # -- E&M quantities --
    'nq': 'charge density',
    'Jf': 'current density (associated with fluid)',  # per area, e.g. A/m^2
    'J': 'total current density',  # per area, e.g. A/m^2
    'E_un0': 'electric field in the u_neutral=0 frame',
}

class AllBasesLoader(QuantityLoader):
    '''all base quantities.
    The implementation here just raises LoadingNotImplementedError, for all the BASE_QUANTS.

    Subclasses should override these methods to load the quantities as appropriate,
        probably either from a file or from calculations involving other quantities loaded from files.

    See also: BASE_QUANTS
    '''
    # # # NON-PLASMA QUANTITIES # # #
    @known_var
    def get_ds(self):
        '''vector(spatial scale), e.g. [dx, dy, dz]
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('ds')

    # # # FLUID CONSTANT QUANTITIES # # #
    @known_var
    def get_m(self):
        '''mass, of a "single particle". For protons, ~= +1 atomic mass unit.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('m')

    @known_var
    def get_q(self):
        '''charge, of a "single particle". for protons, == +1 elementary charge.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('q')

    @known_var
    def get_gamma(self):
        '''adiabatic index.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('gamma')

    # # # FLUID QUANTITIES # # #
    @known_var
    def get_n(self):
        '''number density.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('n')

    @known_var(dims=['component'])
    def get_u(self):
        '''velocity. vector quantity (result depends on self.component)
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('u')

    @known_var
    def get_T(self):
        '''temperature. "maxwellian" temperature (classical T in thermodynamics).
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('T')

    @known_var
    def get_nusj(self):
        '''collision frequency. for a single particle of s to collide with any of j.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('nusj')

    # # # GLOBAL ELECTROMAGNETIC QUANTITIES # # #
    @known_var
    def get_E(self):
        '''electric field.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('E')

    @known_var
    def get_B(self):
        '''magnetic field.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('B')

    # # # NEUTRAL QUANTITIES # # #
    # (since it's common for plasma codes to treat neutrals in some special way.)
    @known_var(aliases=['m_n'], ignores_dims=['fluid'])
    def get_m_neutral(self):
        '''mass, of a "single neutral particle". For Hydrogen, ~= +1 atomic mass unit.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('m_neutral')

    @known_var(aliases=['n_n'], ignores_dims=['fluid'])
    def get_n_neutral(self):
        '''number density of neutrals.
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('n_neutral')

    @known_var(aliases=['u_n'], dims=['component'], ignores_dims=['fluid'])
    def get_u_neutral(self):
        '''velocity of neutrals. vector quantity (result depends on self.component)
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('u_neutral')

    @known_var(aliases=['T_n'], ignores_dims=['fluid'])
    def get_T_neutral(self):
        '''temperature of neutrals. "maxwellian" temperature (classical T in thermodynamics).
        [Not implemented for this class]
        '''
        raise LoadingNotImplementedError('T_neutral')


class SimpleDerivedLoader(QuantityLoader):
    '''simple quantities derived from the base quantities.
    Subclasses are decently-likely to override these methods, depending on the kind of input,
        because these provide similar information to the base quantities so different kinds of input
        might save these instead of saving base quantities.
        (E.g. Ebysus saves 'r' instead of 'n', so EbysusCalculator
            will override get_r to read from file, and get_n to n = r / m.)

    See also: SIMPLE_DERIVED_QUANTS
    '''
    # # # NON-E&M QUANTITIES # # #
    @known_var(deps=['n', 'm'])
    def get_r(self):
        '''mass density. r = (n * m) = (number density * mass)'''
        return self('n') * self('m')

    @known_var(deps=['u', 'r'])
    def get_p(self):
        '''momentum density. p = (u * r) = (velocity * mass density).'''
        return self('u') * self('r')

    @known_var(deps=['n', 'Tjoule'])
    def get_P(self):
        '''pressure ("isotropic/maxwellian"). P = (n * Tjoule) = (number density * T [energy units])'''
        return self('n') * self('Tjoule')

    @known_var(deps=['T'])
    def get_Tjoule(self):
        '''temperature ("isotropic/maxwellian"), in energy units. Tjoule = kB * T.
        If using SI units, result will be in Joules.
        '''
        return self.u('kB') * self('T')

    @known_var(deps=['gamma', 'P'])
    def get_e(self):
        '''energy density. e = P / (gamma - 1) = pressure / (adiabatic index - 1)'''
        return self('P') / (self('gamma') - 1)

    @known_var(deps=['nusj'], ignores_dims=['jfluid'])
    def get_nusn(self):
        '''collision frequency. for a single particle of s to collide with any neutral.'''
        neutral = self.jfluids.get_neutral()  # if crash, subclass should implement nusn separately.
        with self.using(jfluid=neutral):
            return self('nusj')

    # # # E&M QUANTITIES # # #
    @known_var(deps=['n', 'q'])
    def get_nq(self):
        '''charge density. nq = (n * q) = (number density * charge)'''
        return self('n') * self('q')

    @known_var(deps=['nq', 'u'])
    def get_Jf(self):
        '''current density (associated with fluid). Jf = (nq * u) = (charge density * velocity)
        This is per unit area, e.g. the SI units would be Amperes / meter^2.

        (If self is not a FluidHaver, this will equal the total current density.)
        '''
        return self('nq') * self('u')

    @known_var(deps=['Jf'], ignores_dims=['fluid'])
    def get_J(self):
        '''total current density. J = sum_across_fluids(n*q*u)
        This is per unit area, e.g. the SI units would be Amperes / meter^2.
        '''
        try:
            fluids = self.fluids
        except AttributeError:
            errmsg = f'J, for object of type {type(self)} which has no .fluids attribute'
            raise LoadingNotImplementedError(errmsg) from None
        charged = fluids.charged()  # [EFF] exclude uncharged fluids, for efficiency.
        Jfs = self('Jf', fluid=charged)
        return Jfs.sum('fluid')  # [TODO] handle "only 1 fluid" case?

    @known_var(deps=['E', 'u_n'])
    def get_E_un0(self):
        '''electric field in the u_neutral=0 frame.
        Here, asserts all of self('u_n')==0, then returns self('E').
        if the assertion fails, raise NotImplementedError (expect subclass to handle it).
        '''
        if not np.all(self('u_n', component=None)==0):
            raise NotImplementedError('E_un0 implementation here assumes u_n=0')
        return self('E')
