"""
File Purpose: reading runtime info for EppicCalculator

this is the timing information from the timers.dat file.
"""
import numpy as np
import xarray as xr

from .eppic_io_tools import read_timers_dat
from ...quantities import QuantityLoader
from ...tools import (
    xarray_promote_dim,
)

class EppicRuntimeInfoLoader(QuantityLoader):
    '''runtime info for EppicCalculator.'''
    # # # LOGIC / PROPERTIES / HELPER METHODS # # #
    def timers_dat(self, *, with_snaps=False, as_array=False):
        '''return timers.dat as an xarray.Dataset. (dimension will be named 'it')
        result will have the same units as timers.dat file.

        with_snaps: bool
            if True, attach snap & t coords and promote 'snap' to main dim.
            based on self.snaps (not self.snap)
        as_array: bool
            whether to use xarray.Dataset.to_array() to return a DataArray instead of Dataset.
            if True, vars from Dataset will be concatenated along the new dimension named 'timer'.
        '''
        result = read_timers_dat(self.dirname, as_array=as_array, # [TODO][EFF] use caching if this is slow.
                                fix_snaps=(self.snaps_from=='parallel'))
        if with_snaps:
            existing_snaps = self.existing_snaps()
            result = self.assign_snap_along(result, 'it', existing_snaps)
            result = xarray_promote_dim(result, 'snap')
            if len(existing_snaps) != len(self.snaps):  # some self.snaps refer to MISSING_SNAP
                # fill MISSING_SNAP points with NaN.
                result = result.reindex(snap=self.snaps, fill_value=self.snap_dim.NAN)
                # assign t coords to MISSING_SNAP points  # [TODO][EFF] do something more efficient?
                result = self.assign_snap_along(result, 'snap', self.snaps)
            result = result.drop_vars('it')
        return result

    # # # LOADABLE QUANTITIES -- TIMERS # # #
    @known_var(dims=['snap'])
    def get_timers(self):
        '''timers_dat info as an xarray.Dataset, at snaps in self.snap. see also: 'runtimes'.'''
        result = self.timers_dat(with_snaps=True, as_array=False)
        result = result.sel(snap=np.array(self.snap))
        return result

    @known_var(dims=['snap'])
    def get_runtimes(self):
        '''timers_dat info as an xarray.DataArray, at snaps in self.snap. see also: 'timers'.'''
        result = self.timers_dat(with_snaps=True, as_array=True)
        result = result.sel(snap=np.array(self.snap))
        return result

    @known_var(deps=['timers'])
    def get_run_time(self):
        '''Wall clock runtime for each snap. Same units as timers_dat info.'''
        return self('timers')['Wall Clock']

    @known_var(deps=['timers'])
    def get_write_time(self):
        '''time spent writing output files. Same units as timers_dat info.'''
        return self('timers')['output']

    @known_var(deps=['run_time', 'write_time'])
    def get_calc_time(self):
        '''Wall clock runtime, ignoring time spent writing output files. Same units as timers_dat info.'''
        return self('run_time') - self('write_time')

    @known_pattern(r'(write|calc)_time_frac', deps=['run_time', lambda ql, var, groups: f'{groups[0]}_time'])
    def get_time_frac(self, var, *, _match=None):
        '''fraction of runtime spent on writing or calculating.
            var='write_time_frac' --> fraction of runtime spent writing output files.
            var='calc_time_frac' --> fraction of runtime spent calculating, ignoring write_time.
        '''
        here, = _match.groups()
        return self(f'{here}_time') / self('run_time')

    @known_pattern(r'(run|calc|write)_(timestep|dt)_cost(_f|_nosub|_fnosub|_nosubf)?',
            deps=['nit_since_prev', 'npd',
                lambda ql, var, groups: f'{groups[0]}_time',
                lambda ql, var, groups: 'subcycle' if (groups[2] is not None and 'sub' in groups[2]) else []])
    def get_timestep_cost_or_dt_cost(self, var, *, _match=None):
        '''total cpu time per simulated particle, per timestep (or per dt).
        
        time_cost = (runtime / timestep_or_dt) * (n_processors / total number of particles)
        total number of particles = n_processors * npart.
            Note: n_processors cancels out; time_cost = (runtime / timestep_or_dt) / npart
        timestep_or_dt = one timestep or one dt; see below.
        npart = number of simulated particles, in one processor. Depends on {settings}; see below.

        '{clock}_{time}_cost{settings}'
            E.g. 'run_timestep_cost', 'write_dt_cost_f', 'calc_dt_cost_nosubf'
            {clock} = 'run', 'calc', or 'write'
                tells which clock to use.
                'run' --> 'Wall clock' | 'calc' --> 'Wall Clock - output' | 'write' --> 'output'
            {time} = 'timestep' or 'dt'
                'timestep' --> report result as cost per timestep, regardless of dt.
                'dt'       --> report result as cost per dt (converted to SI units).
            {settings} = '', '_f', '_nosub', '_fnosub', or '_nosubf'
                tells whether to return a separate value for each fluid, and whether to account for subcycling.
                    ''        --> single value. account for subcycling.     npart = self('npd/subcycle').sum('fluid')
                    '_nosub'  --> single value. ignore subcycling.          npart = self('npd').sum('fluid')
                    '_f'      --> per-fluid values. account for subcycling. npart = self('npd/subcycle')
                    '_fnosub' --> per-fluid values. ignore subcycling.      npart = self('npd')
                    '_nosubf' --> same as '_fnosub'; provided for convenience.

                accounting for subcycling means dividing by the subcycling factor,
                because less effort is spent on subcycled distributions.
        '''
        clock, time, settings = _match.groups()
        clock_per_timestep = self(f'{clock}_time') / self('nit_since_prev')
        # get npart
        if settings is None:
            settings = ''
        if 'f' in settings:
            npart = self('npd')
            if 'nosub' not in settings:
                npart = npart / self('subcycle')
        else:
            with self.using(fluid=None):
                npart = self('npd')
                if 'nosub' not in settings:
                    npart = npart / self('subcycle')
                npart = npart.sum(dim='fluid')  # [TODO] does this still work if len(self.fluids)==1?
        result = clock_per_timestep / npart
        if time == 'dt':
            result = self.record_units(result / self.input_deck['dt'])
        elif time == 'timestep':
            pass  # already divided by timestep.
        else:
            raise NotImplementedError(f'coding error, expected time="timestep" or "dt", got {time!r}')
        return result
