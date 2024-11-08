"""
File Purpose: EppicSimInfoLoader
loading details about the simulation, not necessarily physics-based.
"""

import numpy as np
import xarray as xr

from .eppic_io_tools import n_mpi_processors
from ...errors import FluidKeyError
from ...quantities import QuantityLoader
from ...tools import (
    product,
    n_slurm_nodes,
)

class EppicSimInfoLoader(QuantityLoader):
    '''simulation info for EppicCalculator.
    These are details about the simulation, not necessarily physics-based.
    E.g., number of particles per simulation cell, number of MPI processors used, simulation dx.

    (note that dx between cells in the output is actually dx_sim * nout_avg,
        since nout_avg is used to average over a few cells in space before providing the output.)
    '''
    # # # LOGIC / PROPERTIES / HELPER METHODS # # #
    def n_processors(self):
        '''return the number of MPI processors used.'''
        return n_mpi_processors(self.dirname)

    def n_nodes(self):
        '''return the number of nodes used. n_processors = n_nodes * (n processors per node).
        (the implementation here assumes slurm. [TODO] support other architecture, such as PBS.)
        '''
        return n_slurm_nodes(self.dirname)

    def ncells_sim(self):
        '''return the number of gridcells from the simulation (differs from output when nout_avg != 1).'''
        nout_avg = self.input_deck['nout_avg']
        ncellsx = [self.input_deck.get_nspace(x)*nout_avg for x in self.maindims]
        return product(ncellsx)

    def npd_for_fluid(self, fluid):
        '''return the npd for this fluid.
        This is equivalent to fluid['npd'] when it is provided,
            otherwise determined by the appropriate alternative (npcelld, nptotd, or nptotcelld).
        This method is implemented for the calculator rather than the fluid, 
            because fluid doesn't know the possibly-required global values (ncells and/or n_processors).

        result will always be converted to int, since npd is an integer.
        '''
        key = None
        for key in ('npd', 'npcelld', 'nptotd', 'nptotcelld'):
            if key in fluid.keys():
                break
        else:  # didn't break
            raise FluidKeyError(f'fluid {fluid} does not have npd, npcelld, nptotd, or nptotcelld.')
        if key == 'npd':
            return int(fluid['npd'])
        elif key == 'npcelld':
            return int(fluid['npcelld'] * self.ncells_sim())
        elif key == 'nptotd':
            return int(fluid['nptotd'] / self.n_processors())
        elif key == 'nptotcelld':
            return int(fluid['nptotcelld'] * self.ncells_sim() / self.n_processors())
        else:
            assert False, "coding error if reached this line"

    # # # LOADABLE QUANTITIES -- SPACE & TIME # # #
    @known_var
    def get_n_processors(self):
        '''number of processors used to run this run. Equivalent value to self.n_processors().'''
        return xr.DataArray(self.n_processors())

    @known_var
    def get_n_nodes(self):
        '''number of nodes used to run this run. Equivalent value to self.n_nodes().'''
        return xr.DataArray(self.n_nodes())

    @known_var(deps=['n_processors', 'n_nodes'])
    def get_tasks_per_node(self):
        '''number of processors per node.'''
        return self('n_processors') / self('n_nodes')

    @known_var
    def get_ncells_sim(self):
        '''number of gridcells from simulation (differs from output when nout_avg != 1).'''
        return xr.DataArray(self.ncells_sim())

    @known_var(load_across_dims=['component'])
    def get_ds_sim(self):
        '''grid spacing (of simulation). vector(ds), e.g. [dx, dy, dz]. Depends on self.component.
        ds_sim = (dx, dy, dz) from input deck (not divided by nout_avg)
        '''
        x = str(self.component)
        dx = self.input_deck[f'd{x}'] * self.u('length')
        return xr.DataArray(dx, attrs=dict(units=self.units))

    @known_var
    def get_dt_sim(self):
        '''time spacing (of simulation). Time between iterations (not between snapshots)'''
        return xr.DataArray(self.input_deck['dt'], attrs=dict(units=self.units))

    
    # # # LOADABLE QUANTITIES -- PARTICLES # # #
    @known_var(load_across_dims=['fluid'])
    def get_npd(self):
        '''number of PIC particles in each distribution.
        This is equivalent to fluid['npd'] when it is provided,
            otherwise determined by the appropriate alternative (npcelld, nptotd, or nptotcelld).
        '''
        return xr.DataArray(self.npd_for_fluid(self.fluid))

    @known_var(deps=['npd', 'ncells_sim'])
    def get_npcelld(self):
        '''number of PIC particles per simulation cell.'''
        return self('npd') / self('ncells_sim')

    @known_var(deps=['npd', 'n_processors'])
    def get_nptotd(self):
        '''number of PIC particles (total across all processors).'''
        return self('npd') * self('n_processors')

    @known_var(deps=['npd', 'n_processors', 'ncells_sim'])
    def get_nptotcelld(self):
        '''number of PIC particles per simulation cell (total across all processors).'''
        return self('npd') * self('n_processors') / self('ncells_sim')

    # # # LOADABLE QUANTITIES -- TIME # # #
    @known_var(load_across_dims=['fluid'])
    def get_subcycle(self):
        '''subcycling factor (for each fluid in self.fluid).
        (If subcycle not provided for a distribution, assume it implies subcycle=1).
        '''
        return xr.DataArray(self.fluid.get('subcycle', 1))

    @known_var(load_across_dims=['snap'])
    def get_nit_since_prev(self):
        '''return number of timesteps since previous snapshot in self.
        when determining previous snapshot, ignore any where snap.file_snap(self) is MISSING_SNAP.
        return inf when no previous snap, e.g. at snap=0.
        '''
        snap_here = self.snap  # this will be a single snap thanks to load_across_dims=['snap']
        if not snap_here.exists_for(self):
            return xr.DataArray(self.snap_dim.NAN)
        # get previous existing snap.
        prev_snap_i = self.snaps.index(self.snap) - 1
        while prev_snap_i >= 0:
            prev_snap = self.snaps[prev_snap_i]
            if prev_snap.exists_for(self):
                break
            else:
                prev_snap_i -= 1
        else:  # didn't break; no previous snap found.
            return xr.DataArray(np.inf)
        # <-- at this point, prev_snap is the previous existing snap, and snap_here is the current snap.
        it_here = int(snap_here.file_s(self))
        it_prev = int(prev_snap.file_s(self))
        return xr.DataArray(it_here - it_prev)
