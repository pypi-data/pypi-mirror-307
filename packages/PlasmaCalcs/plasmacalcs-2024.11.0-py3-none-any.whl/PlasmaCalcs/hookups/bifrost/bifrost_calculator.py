"""
File Purpose: Bifrost Calculator
"""
import os

import numpy as np

from .bifrost_bases import BifrostBasesLoader
from .bifrost_direct_loader import BifrostDirectLoader
from .bifrost_efield import BifrostEfieldLoader
from .bifrost_io_tools import (
    bifrost_infer_snapname_here,
    read_bifrost_meshfile,
)
from .bifrost_snaps import BifrostSnap, BifrostSnapList
from .bifrost_stagger import BifrostStaggerable
from .bifrost_tables import BifrostTabInputManager
from .bifrost_units import BifrostUnitsManager
from ...errors import (
    FileAmbiguityError, FileContentsError, FileContentsMissingError, FileContentsConflictError,
    DimensionError,
)
from ...plasma_calculator import PlasmaCalculator
from ...tools import (
    alias, simple_property, simple_setdefaultvia_property,
)

class BifrostCalculator(BifrostEfieldLoader, BifrostBasesLoader,
                        BifrostStaggerable,
                        BifrostDirectLoader,
                        PlasmaCalculator):
    '''PlasmaCalculator for Bifrost outputs.

    snapname: None or str
        snapname. Snaps info from snapname_NNN.idl files (which should have param snapname)
        None --> infer; look for files like "*_NNN.idl" in dir. if none, raise FileNotFoundError;
                if 2+ different implied snapnames, raise FileAmbiguityError.
    dir: str
        directory where files are located. Stored as self.dirname = os.path.abspath(dir).
    init_checks: bool
        whether to check some things during init.
        Use False for a small efficiency improvement if you know everything looks correct.
    units: 'si' or 'raw'
        units system for outputs of self. 'raw' for same as bifrost data, 'si' for SI units.
    '''
    def __init__(self, snapname=None, *, dir=os.curdir, init_checks=True, units='si', **kw_super):
        if snapname is None:
            snapname = bifrost_infer_snapname_here(dir)
        self.snapname = snapname
        self.dirname = os.path.abspath(dir)
        self.init_snaps()
        # note: self.u units depends on self.params, so it must go after init_snaps
        self.u = BifrostUnitsManager.from_bifrost_calculator(self, units=units)
        # [EFF] u defined before super() --> super() does not create new UnitsManager u.
        super().__init__(**kw_super)
        self.init_tabin()
        if init_checks:
            self.init_checks()

    title = property(lambda self: os.path.basename(self.dirname),
            doc='''title to help distinguish this calculator from others: basename of directory.''')

    # # # DIMENSIONS SETUP --- SNAPS # # #
    def init_snaps(self):
        '''set self.snaps based on snap files in self.dirname.'''
        self.snaps = BifrostSnapList.from_here(self.snapname, dir=self.dirname)

    # # # PARAMS # # #
    @property
    def params(self):
        '''return the global params shared by all snaps.
        Equivalent to self.snaps.params_global(recalc=False).
        '''
        return self.snaps.params_global(recalc=False)

    # # # BEHAVIOR_ATTRS # # #
    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['flip_z_mesh', 'elements'], plus any behavior_attrs from super().
        '''
        return ['flip_z_mesh', 'elements'] + list(getattr(super(), 'behavior_attrs', []))

    flip_z_mesh = simple_property('_flip_z_mesh', default=True,
            doc='''whether to flip (multiply by -1) the z mesh coordinates relative to meshfile.
            When True, z<0 implies "below photosphere", for solar simulations.''')

    # # # DIMENSIONS SETUP -- MAINDIMS # # #
    @property
    def maindims(self):
        '''return tuple of maindims of self, e.g. ('x', 'y', 'z').
        if self.squeeze_direct, discards dims with size 1.
        '''
        return self._maindims_post_squeeze()  # see BifrostDirectLoader for details.

    def get_maindims_coords(self):
        '''return dict of {'x': xcoords, 'y': ycoords, 'z': zcoords}.
        Units will be whatever is implied by self.coords_units system (default: self.units)
        coords will be sliced according to self.slices, if relevant.
        '''
        maindims = self.maindims  # e.g. ('x', 'y', 'z')
        if (self.meshfile is not None) and os.path.isfile(self.meshfile):
            result = self.load_mesh_coords()
            u_l = self.u('l', self.coords_units)
            result = {x: u_l * result[x] for x in maindims}
            result = self._apply_maindims_slices_to_dict(result)
            return result
        # else, default to np.linspace.
        dx = {x: self.params[f'd{x}'] for x in maindims}
        Nx = {x: self.params[f'm{x}'] for x in maindims}
        result = {x: np.arange(Nx[x]) * dx[x] for x in maindims}
        return result

    @property
    def meshfile(self):
        '''abspath to meshfile, if self.params['meshfile'] exists, else None.'''
        meshfile = self.params.get('meshfile', None)
        if meshfile is not None:
            meshfile = os.path.join(self.dirname, meshfile)
        return meshfile

    def load_mesh_coords(self, *, recalc=False):
        '''return dict of coords and diff (e.g. dx), from meshfile. [raw] units.
        {'x': xcoords, 'y': ycoords, 'z': zcoords, 'dx': dx, 'dy': dy, 'dz': dz}

        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc:
            if self.flip_z_mesh:
                if hasattr(self, '_mesh_coords_flipz'):
                    return self._mesh_coords_flipz
            else:
                if hasattr(self, '_mesh_coords_noflip'):
                    return self._mesh_coords_noflip
        # computing result
        meshfile = self.meshfile
        mesh = read_bifrost_meshfile(meshfile)
        result = {'x': mesh['x'],
                  'y': mesh['y'],
                  'z': mesh['z'],
                  'dx': mesh['x_ddup'],
                  'dy': mesh['y_ddup'],
                  'dz': mesh['z_ddup']}
        if self.flip_z_mesh:
            result['z'] = -result['z']
        # sanity checks
        if mesh['x_size'] != self.params['mx']:
            raise DimensionError(f"x meshfile size ({mesh['x_size']}) != mx param ({self.params['mx']})")
        if mesh['y_size'] != self.params['my']:
            raise DimensionError(f"y meshfile size ({mesh['y_size']}) != my param ({self.params['my']})")
        if mesh['z_size'] != self.params['mz']:
            raise DimensionError(f"z meshfile size ({mesh['z_size']}) != mz param ({self.params['mz']})")
        # caching
        if self.flip_z_mesh:
            self._mesh_coords_flipz = result
        else:
            self._mesh_coords_noflip = result
        return result

    # # # INIT CHECKS # # #
    def init_checks(self):
        '''checks some things:
        should always be true:
            - self.snapname == snapname param value in all snaps.
            - mx, my, and mz are the same for all snapshots

        raise NotImplementedError in any of the following scenarios:
            - boundarychk enabled in any snap (or boundarychkx or boundarychky)
            - do_out_of_eq enabled in any snap
        '''
        params = self.params  # <-- checks require to get global params (from snaps)
        # # SHOULD ALWAYS BE TRUE # #
        # check snapname
        if 'snapname' not in params:
            raise FileContentsConflictError("'snapname' param is not the same for every snap.")
        if params['snapname'] != self.snapname:
            raise FileContentsError("self.snaps 'snapname' is not the same as self.snapname.")
        # check mx, my, mz
        for mx in ('mx', 'my', 'mz'):
            if mx not in params:
                raise FileContentsMissingError(f'{mx!r} param does not have the same value in every snap.')
        # # NOT YET IMPLEMENTED # #
        enabled_not_yet_implemented = ('boundarychk', 'boundarychkx', 'boundarychky',
                                        'do_out_of_eq',
                                        )
        for p in enabled_not_yet_implemented:
            for val in self.snaps.iter_param_values(p, False):
                if val: raise NotImplementedError(f'BifrostCalculator when {p!r} enabled.')
        # # ALL CHECKS PASSED # #
        return True

    # # # INPUT TABLES (self.tabin) # # #
    tabin_cls = BifrostTabInputManager  # class for making tabin during self.init_tabin()

    def init_tabin(self):
        '''initialize self.tabin, a BifrostTabInputManager.'''
        tabinputfile = self.params.get('tabinputfile', None)
        if tabinputfile is None:
            # save self.tabin = error. This will make debugging easier if someone tries to use tabin.
            # But don't crash here; non-tabin stuff can still work just fine without tabin.
            errmsg = "making tabin requires 'tabinputfile' param to exist & match across all snaps"
            self.tabin = FileAmbiguityError(errmsg)
        else:  # tabinputfile exists!
            tabinputfile = os.path.join(self.dirname, tabinputfile)
            self.tabin = self.tabin_cls(tabinputfile, u=self.u)

    # # # ELEMENTS # # #
    elements = simple_setdefaultvia_property('_elements', 'get_tabin_elements',
            doc='''ElementList of elements composing the "single fluid" modeled by Bifrost.
            Only affects postprocessing; can replace with a different ElementList if desired.
            Default: self.tabin.make_element_list(), which is affected by self.params['tabinputfile'].''')

    def get_tabin_elements(self, *, ionize_ev=None):
        '''return ElementList of elements composing the "single fluid" modeled by Bifrost.
        Implied from self.params['tabinputfile'].
        ionize_ev: None, str, or dict
            first ionization potentials of elements [eV]. E.g., {'H': 13.6}.
            str --> use ElementList.DEFAULTS['ionize_ev'][ionize_ev]
            None --> use self.tabin.ionize_ev (default: 'physical')
        '''
        return self.tabin.make_element_list(ionize_ev=ionize_ev)
