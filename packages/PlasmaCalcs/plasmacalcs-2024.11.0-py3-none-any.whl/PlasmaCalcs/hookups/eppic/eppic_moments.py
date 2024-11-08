"""
File Purpose: reading moments for EppicCalculator.
"""
import re

import xarray as xr

from .eppic_io_tools import read_moments_out_files
from ...dimensions import MISSING_SNAP
from ...errors import LoadingNotImplementedError, ValueLoadingError, InputError
from ...quantities import QuantityLoader
from ...tools import simple_setdefaultvia_property, UNSET
from ...defaults import DEFAULTS


class EppicMomentsLoader(QuantityLoader):
    '''moments (from moments*.out files) from Eppic outputs.'''

    # # # MOMENTS FROM FILE # # #
    @known_var(dims=['snap', 'fluid', 'component'])
    def get_moment1(self):
        '''1st moment of distribution function, along an axis (vector component). Mean.
        directly from moments*.out files (multiplied by units conversion factor).
        Compare with 'nmean_u' (which is equivalent to 'mean_(n*u)/mean_n').
            (nmean instead of mean, because moments.out averages across all particles!
            u is the value averaged across all particles in each cell,
            and mean_u averages u across all cells, using an equal weight for each cell.
            so mean_u gives less weight to particles in denser cells, unlike nmean_u and moments.out.)
        '''
        def moment1_loader():  # implicity loads across snap (see _load_moment).
            __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
            return self._load_moment('moment1') * self.u('speed')**1
        result = self.load_across_dims(moment1_loader, dims=['fluid', 'component'])
        return self.record_units(result)

    @known_var(dims=['snap', 'fluid', 'component'])
    def get_moment2(self):
        '''2nd moment of distribution function, along an axis (vector component). Variance.
        directly from moments*.out files (multiplied by units conversion factor).
        Compare with 'nmean_(vsqr-(nmean_u)**2)'.
            (nmean instead of mean, because moments.out averages across all particles!
            vsqr is the value averaged across all particles in each cell,
            and mean_vsqr averages vsqr across all cells, using an equal weight for each cell.
            So, mean_vsqr gives less weight to particles in denser cells, unlike nmean_vsqr and moments.out.)
        '''
        def moment2_loader():  # implicity loads across snap (see _load_moment).
            __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
            return self._load_moment('moment2') * self.u('speed')**2
        result = self.load_across_dims(moment2_loader, dims=['fluid', 'component'])
        return self.record_units(result)

    @known_var(dims=['snap', 'fluid', 'component'])
    def get_moment3(self):
        '''3rd moment of distribution function, along an axis (vector component).
        directly from moments*.out files (multiplied by units conversion factor).
        '''
        def moment3_loader():  # implicity loads across snap (see _load_moment).
            __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
            return self._load_moment('moment3') * self.u('speed')**3
        result = self.load_across_dims(moment3_loader, dims=['fluid', 'component'])
        return self.record_units(result)

    @known_var(dims=['snap', 'fluid', 'component'])
    def get_moment4(self):
        '''4th moment of distribution function, along an axis (vector component).
        directly from moments*.out files (multiplied by units conversion factor).
        '''
        def moment4_loader():  # implicity loads across snap (see _load_moment).
            __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
            return self._load_moment('moment4') * self.u('speed')**4
        result = self.load_across_dims(moment4_loader, dims=['fluid', 'component'])
        return self.record_units(result)

    input_moments = simple_setdefaultvia_property('_input_moments', '_read_all_moments',
        doc=r'''moments from domain000/moments*.out files.
        Can be read using PlasmaCalcs architecture by reading vars:
            moment1, moment2, moment3, moment4.
        These are sensitive to self.component and self.fluid.
        To get moments values directly from file, without helpful xarray labeling,
            use the "eppic_var" versions, which look like:
            'moment{i}{x}{N}' (e.g. 'moment3x0'), where
                i=1,2,3,4 is the moment number,
                x='x','y','z' is the component,
                N=0,1,2,... is the fluid number (i.e., distribution number).
        That is similar to getting, e.g., 'fluxx1'; it gives a value directly from file.

        [EFF] for efficiency, input moments are only read from file one time, then cached.
            You can remove the cached values by doing: del self.input_moments.''')

    def _read_all_moments(self):
        '''read all moments; return result. See help(type(self).input_moments) for more details.'''
        return read_moments_out_files(self.input_deck.dirname)

    def _loadable_moments(self):
        '''tells eppic_var variable names of loadable moments.'''
        moments = self.input_moments
        dists = list(moments.keys())
        # note - the next line assumes all 4*3 moments exist in each file:
        return [f'moment{i}{x}{N}' for i in (1,2,3,4) for N in dists for x in 'xyz']

    def _load_moment(self, eppic_var, *args__None, snap=UNSET, **kw__None):
        r'''load moment indicated by eppic_var. (e.g. 'moment3x0' --> moment 3, component x, fluid 0).
        Units will be the same units as the moments.out files (raw units).
        
        eppic_var: str
            should match full_pattern='moment([1234])([xyz])(\d+)', or partial_pattern='moment([1234])'
            matches full_pattern -->
                ([1234]) indices moment number (1,2,3,4),
                ([xyz]) indicates component (x, y, z),
                (\d+) indicates distribution number (any integer).
            matches partial_pattern --> 
                try to match full_pattern using eppic_var=self._var_dimmed(eppic_var) instead.
                (_var_dimmed appends x and N, if self._loading_component & self._loading_fluid)
            match not found -->
                raise LoadingNotImplementedError
            match found but no associated value in moments data -->
                raise ValueLoadingError
        snap: UNSET, None, or any indicator of any number of snaps
            if provided, return value at this snap, else return value at self.snap.
            if snap indicates multiple values, result will be a list of values.
        '''
        full_pattern = r'moment([1234])([xyz])(\d+)'  # e.g. 'moment3x0'
        match = re.fullmatch(full_pattern, eppic_var)
        if match is None:
            partial_match = re.fullmatch(r'moment([1234])', eppic_var)
            if partial_match:
                var_dimmed = self._var_dimmed(eppic_var)
                match = re.fullmatch(full_pattern, var_dimmed)
            if match is None:
                raise LoadingNotImplementedError(f'var={eppic_var!r} not recognized by _load_moment')
        else:
            var_dimmed = eppic_var
        momi, x, N = match.groups()

        # [TODO] if moments is refactored to be more object-oriented, the code here can be cleaned up a bit.
        moments = self.input_moments
        momname = {'1': 'Mean', '2': 'Variance', '3': 'Moment3', '4': 'Moment4'}[momi]
        momkey = f'V{x}_{momname}'
        try:
            momvals = moments[N][momkey]
        except KeyError:
            raise ValueLoadingError(f'{var_dimmed!r} not found in moments data') from None
        kw_snap = dict() if snap is UNSET else dict(snap=snap)
        with self.using(**kw_snap):
            if self.snap_is_iterable():
                result = [(momvals[int(s.file_s(self))] if s.exists_for(self) else self.snap_dim.NAN) for s in self.snap]
                result = xr.DataArray(result, dims=['snap'], attrs=dict(units='raw'))  # moments file uses raw units
                result = self.assign_snap_along(result, 'snap')
            else:
                result = momvals[int(self.snap.file_s(self))] if self.snap.exists_for(self) else self.snap_dim.NAN
                result = xr.DataArray(result, attrs=dict(units='raw'))  # moments file uses raw units
                result = self.assign_snap_coord(result)
        return result

    # # # TEMPERATURES # # #
    @known_pattern(r'Ta(joule)?_from_moment2', deps=['m', 'moment2'])
    def get_Ta_from_moment2_or_Tajoule_from_moment2(self, var, *, _match=None):
        '''temperature ("anisotropic"), from moment2 instead of nvsqr/n.
        'Ta_from_moment2'      --> (m * moment2 / kB) [Kelvin]
        'Tajoule_from_moment2' --> (m * moment2)      [energy units]
        Compare with nmean_Ta (or nmean_Tajoule).
            nmean instead of mean because moments.out averages across all particles!
            (see help(self.get_moment2) for more details.)
        '''
        here, = _match.groups()
        result = self('m') * self('moment2')
        if here != 'joule':  # Ta, not Tajoule
            result = result / self.u('kB')
        return result

    @known_pattern(r'T(joule)?_from_moment2',
                   deps=[lambda ql, var, groups: f"Ta{groups[0] or ''}_from_moment2"])
    def get_T_from_moment2_or_Tjoule_from_moment2(self, var, *, _match=None):
        '''temperature ("isotropic/maxwellian"), from moment2 instead of nvsqr/n.
        'T_from_moment2' --> mean of Ta_from_moment2 across components.
            == (m * moment2 / kB) [Kelvin], averaged across components.
        'Tjoule_from_moment2' --> similar, but don't divide by kB; result has [energy units].
        '''
        with self.using(component=None):
            return self('Ta_from_moment2').mean('component')

    @known_var(deps=['rmscomps_Ta_from_moment2'], ignores_dims=['component'])
    def get_T_box(self):
        '''temperature of the entire simulation box, as if full of particles,
        and observed by something that could not resolve the individual cells.
        Equivalent: rmscomps(Ta_from_moment2).

        Ignores Ta components for directions in which the box has no extent.
        '''
        return self('rmscomps_Ta_from_moment2', component=self.maindims)
