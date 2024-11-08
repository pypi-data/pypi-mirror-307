"""
File Purpose: units in Bifrost
"""
import numpy as np

from .bifrost_io_tools import read_bifrost_snap_idl
from ...units import UnitsManager, _units_manager_helpstr
from ...tools import format_docstring


''' --------------------- BifrostUnitsManager --------------------- '''

@format_docstring(helpstr=_units_manager_helpstr, sub_ntab=1)
class BifrostUnitsManager(UnitsManager):
    '''units manager with the from_bifrost method,
    which determines all units based on only u_l, u_t, and u_r.

    How to infer electromagnetic units from t, l, and r alone?
        It is possible because 'raw' Bifrost units guarantee mu0 = 1,
            while in 'si', mu0 = 4 * pi * 10^-7 Newtons Ampere^-2
        Internally, this method determines:
            u_M = u_r * u_l**3   # mass
            u_N = u_M * u_l * u_t**-2   # energy (Newtons in SI)
        Amperes units:
            (mu0 [si]) = u_N * u_A**-2 * (mu0 [raw])
            --> u_A = sqrt(u_N * (mu0 [raw]) / (mu0 [si]))
            --> u_A = sqrt(u_N * (1) / (4 * pi * 10^-7))
        Which yields, for charge units:
            u_q = u_A * u_t
        At which point, we have u_l, u_t, u_M, and u_q,
            which is sufficient to infer all other units (aside from K for temperature)

    --- BifrostUnitsManager.help() will print a helpful message: ---
        {helpstr}
    '''
    @classmethod
    def from_bifrost(cls, units='si', *, u_l, u_t, u_r, K=1):
        '''create a BifrostUnitsManager from u_l, u_t and u_r, the SI conversion factors.
        CAUTION: the names u_l, u_t, u_r refer to cgs in Bifrost, but SI in PlasmaCalcs.
        
        units: 'si' or 'raw'
            by default, outputs of the resulting UnitsManager convert to this unit system.
            Can easily change later by setting result.units to a different value.
        u_l: number
            length [si] = u_l * length [raw]
        u_t: number
            time [si] = u_l * time [raw]
        u_r: number
            mass density [si] = u_r * mass density [raw]
        K: number, default 1
            temperature [si] = K * temperature [raw]

        see help(cls) for more details on how the units are inferred.
        '''
        u_M = u_r * u_l**3
        u_N = u_M * u_l * u_t**-2
        u_A = np.sqrt(u_N / (4 * np.pi * 1e-7))
        u_q = u_A * u_t
        return cls(units=units, q=u_q, M=u_M, l=u_l, t=u_t, K=K)

    @classmethod
    def from_bifrost_cgs(cls, units='si', *, ucgs_l, ucgs_t, ucgs_r, K=1):
        '''create a BifrostUnitsManager from ucgs_l, ucgs_t and ucgs_r.

        units: 'si' or 'raw'
            by default, outputs of the resulting UnitsManager convert to this unit system.
            Can easily change later by setting result.units to a different value.
        ucgs_l: number
            length [cgs] = ucgs_l * length [raw]
        ucgs_t: number
            time [cgs] = ucgs_t * time [raw]
        ucgs_r: number
            mass density [cgs] = ucgs_r * mass density [raw]
        K: number, default 1
            temperature [cgs] = K * temperature [raw]

        see help(cls) for more details on how the units are inferred.
        '''
        # length [si]  = u_l    * length [raw]
        # length [cgs] = ucgs_l * length [raw]
        # --> u_l / ucgs_l = length [si] / length [cgs]
        # e.g. length [si] = 1, length [cgs] = 100 --> u_l = ucgs_l * 1e-2
        u_l = ucgs_l * 1e-2
        # s to s... cgs and si use same time units
        u_t = ucgs_t
        # similar logic as for length... but now we have g/cm^3 to kg/m^3,
        # so g to kg gives 10^-3, and cm^-3 to m^-3 gives 10^6
        u_r = ucgs_r * 1e3
        return cls.from_bifrost(units=units, u_l=u_l, u_t=u_t, u_r=u_r)

    @classmethod
    def from_bifrost_calculator(cls, bifrost_calculator, units='si', *, K=1):
        '''create a BifrostUnitsManager from a BifrostCalculator instance.

        bifrost_calculator: BifrostCalculator
            determine units based on this calculator's params: u_l, u_t, and u_r.
            (Assumes all snaps have the same u_l, u_t, and u_r.)
            CAUTION: the names u_l, u_t, u_r refer to cgs in Bifrost, but SI in PlasmaCalcs.
        units: 'si' or 'raw'
            by default, outputs of the resulting UnitsManager convert to this unit system.
            Can easily change later by setting result.units to a different value.
        K: number, default 1
            temperature [si] = K * temperature [raw]

        see help(cls.from_bifrost) for more details on how the units are inferred.
        '''
        params = bifrost_calculator.params
        ucgs_l = params['u_l']
        ucgs_t = params['u_t']
        ucgs_r = params['u_r']
        # length [si]  = u_l    * length [raw]
        # length [cgs] = ucgs_l * length [raw]
        # --> u_l / ucgs_l = length [si] / length [cgs]
        # e.g. length [si] = 1, length [cgs] = 100 --> u_l = ucgs_l * 1e-2
        u_l = ucgs_l * 1e-2
        # s to s... cgs and si use same time units
        u_t = ucgs_t
        # similar logic as for length... but now we have g/cm^3 to kg/m^3,
        # so g to kg gives 10^-3, and cm^-3 to m^-3 gives 10^6
        u_r = ucgs_r * 1e3
        return cls.from_bifrost(units=units, u_l=u_l, u_t=u_t, u_r=u_r)

    @classmethod
    def from_snap_idl(cls, filename, units='si', *, K=1):
        '''create a BifrostUnitsManager from a Bifrost snap's snapname_NNN.idl file.

        filename: str
            path to the snap's IDL file.
        units: 'si' or 'raw'
            by default, outputs of the resulting UnitsManager convert to this unit system.
            Can easily change later by setting result.units to a different value.
        K: number, default 1
            temperature [si] = K * temperature [raw]

        see help(cls.from_bifrost) for more details on how the units are inferred.
        '''
        from .bifrost_io_tools import read_idl_params_file
        params = read_bifrost_snap_idl(filename, eval=True)
        ucgs_l = params['u_l']
        ucgs_t = params['u_t']
        ucgs_r = params['u_r']
        return cls.from_bifrost_cgs(units=units, ucgs_l=ucgs_l, ucgs_t=ucgs_t, ucgs_r=ucgs_r, K=K)

    # # # DISPLAY # # #
    def _repr_show_factors(self):
        '''returns dict of name and conversion factor to si, to include in repr(self).
        Here, include l, t, and r. Also include K if it is not 1.
        '''
        factors = {key: self(key, 'si', 'raw') for key in ('l', 't', 'r', 'K')}
        if factors['K'] == 1:
            del factors['K']
        return factors
