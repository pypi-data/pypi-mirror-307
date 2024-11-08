"""
File Purpose: loading Bifrost number densities
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
    alias, simple_property,
    UNSET,
    Partition,
    xarray_promote_dim,
)

class BifrostNumberDensityLoader(QuantityLoader):
    '''number density quantities based on Bifrost.'''

    # # # BEHAVIOR ATTRS # # #
    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['n_mode, ne_mode'], plus any behavior_attrs from super().
        '''
        return ['n_mode', 'ne_mode'] + list(getattr(super(), 'behavior_attrs', []))

    n_mode = simple_property('_n_mode', default='best',
        doc='''str. mode for getting number densities.
        Note that you can always calculate n using a specific formula with the appropriate var,
            regardless of n_mode; e.g. n_neq will always load non-equilirbium value.
        Options:
            'best' --> use best mode available, based on fluid:
                    element --> 'elem'
                    electron --> 'neq' if simulation neq enabled, else 'table'.
                    H or He Specie --> 'neq' if simulation neq enabled, else 'saha'
                    other Specie --> 'saha'
            'elem' --> n for Element, from abundances and SINGLE_FLUID r.
            'neq' --> load value directly from file if simulation neq enabled, else crash or NaN.
            'saha' --> n_elem + saha ionization equation, assuming n=0 for twice+ ionized species.
        Note: if ne_mode is not None, override n_mode with ne_mode for electrons.
        Additional options for electrons only (crash or NaN if used for non-electrons):
            'table', 'QN_best', 'QN_neq', 'QN_table'.
        See help(type(self).ne_mode) for more details on electron options.''')
    
    ne_mode = simple_property('_ne_mode', default=None,
        doc='''None or str. mode for getting electron number density.
        None --> use n_mode for electrons instead of ne_mode.
        'best' --> 'neq' if simulation neq enabled, else 'table'.
        'neq' --> load value directly from file if simulation neq enabled, else crash or NaN.
        'table' --> infer from EOS table, using SINGLE_FLUID r and e.
        'QN', 'QN_neq', or 'QN_table' --> sum of qi ni across self.fluids,
                    using 'best', 'neq', or 'table' methods when getting 'ne' for saha equation.''')

    ne_mode_explicit = alias('ne_mode', doc='''explicit ne_mode: ne_mode if not None, else n_mode.''')
    @ne_mode_explicit.getter
    def ne_mode_explicit(self):
        '''return ne_mode if set, else n_mode for electrons.'''
        ne_mode = self.ne_mode
        return self.n_mode if ne_mode is None else ne_mode

    # whether to crash during get_n methods if ntype 'nan'.
    # False --> return NaN for fluid(s) with ntype 'nan', instead of crashing.
    ntype_crash_if_nan = True

    def _get_n_nan(self):
        '''return n when ntype='nan' (or crash if ntype_crash_if_nan = True)'''
        if self.ntype_crash_if_nan:
            errmsg = (f'ntype "nan" for fluid(s): {self.fluid}.\n'
                      'To return NaN instead of crashing, set self.ntype_crash_if_nan=False.')
            raise FormulaMissingError(errmsg)
        # else:
        return xr.DataArray([np.nan for f in self.fluid], dims='fluid', coords={'fluid': self.fluid})

    # # # GENERIC NUMBER DENSITY # # #
    @known_var(deps=[lambda ql, var, groups: ql._n_deps()])
    def get_n(self):
        '''number density. Formula depends on fluid:
        if SINGLE_FLUID, n = (r / m), where
            r is mass density directly from Bifrost snapshot, and
            m is abundance-weighted average particle mass; see help(self.get_m) for details.
        if Element, n = (r / m), where
            r is inferred from abundances combined with SINGLE_FLUID r, and
            m is element particle mass (fluid.m)
        if Specie, n depends on self.n_mode (and possibly self.ne_mode, if electron):
                'best' --> use best mode available based on fluid:
                        element --> 'elem'
                        electron --> 'neq' if available else 'table'
                        H or He Specie --> 'neq' if available else 'saha'
                        other Specie --> 'saha'
                'elem' --> n for Element, from abundances and SINGLE_FLUID r.
                'neq' --> load value directly from file if available, else crash or NaN.
                        neq possibly available in aux:
                            e-     --> 'hionne'
                            H_I    --> sum('n1', 'n2', 'n3', 'n4', 'n5')
                            H_II   --> 'n6'
                            He_I   --> 'nhe1'  (actually, exp('nhe1'); aux stores log values)
                            He_II  --> 'nhe2'  (actually, exp('nhe2'); aux stores log values)
                            He_III --> 'nhe3'  (actually, exp('nhe3'); aux stores log values)
                'table' --> infer from EOS table, using SINGLE_FLUID r and e.
                'saha' --> n from saha ionization equation, assuming n=0 for twice+ ionized species,
                            using self('ne'), self('T'), fluid.saha_g1g0, and fluid.ionize_ev.
            if ne_mode not None, use ne_mode for electrons instead of n_mode.
                electrons not compatible with 'saha' or 'elem'.
                Additional option for electrons only:
                'QN' --> charge-weighted sum of all ion number densities across self.fluids.
            if mode incompatible with any Specie in self.fluid,
                crash or return NaN, depending on self.ntype_crash_if_nan.
        '''
        squeeze_later = not self.fluid_is_iterable()
        part = Partition(self.fluid_list(), self._ntype)
        result = []
        for ntype, flist in part.items():
            with self.using(fluid=flist):
                if ntype == 'SINGLE_FLUID':
                    if len(flist) > 1:
                        raise NotImplementedError('[TODO] get_n with multiple SINGLE_FLUID...')
                    with self.using(fluid=SINGLE_FLUID):
                        result.append(super().get_n().expand_dims('fluid'))
                elif ntype == 'elem':
                    result.append(self('n_elem'))
                elif ntype == 'neq':
                    result.append(self('n_neq'))
                elif ntype == 'saha':
                    result.append(self('n_saha'))
                elif ntype == 'table':
                    result.append(self('ne_fromtable'))
                elif ntype == 'QN_neq':
                    result.append(self('ne_QN', ne_mode='neq'))
                elif ntype == 'QN_table':
                    result.append(self('ne_QN', ne_mode='table'))
                elif ntype == 'nan':
                    result.append(self._get_n_nan())
                else:
                    raise FormulaMissingError(f'ntype unknown: {ntype}')
        result = self.join_fluids(result)
        if squeeze_later:  # single fluid only!
            result = xarray_promote_dim(result, 'fluid').squeeze('fluid')
        else:  # isel back to original order to match self.fluid order.
            result = result.isel(fluid=part.ridx_flat)
        return result

    def _ntype(self, fluid=UNSET):
        '''return ntype for (single) fluid. See help(self.get_n) for details.
        if fluid is UNSET, use self.fluid. Must represent a single fluid.
        result depends on fluid as well as self.n_mode (and ne_mode if electron).

        Possible results (here, mode=ne_mode_explicit for electrons, n_mode for others):
            'SINGLE_FLUID': SINGLE_FLUID fluid
            'elem': Element.
                    Or, Specie when mode='elem' and fluid.element exists.
            'neq': e or H Specie when mode='neq' (regardless of whether simulation neq enabled).
                    Or, e, H, or He Specie when mode='best' or 'neq' and simulation neq enabled.
                    (simulation neq enabled for e and H if params['do_hion']. also for He if 'do_helium')
            'saha': non-electron Specie when mode='saha'.
                    Or, non-electron Specie when mode='best', and simulation neq disabled.
            'table': electron Specie when mode='table'.
                    Or, electron Specie when mode='best', and simulation neq mode disabled.
            'QN_neq': electron Specie when mode='QN_neq'.
                    Or, electron Specie when mode='QN' and simulation neq enabled.
            'QN_table': electron Specie when mode='QN_table'.
                    Or, electron Specie when mode='QN' and simulation neq disabled.
            'nan': none of the above --> don't know how to get n for fluid.

        Will crash if mode unrecognized (ne_mode if electron, n_mode if non-electron Specie.)
        '''
        using = dict() if fluid is UNSET else dict(fluid=fluid)
        with self.using(**using):
            f = self.fluid
            if self.fluid_is_iterable():
                raise FluidValueError(f'_ntype expects single fluid but got iterable: {f}')
            if f is SINGLE_FLUID:
                return 'SINGLE_FLUID'
            elif isinstance(f, Element):
                return 'elem'
            elif isinstance(f, Specie):
                # bookkeeping:
                neq_H = self.params.get('do_hion', False)
                neq_e = neq_H  # if neq_H, also have neq_e.
                neq_He = self.params.get('do_helium', False)
                electron = f.is_electron()
                H = f.element == 'H'
                He = f.element == 'He'
                if electron or H:
                    neq_enabled = self.params.get('do_hion', False)
                elif He:
                    neq_enabled = self.params.get('do_helium', False)
                else:
                    neq_enabled = False
                mode = self.ne_mode_explicit if electron else self.n_mode
                # check if mode recognized:
                if electron:
                    if mode not in ['best', 'neq', 'table', 'QN', 'QN_neq', 'QN_table']:
                        raise InputError(f'ne_mode {mode!r} not recognized for electron fluid: {f}.')
                else:
                    if mode not in ['best', 'elem', 'neq', 'saha']:
                        raise InputError(f'n_mode {mode!r} not recognized for non-electron fluid: {f}.')
                # logic (same order as in docstring. readability is more important than efficiency here.)
                if mode == 'elem' and f.element is not None:
                    return 'elem'
                elif mode == 'neq' and (electron or H):
                    return 'neq'
                elif (mode == 'best' or mode == 'neq') and neq_enabled:
                    return 'neq'
                elif mode == 'saha' and not electron:
                    return 'saha'
                elif mode == 'best' and not electron and not neq_enabled:
                    return 'saha'
                elif electron:
                    if mode == 'table':
                        return 'table'
                    elif mode == 'best' and not neq_enabled:
                        return 'table'
                    elif mode == 'QN_neq':
                        return 'QN_neq'
                    elif mode == 'QN' and neq_enabled:
                        return 'QN_neq'
                    elif mode == 'QN_table':
                        return 'QN_table'
                    elif mode == 'QN' and not neq_enabled:
                        return 'QN_table'
        return 'nan'

    @known_var(load_across_dims=['fluid'])
    def get_ntype(self):
        '''ntype for self.fluid; affects 'n' result, see help(self.get_n) for details.
        The output array will have dtype string.
        '''
        return xr.DataArray(self._ntype())

    def _n_deps(self=UNSET):
        '''returns the list of variables which are used to calculate n, based on self.fluid.'''
        if self is UNSET:
            errmsg = ('Cannot determine deps for var="n" when called as a classmethod. '
                       'n depend on the present value of self.fluid')
            raise InputError(errmsg)
        part = Partition(self.fluid_list(), self._ntype)
        result = set()
        if 'SINGLE_FLUID' in part:
            result.update(['SF_r', 'SF_m'])
        if 'elem' in part:
            result.add('n_elem')
        if 'neq' in part:
            result.add('n_neq')
        if 'saha' in part:
            result.add('n_saha')
        if 'table' in part:
            result.add('ne_fromtable')
        if 'QN_neq' in part:
            result.update(['ne_QN', 'ne_neq'])
        if 'QN_table' in part:
            result.update(['ne_QN', 'ne_fromtable'])
        return list(result)

    # # # SAHA NUMBER DENSITY # # #
    # (details of saha_n0 and saha_n1 are defined in BifrostIonizationLoader)
    @known_var(deps=[lambda ql, var, groups: ql._n_saha_deps()], aliases=['n_saha'])
    def get_n_saha(self):
        '''number density of self.fluid specie(s), based on saha equation.
        neutral --> saha_n0, = n * (1 - ionfrac)
        once-ionized ion --> saha_n1, = n * ionfrac
        twice+ ionized ion --> 0
        SINGLE_FLUID, Element, or electron --> nan
        '''
        squeeze_later = not self.fluid_is_iterable()
        part = Partition(self.fluid_list(), self._ntype_saha)
        result = []
        for ntype, flist in part.items():
            with self.using(fluid=flist):
                if ntype == 'nan':
                    result.append(self._get_n_nan())
                elif ntype == '0':
                    arr_0 = xr.DataArray([0 for f in flist], dims='fluid', coords={'fluid': flist})
                    result.append(arr_0)
                elif ntype == 'saha_n0':  # [TODO][EFF] don't recalculate ionfrac terms for n0 and n1.
                    result.append(self('saha_n0'))
                elif ntype == 'saha_n1':
                    result.append(self('saha_n1'))
                else:
                    raise FormulaMissingError(f'ntype unknown: {ntype}')
        result = self.join_fluids(result)
        if squeeze_later:  # single fluid only!
            result = result.squeeze('fluid')
        else:  # isel back to original order to match self.fluid order.
            result = result.isel(fluid=part.ridx_flat)
        return result

    def _ntype_saha(self, fluid):
        '''return ntype for fluid with nfrom saha.
        SINGLE_FLUID --> 'nan'
        Element --> 'nan'
        Specie -->
            electron --> 'nan'
            neutral --> 'saha_n0'
            once-ionized ion --> 'saha_n1'
            twice+ ionized ion --> '0'
        '''
        if fluid is SINGLE_FLUID:
            return 'nan'
        elif isinstance(fluid, Element):
            return 'nan'
        elif isinstance(fluid, Specie):
            if fluid.is_electron():
                return 'nan'
            elif fluid.is_neutral():
                return 'saha_n0'
            elif fluid.q == 1:
                return 'saha_n1'
            elif fluid.q > 1:
                return '0'
        raise FormulaMissingError(f'saha_ntype for fluid {fluid}')

    def _n_saha_deps(self=UNSET):
        '''returns the list of variables which are used to calculate n_saha,
        based on self.fluid.
        '''
        if self is UNSET:
            errmsg = ('Cannot determine deps for var="n_saha" when called as a classmethod. '
                      'n_saha depends on the present value of self.fluid.')
            raise InputError(errmsg)
        part = Partition(self.fluid_list(), self._ntype_saha)
        result = set()
        if 'saha_n0' in part:
            result.add('saha_n0')
        if 'saha_n1' in part:
            result.add('saha_n1')
        return list(result)

    # # # NON-EQUILIBRIUM NUMBER DENSITY # # #
    @known_var(load_across_dims=['fluid'])
    def get_n_neq(self):
        '''number density of self.fluid specie(s); non-equilibrium values.
        Result depends on fluid:
            electron --> 'hionne'
            'H_I'    --> sum('n1', 'n2', 'n3', 'n4', 'n5')
            'H_II'   --> 'n6'
            'He_I'   --> 'nhe1'  (actually, exp('nhe1'); aux stores log values)
            'He_II'  --> 'nhe2'  (actually, exp('nhe2'); aux stores log values)
            'He_III' --> 'nhe3'  (actually, exp('nhe3'); aux stores log values)
            other --> crash with FormulaMissingError.
        the electron fluid is tested via fluid.is_electron(),
        while the other species are tested via name-matching to the names above.
        '''
        # load_across_dims for this one, instead of grouping via Partition & ntype,
        #   because here we don't expect multiple self.fluid with same formula,
        #   so there's basically no efficiency improvements from grouping.
        f = self.fluid
        if f.is_electron():
            return self('ne_neq')
        elif f == 'H_I':
            n1 = self('load_n1')
            n2 = self('load_n2')
            n3 = self('load_n3')
            n4 = self('load_n4')
            n5 = self('load_n5')
            result_cgs = n1 + n2 + n3 + n4 + n5
            result = result_cgs * self.u('n', convert_from='cgs')
        elif f == 'H_II':
            result = self('load_n6') * self.u('n', convert_from='cgs')
        elif f == 'He_I':
            result = np.exp(self('load_nhe1')) * self.u('n', convert_from='cgs')
        elif f == 'He_II':
            result = np.exp(self('load_nhe2')) * self.u('n', convert_from='cgs')
        elif f == 'He_III':
            result = np.exp(self('load_nhe3')) * self.u('n', convert_from='cgs')
        else:
            raise FormulaMissingError(f'n_neq for fluid {f}.')
        return self.record_units(result)

    # # # ELECTRON NUMBER DENSITY # # #
    def _assign_electron_fluid_coord_if_unambiguous(self, array):
        '''return self.assign_fluid_coord(array, electron fluid).
        if self doesn't have exactly 1 electron fluid, don't assign coord.
        '''
        try:
            electron = self.fluids.get_electron()
        except FluidValueError:
            return array
        # else
        return self.assign_fluid_coord(array, electron, overwrite=True)

    @known_var  # [TODO] deps...
    def get_ne(self):
        '''electron number density.
        method based on self.ne_mode (use self.n_mode if ne_mode is None):
            'best' --> 'neq' if simulation neq enabled, else 'table'
            'neq' --> load value directly from file if simulation neq enabled, else crash or NaN.
            'table' --> infer from EOS table, using SINGLE_FLUID r and e.
            'QN', 'QN_neq', or 'QN_table' --> sum of qi ni across self.fluids,
                    using 'best', 'neq', or 'table' methods when getting 'ne' for saha equation.
        '''
        # bookkeeping
        mode = self.ne_mode_explicit
        if mode == 'QN':
            mode = 'QN_neq' if self.params.get('do_hion', False) else 'QN_table'
        if mode == 'best':
            mode = 'neq' if self.params.get('do_hion', False) else 'table'
        # getting results:
        if mode == 'neq':
            result = self('ne_neq')
        elif mode == 'table':
            result = self('ne_fromtable')
        elif mode == 'QN_neq':
            result = self('ne_QN', ne_mode='neq')
        elif mode == 'QN_table':
            result = self('ne_QN', ne_mode='table')
        else:
            raise InputError(f'ne_mode {mode!r} not recognized.')
        return result

    @known_var(deps=['n', 'q'], ignores_dims=['fluid'])
    def get_ne_QN(self):
        '''electron number density, assuming quasineutrality.
        result is sum_i qi ni / |qe|, with sum across all ions i in self.fluids.
        (Comes from assuming sum_s qs ns = 0, with sum across all species s in self.fluids.)
        '''
        ions = self.fluids.ions()
        if self.ne_mode_explicit in ['QN', 'QN_neq', 'QN_table']:
            ne_mode = self.ne_mode_explicit
            errmsg = (f"cannot get 'ne_QN' when ne_mode (={ne_mode!r}) still implies QN; "
                      "need a non-QN way to get ne to use for saha equation.\n"
                      "Suggest retrying with ne_mode='neq' or ne_mode='table'.")
            raise FormulaMissingError(errmsg)
        ni = self('n', fluid=ions)  # <-- internally, ne for saha comes from neq or table.
        Zi = self('q', fluid=ions) / self.u('qe')  # Zi = qi / |qe|
        result = Zi * ni
        result = xarray_promote_dim(result, 'fluid').sum('fluid')
        return self._assign_electron_fluid_coord_if_unambiguous(result)

    @known_var(deps=['SF_e', 'SF_r'], ignores_dims=['fluid'])
    def get_ne_fromtable(self):
        '''electron number density, from plugging r and e into eos tables (see self.tabin).'''
        result = super().get_ne_fromtable()
        return self._assign_electron_fluid_coord_if_unambiguous(result)

    @known_var(dims=['snap'], ignores_dims=['fluid'])
    def get_ne_neq(self):
        '''electron number density, from 'hionne' in aux.
        hionne in aux is stored in cgs units.
        '''
        result = super().get_ne_neq()
        return self._assign_electron_fluid_coord_if_unambiguous(result)

