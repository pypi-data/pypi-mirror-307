"""
File Purpose: base quantities for BifrostCalculator
"""
import numpy as np

from ...defaults import DEFAULTS
from ...dimensions import SINGLE_FLUID
from ...errors import (
    FluidValueError, FormulaMissingError,
    InputError, InputMissingError,
)
from ...quantities import AllBasesLoader, SimpleDerivedLoader
from ...tools import (
    simple_property, simple_setdefaultvia_property,
    UNSET,
)


''' --------------------- BifrostBasesLoader --------------------- '''

class BifrostBasesLoader(AllBasesLoader, SimpleDerivedLoader):
    '''base quantities based on Bifrost output.'''

    # # # SINGLE FLUID MODE CHECK # # #
    @property
    def in_single_fluid_mode(self):
        '''whether self is in "single fluid mode".
        BifrostCalculator is always in single-fluid mode... but subclass might not be.
        Some vars (bases especially) assume single-fluid mode, so it is good to check.
            E.g. this ensures multifluid subclasses don't do weird things by accident.
        '''
        try:
            return self.fluid is SINGLE_FLUID
        except AttributeError:
            return True

    def assert_single_fluid_mode(self, varname='var'):
        '''asserts that self is in single fluid mode; else crash with FluidValueError.
        varname: str
            name of var to include in error message if crashing.

        Use for operations which directly assume single fluid mode (e.g. get_r implementation here).
        Not necessary for operations which apply regardless of number of fluids,
            E.g. n = r / m for any number of fluids, and B is always independent of fluid.
        If unsure, err on the side of caution and use this function,
            to require multifluid subclass to explicitly handle the situation else crash.
        '''
        if not self.in_single_fluid_mode:
            errmsg = (f'{type(self).__name__} getting {var} requires self.in_single_fluid_mode,\n'
                      f'but got self.fluid={self.fluid} instead of SINGLE_FLUID.')
            raise FluidValueError(errmsg)

    @known_pattern(r'(SF|SINGLE_FLUID)_(.+)', deps=[1])  # SF_{var} or SINGLE_FLUID_{var}
    def get_single_fluid_var(self, var, *, _match=None):
        '''SF_{var} (or SINGLE_FLUID_{var}) --> {var}, definitely in single fluid mode.
        crashes with FluidValueError if not self.in_single_fluid_mode.

        The implementation here just does self.assert_single_fluid_mode(),
            then returns self(var) (var from SF_var or SINGLE_FLUID_var string).
        Subclass might override to also set self.fluid = SINGLE_FLUID.
        '''
        _sf, here, = _match.groups()
        self.assert_single_fluid_mode(here)
        return self(here)
    
    # # # DIRECTLY FROM BIFROST # # #
    @known_var(dims=['snap'])
    def get_r(self):
        '''mass density. (directly from Bifrost)
        assumes single fluid mode, i.e. result corresponds to the single fluid from Bifrost.
        '''
        self.assert_single_fluid_mode('r')
        return self.load_maindims_var_across_dims('r', u='mass_density', dims=['snap'])

    @known_var(dims=['snap', 'component'])
    def get_p(self):
        '''momentum density. (directly from Bifrost)
        assumes single fluid mode, i.e. result corresponds to the single fluid from Bifrost.
        '''
        self.assert_single_fluid_mode('p')
        return self.load_maindims_var_across_dims('p', u='momentum_density', dims=['snap', 'component'])

    @known_var(dims=['snap'])
    def get_e(self):
        '''energy density. (directly from Bifrost)
        Per unit volume, e.g. the SI units would be Joules / meter^3.
        assumes single fluid mode, i.e. result corresponds to the single fluid from Bifrost.
        '''
        self.assert_single_fluid_mode('e')
        return self.load_maindims_var_across_dims('e', u='energy number_density', dims=['snap'])

    @known_var(dims=['snap', 'component'])
    def get_B(self):
        '''magnetic field. (directly from Bifrost)'''
        return self.load_maindims_var_across_dims('b', u='b', dims=['snap', 'component'])

    @known_var
    def get_gamma(self):
        '''adiabatic index. (directly from Bifrost)'''
        return self.params['gamma']

    @known_pattern(r'load_(.+)', dims=['snap'])
    def get_load_direct_maindims_var(self, var, *, _match=None):
        '''load maindims var directly from files.
        var should be name of a Bifrost var, e.g. bifrost_bx.
        Output always uses 'raw' units, regardless of self.units,
            but coords are in self.coords_units (default: same as self.units).
        For available vars see self.directly_loadable_vars()
        '''
        # [TODO][MV] this is more generic than Bifrost and could move elsewhere.
        # [TODO] doesn't currently interact well with other patterns, but it should...
        #       (workaround: use parenthesis e.g. load_tg/m fails but (load_tg)/m is fine)
        here, = _match.groups()
        with self.using(coords_units=self.coords_units, units='raw'):
            result = self.load_maindims_var_across_dims(here, dims=['snap'])
        return result

    # # # DERIVED # # #
    @known_var(deps=['curl_B'])
    def get_J(self):
        '''current density. J = curl(B) / mu0.
        Per unit area, e.g. the SI units would be Amperes / meter^2.
        '''
        curl_B = self('curl_B')
        return curl_B / self.u('mu0')

    @known_var(deps=['p', 'r'])
    def get_u(self):
        '''velocity. u = p / r = (momentum density / mass density)'''
        return self('p') / self('r')

    @known_var(deps=['e', 'r'])
    def get_eperm(self):
        '''internal energy per unit mass. eperm = e / r.'''
        return self('e') / self('r')

    # # # FROM ASSUMED ABUNDANCES # # #
    @known_var
    def get_m(self):
        '''abundance-weighted average fluid particle mass.
        m = self.elements.mtot() * (mass of 1 atomic mass unit).
        The "abundance-weighting" is as follows:
            m = sum_x(mx ax) / sum_x(ax), where ax = nx / nH, and x is any elem from self.elements.
            note: ax is related to abundance Ax via Ax = 12 + log10(ax).
        see help(self.elements.mtot) for more details, including a proof that mtot = rtot / ntot.
        '''
        self.assert_single_fluid_mode('m')
        return self.elements.mtot() * self.u('amu')

    @known_var(deps=['r', 'm'])
    def get_n(self):
        '''number density. n = (r / m) = (mass density / mass)
        (Note: for single-fluid, this excludes electron number density.)
        '''
        r = self('r')
        m = self('m')
        r = self._upcast_if_max_n_requires_float64(r)
        return r / m

    def _max_n_requires_float64(self):
        '''returns whether max supported n, in self.units unit system, is too big for float32.
        max supported n, in SI units, is DEFAULTS.BIFROST_MAX_GUARANTEE_SUPPORT_N_SI.
        crash with ValueError if max supported n is too big for float64 as well.
        without this check (and conversion to float64 if needed), some n values might become inf.
        '''
        max_n = DEFAULTS.BIFROST_MAX_GUARANTEE_SUPPORT_N_SI * self.u('n', convert_from='si')
        if max_n > np.finfo(np.float32).max:
            if max_n > np.finfo(np.float64).max:
                errmsg = (f'cannot guarantee support for DEFAULTS.BIFROST_MAX_GUARANTEE_SUPPORT_N_SI,'
                          f'{DEFAULTS.BIFROST_MAX_GUARANTEE_SUPPORT_N_SI}, even using float64.')
                raise ValueError(errmsg)
            return True
        return False

    def _upcast_if_max_n_requires_float64(self, array):
        '''if max n requires float64, upcast array to float64,
        unless array's dtype was already float64 or larger (in which case, just return array).
        see self._max_n_requires_float64 for details on when max n requires float64.
        '''
        if self._max_n_requires_float64():
            if np.finfo(array.dtype).max < np.finfo(np.float64).max:
                return array.astype(np.float64)
        else:
            return array

    # # # EOS VARIABLES / TABLES # # #
    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['eos_mode'], plus any behavior_attrs from super().
        '''
        return ['eos_mode'] + list(getattr(super(), 'behavior_attrs', []))

    eos_mode = simple_setdefaultvia_property('_eos_mode', 'eos_mode_sim',
            doc='''mode for "Equation of State" related variables (ne, T, P).
            'ideal' --> treat as ideal gas. P = n kB T = (gamma - 1) e, and can't get ne.
            'table' --> plug r and e into tables (see self.tabin) to get ne, T, P.
            'neq' --> non-equilibrium ionization for H (possibly also for He too):
                       ne and T from hionne and hiontg (from aux). P from table, r, and e.''')

    def eos_mode_sim(self):
        '''how simulation handled "Equation of State" related variables (ne, T, P).

        'ideal' --> treated as ideal gas: P = n kB T = (gamma - 1) e.
            ne not available.
        'table' --> plugged into EOS lookup tables (see self.tabin)
            plug r and e into tables to get ne, T, P.
        'neq' --> non-equilibrium ionization for H (possibly also for He too):
            ne and T from hionne and hiontg (from aux). P from table, r, and e.
        '''
        if 'tabinputfile' not in self.params:
            return 'ideal'
        elif self.params.get('do_hion', False):
            return 'neq'
        else:
            return 'table'

    def _eos_var_deps(self=UNSET, var=UNSET):
        '''returns the list of variables which are used to calculate var, based on self.eos_mode.'''
        if self is UNSET:
            errmsg = (f'Cannot determine deps for var={var!r} when called as a classmethod. '
                      f'{var!r} depends on the present value of self.eos_mode.')
            raise InputError(errmsg)
        if var is UNSET:
            raise InputMissingError("_eos_var_deps expects 'var' to be provided, but got var=UNSET.")
        if var not in ('ne', 'T', 'P'):
            raise FormulaMissingError(f"_eos_var_deps for var={var!r}. Expected one of: 'ne', 'T', 'P'.")
        mode = self.eos_mode
        if mode == 'ideal' and var == 'ne':
            raise FormulaMissingError("'ne' when eos_mode='ideal'.")
        elif mode == 'ideal':
            return [f'{var}_ideal']  # e.g. P_ideal
        elif mode == 'table':
            return [f'{var}_fromtable']  # e.g. P_fromtable
        elif mode == 'neq' and var == 'P':
            return ['P_fromtable']  # P still comes from table, in neq case
        elif mode == 'neq':
            return [f'{var}_neq']  # e.g. T_neq
        else:
            raise FormulaMissingError(f"eos_mode={mode!r}. Expected 'ideal', 'table', or 'neq'.")

    @known_var(deps=[lambda ql, var, groups: ql._eos_var_deps(var='ne')])
    def get_ne(self):
        '''electron number density. Depends on self.eos_mode; see help(type(self).eos_mode).
        'ideal' --> cannot get ne. Crash with FormulaMissingError.
        'table' --> ne from plugging r and e into EOS lookup tables (see self.tabin).
        'neq' --> ne from 'hionne' from aux.
        '''
        mode = self.eos_mode
        if mode == 'ideal':
            raise FormulaMissingError("'ne' when eos_mode='ideal'.")
        elif mode == 'table':
            return self('ne_fromtable')
        elif mode == 'neq':
            return self('ne_neq')
        else:
            raise FormulaMissingError(f"eos_mode={mode!r}. Expected 'ideal', 'table', or 'neq'.")

    @known_var(deps=[lambda ql, var, groups: ql._eos_var_deps(var='T')])
    def get_T(self):
        '''temperature. Depends on self.eos_mode; see help(type(self).eos_mode).
        'ideal' --> T from ideal gas law: P_ideal = n kB T_ideal --> T_ideal = P_ideal / (n kB).
        'table' --> T from plugging r and e into EOS lookup tables (see self.tabin).
        'neq' --> T from 'hiontg' from aux.
        '''
        mode = self.eos_mode
        if mode == 'ideal':
            return self('T_ideal')
        elif mode == 'table':
            return self('T_fromtable')
        elif mode == 'neq':
            return self('T_neq')
        else:
            raise FormulaMissingError(f"eos_mode={mode!r}. Expected 'ideal', 'table', or 'neq'.")

    @known_var(deps=[lambda ql, var, groups: ql._eos_var_deps(var='P')])
    def get_P(self):
        '''pressure. Depends on self.eos_mode; see help(type(self).eos_mode).
        'ideal' --> P from ideal gas law: P = (gamma - 1) e.
        'table' --> P from plugging r and e into EOS lookup tables (see self.tabin).
        'neq' --> P from table, r, and e. (Even in neq mode, P still comes from table.)
        '''
        mode = self.eos_mode
        if mode == 'ideal':
            return self('P_ideal')
        elif mode == 'table' or mode == 'neq':
            return self('P_fromtable')
        else:
            raise FormulaMissingError(f"eos_mode={mode!r}. Expected 'ideal', 'table', or 'neq'.")

    # EOS - IDEAL GAS #
    @known_var(deps=['e', 'gamma'])
    def get_P_ideal(self):
        '''pressure (from ideal gas law?) P = (gamma - 1) * e
        [TODO] when is this relation actually true? is it ideal gas law, or something else?
        '''
        return (self('gamma') - 1) * self('e')

    @known_var(deps=['P_ideal', 'n'])
    def get_T_ideal(self):
        '''temperature, assuming ideal gas law. P = n kB T --> T = P / (n kB)'''
        return self('P_ideal') / (self('n') * self.u('kB'))

    # EOS - TABLES #
    def _get_ertab_var_raw(self, var):
        '''get var in 'raw' units, from the eos tables, using single-fluid r and e from self.
        CAUTION: array values use [raw], but coords use [self.coords_units].
        see self.tabin.keys() for var options. gets value via interpolation.
        '''
        table = self.tabin[var]  # <-- in its own line to help with debugging in case of crash.
        with self.using(coords_units=self.coords_units, units='raw'):
            # table values are always in 'raw' units, but result coords are in self.coords_units.
            e = self('SF_e')  # 'SF' - value for SINGLE_FLUID mode.
            r = self('SF_r')
        return table.interp(r=r, e=e)  # [raw] units for values, [self.units] for coords.

    def get_ertab_var(self, var, ustr):
        '''get var in self.units units from the eos tables, using r and e from self.
        see self.tabin.keys() for var options. gets value via interpolation.
        ustr: str
            convert result from raw to self.units by multiplying by self.u(ustr).
        '''
        result = self._get_ertab_var_raw(var) * self.u(ustr)
        return self.record_units(result)

    @known_var(deps=['SF_e', 'SF_r'], aliases=['ne_tab'])
    def get_ne_fromtable(self):
        '''electron number density, from plugging r and e into eos tables (see self.tabin).'''
        return self.get_ertab_var('ne', 'n')

    @known_var(deps=['SF_e', 'SF_r'], aliases=['T_tab'])
    def get_T_fromtable(self):
        '''temperature, from plugging r and e into eos tables (see self.tabin).'''
        return self.get_ertab_var('T', 'temperature')

    @known_var(deps=['SF_e', 'SF_r'], aliases=['P_tab'])
    def get_P_fromtable(self):
        '''pressure, from plugging r and e into eos tables (see self.tabin).'''
        return self.get_ertab_var('P', 'pressure')

    @known_var(deps=['SF_e', 'SF_r'])
    def get_kappaR(self):
        '''Rosseland opacity, from plugging r and e into eos tables (see self.tabin).'''
        return self.get_ertab_var('kappaR', 'opacity')

    # EOS - NEQ #
    @known_var(dims=['snap'])
    def get_ne_neq(self):
        '''electron number density, from 'hionne' in aux.
        hionne in aux is stored in cgs units.
        '''
        ufactor = self.u('n', convert_from='cgs')
        return self.load_maindims_var_across_dims('hionne', u=ufactor, dims=['snap'])

    @known_var(dims=['snap'])
    def get_T_neq(self):
        '''temperature, from 'hiontg' in aux.
        hiontg in aux is stored in [K] units.
        '''
        return self.load_maindims_var_across_dims('hiontg', u='K', dims=['snap'])

    # # # MISC # # #
    @known_var(deps=['ne', 'SF_n'], aliases=['ionization_fraction'])
    def get_ionfrac(self):
        '''ionization fraction. ionfrac = ne / n (from single fluid).
        Assumes quasineutrality, and that only once-ionized ions are relevant.
        '''
        self.assert_single_fluid_mode('ionfrac')
        return self('ne') / self('SF_n')

    # # # NEUTRALS # # #
    @known_var(deps=['SF_T'], aliases=['T_n'])
    def get_T_neutral(self):
        '''temperature of neutrals; T_n = T of SINGLE_FLUID.
        (subclass may implement better T but here T_n equivalent to SF_T.)
        '''
        return self('SF_T')
