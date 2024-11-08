"""
File Purpose: calculating timescales, e.g. timescale from plasma oscillations.
(e.g., useful when trying to pick dt for a simulation)
"""
import numpy as np

from .quantity_loader import QuantityLoader

class TimescalesLoader(QuantityLoader):
    '''timescales, e.g. timescale from wplasma, or from vthermal / dx.
    Spatial scales come from self('ds')
        which must be defined elsewhere (e.g. in the relevant BasesLoader),
        otherwise trying to get the related timescales will cause a crash.
    '''
    # # # HELPERS # # #
    @known_var(deps=['ds'])
    def get_ds_for_timescales(self):
        '''spatial scale used when calculating timescales. vector(ds), e.g. [dx, dy, dz].
        The method here just returns ds. Subclasses might overwrite if they use a different ds for timescales.
        '''
        return self('ds')
    
    @known_var(deps=['ds_for_timescales'])
    def get_dsmin_for_timescales(self):
        '''minimum spatial scale used when calculating timescales. min(ds_for_timescales) across components.'''
        ds_components = self.take_components(self('ds_for_timescales'))
        return min(ds_components)

    # # # TIMESCALES # # #
    @known_var(deps=['wplasma'])
    def get_timescale_wplasma(self):
        '''timescale from plasma oscillations. 2 * pi / wplasma.  (Hz, not rad/s)
        wplasma = sqrt(n q^2 / (m epsilon0)).
        '''
        return 2 * np.pi / self('wplasma')

    @known_var(deps=['gyrof'])
    def get_timescale_gyrof(self):
        '''timescale for cyclotron motion. 2 * pi / gyrof.  (Hz, not rad/s)
        gyrof = |q| |B| / m.
        '''
        return 2 * np.pi / self('gyrof')

    @known_var(deps=['nusn'])
    def get_timescale_nusn(self):
        '''timescale for collisions with neutrals. 1 / nusn.
        nusn = collision frequency of self.fluid with neutrals.
        '''
        return 1 / self('nusn')

    @known_var(deps=['dsmin_for_timescales', 'vthermal'], aliases=['timescale_vth', 'timescale_vthermal'])
    def get_timescale_vtherm(self):
        '''timescale from thermal velocity. dsmin / vthermal.
        vthermal = sqrt(kB T / m).
        '''
        return self('dsmin_for_timescales') / self('vthermal')

    @known_var(deps=['dsmin_for_timescales', 'mod_E', 'mod_B'])
    def get_timescale_EBspeed(self):
        '''timescale from speed using E & B fields. dsmin / (|E| / |B|).'''
        return self('dsmin_for_timescales') / (self('mod_E') / self('mod_B'))
