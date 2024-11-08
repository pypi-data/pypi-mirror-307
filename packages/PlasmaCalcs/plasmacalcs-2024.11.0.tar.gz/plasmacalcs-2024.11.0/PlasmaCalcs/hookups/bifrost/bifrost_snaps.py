"""
File Purpose: Dimension values & lists for Bifrost
"""
import os
import re

from .bifrost_io_tools import (
    read_bifrost_snap_idl,
    bifrost_snap_idl_files,
    bifrost_infer_snapname_here,
)
from ...dimensions import Snap, SnapList
from ...errors import FileContentsConflictError, LoadingNotImplementedError
from ...tools import (
    NO_VALUE, UNSET,
    alias_child, alias_key_of, weakref_property_simple,
    DictlikeFromKeysAndGetitem,
)

''' --------------------- BifrostSnap and BifrostSnapList --------------------- '''

class BifrostSnap(DictlikeFromKeysAndGetitem, Snap):
    '''info about a single bifrost snapshot, including label (str) and index (int).

    The "index" should only be meaningful in the context of a SnapList
    The "label" should be the str name for this snapshot
        - unique within context (e.g. there's only one "snapshot 1" in a simulation)
        - easiest to use str int labels (e.g. "snapshot 1" --> label="1")

    s: the label (str) of the snapshot. if None, cannot convert to str.
    i: the "index" (int) of the snapshot (within a SnapList). if None, cannot convert to int.
    t: time at this snapshot ['raw' units]
    params: dict of parameters (e.g. from .idl file) at this snapshot. if None, make empty dict.
    '''
    def __init__(self, s=None, i=None, *, t=None, params=None):
        params = dict() if params is None else params
        super().__init__(s=s, i=i, t=t)
        self.params = params

    @classmethod
    def from_idl_file(cls, filename, *, i=None):
        '''return BifrostSnap based on idl file.
        filename: str.
            file to read from. Like snapname_NNN.idl.
            will use s=NNN as label. E.g. snapname_071.idl --> s='071'.
            snapname determined from file contents (one of the params should be "snapname")
        i: None or int
            index of this snapshot in a SnapList.
        '''
        params = read_bifrost_snap_idl(filename)
        snapname = params['snapname']
        pattern = rf'{snapname}_([0-9]+)[.]idl'
        match = re.fullmatch(pattern, os.path.basename(filename))
        if match is None:
            errmsg = (f'Filename does not match snapname_NNN.idl pattern. '
                      f'snapname={snapname!r} filename={filename!r}')
            raise FileContentsConflictError(errmsg)
        s = match.group(1)
        t = params.get('t', None)
        return cls(s=s, i=i, t=t, params=params)

    # # # GETTING VALUES / ITERATING # # #
    def __getitem__(self, key):
        '''equivalent to self.params[key]'''
        return self.params[key]

    def keys(self):
        '''return tuple of keys of self.params'''
        return tuple(self.params.keys())

    # # # PROPERTIES # # #
    @property
    def snapname(self):
        '''return snapname of this snap: self.params["snapname"]'''
        return self.params['snapname']

    @property
    def filename(self):
        '''return filename of idl file for this snap: snapname_NNN.idl'''
        return f'{self.snapname}_{self.s}.idl'

    # # # VAR PATH MANAGER # # #
    def var_paths_manager(self, calculator):
        '''return BifrostVarPathsManager for this snap.
        calculator: BifrostCalculator. used for snapdir.

        See result.paths
        '''
        return self.var_paths_manager_cls(self, calculator)
        # BifrostSnap.var_paths_manager_cls defined lower in this file.


class BifrostSnapList(SnapList):
    '''list of BifrostSnap objects'''
    value_type = BifrostSnap

    @classmethod
    def from_idl_files(cls, filenames):
        '''return BifrostSnapList based on idl files.
        order within result matches order of filenames.

        filenames: list of str.
            files to read from. Like snapname_NNN.idl.
            will use s=NNN as label. E.g. snapname_071.idl --> s='071'.
            snapname determined from file contents (one of the params should be "snapname")
        '''
        snaps = [BifrostSnap.from_idl_file(f, i=i) for i, f in enumerate(filenames)]
        return cls(snaps)

    @classmethod
    def from_here(cls, snapname=None, *, dir=os.curdir):
        '''return BifrostSnapList from all snapname_NNN.idl files in directory.
        Sorted by snap number.

        snapname: None or str.
            snaplist from matching snapname_NNN.idl files. (NNN can be any integer, doesn't need to be 3 digits.)
            None --> infer; look for files like "*_NNN.idl" in dir;
                    if 0 such files or 2+ different implied snapnames, raise FileAmbiguityError.
        dir: str. directory to search in.
        '''
        if snapname is None: snapname = bifrost_infer_snapname_here(dir)
        filenames = bifrost_snap_idl_files(snapname, dir=dir)
        result = cls.from_idl_files(filenames)
        # quick check that snapname inside idl file 0 matches with idl file snapname.
        # (don't check all of them here because that could be somewhat slow.)
        if len(result) > 0 and result[0]['snapname'] != snapname:
            errmsg = (f'Snapname provided {snapname!r} does not match snapname param inside '
                      f'idl file {result[0].filename!r}: snapname={result[0]["snapname"]!r}')
            raise FileContentsConflictError(errmsg)
        return result

    # # # MISC PROPERTIES # # #
    @property
    def snapname(self):
        '''return snapname of this snaplist: self[0].snapname.
        returns None if no snaps in list.
        '''
        return self[0].snapname if len(self) > 0 else None

    # # # GETTING KEYS & PARAMS # # #
    def keys(self, *, missing_ok=False, recalc=False):
        '''return list of all keys from snaps. Maintains order in which keys appear.

        missing_ok: bool or None
            whether it is okay for snaps to have different keys.
            False --> not okay. If any snap has any different keys, raise FileContentsConflictError.
            True --> okay. If any snap has different keys, add to list of keys.
        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc:
            if hasattr(self, '_keys_same'):  # result of self.keys(missing_ok=False)
                # if this result exists, then missing_ok doesn't matter either way;
                # because it didn't crash we know all the snaps have the same keys.
                return self._keys_same
            elif missing_ok and hasattr(self, '_keys_join'):  # result of self.keys(missing_ok=True)
                return self._keys_join
        # computing result
        result = []
        if len(self) == 0:
            return result
        result = list(self[0].keys())
        result_set = set(result)
        for snap in self[1:]:
            if missing_ok:
                for key in snap.keys():
                    if key not in result:
                        result.append(key)
            else:
                # ensure key set here matches key set in result, else crash.
                snap_key_set = set(snap.keys())
                if snap_key_set != result_set:
                    missing_here = result_set - snap_key_set
                    missing_zero = snap_key_set - result_set
                    errmsg = (f'Some snaps have different keys. '
                              f'Keys in this snap but not snap 0: {missing_here}. '
                              f'Keys in snap 0 but not this snap: {missing_zero}. '
                              f'This snap = {snap}')
                    raise FileContentsConflictError(errmsg)
        # caching
        if missing_ok:
            self._keys_join = result
        else:
            self._keys_same = result
        return result

    def params(self, *, missing_ok=False, recalc=False):
        '''return dict of {key: [list of values of key from all snaps])
        
        missing_ok: bool
            whether it is okay for snaps to have different keys.
            False --> not okay. If any snap has any different keys, raise FileContentsConflictError.
            True --> okay. When key is missing from a snap, use NO_VALUE instead.
        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc:
            if hasattr(self, '_params_same'):  # result of self.params(missing_ok=False)
                # if this result exists, then missing_ok doesn't matter either way;
                # because it didn't crash we know all the snaps have the same keys.
                return self._params_same
            elif hasattr(self, '_params_join') and missing_ok:  # result of self.params(missing_ok=True)
                return self._params_join
        # computing result
        keys = self.keys(missing_ok=missing_ok, recalc=recalc)
        result = dict()
        if missing_ok:
            for key in keys:
                result[key] = [snap.get(key, NO_VALUE) for snap in self]
        else:
            for key in keys:
                result[key] = [snap[key] for snap in self]
        # caching
        if missing_ok:
            self._params_join = result
        else:
            self._params_same = result
        return result

    def keys_shared(self, *, recalc=False):
        '''return list of keys which appear in all snaps. Maintains order in which keys appear.

        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc and hasattr(self, '_keys_shared'):
            return self._keys_shared
        # computing result
        result = []
        if len(self) == 0:
            return result
        result = list(self[0].keys())
        result_set = set(result)
        for snap in self[1:]:
            snap_key_set = set(snap.keys())
            extras_here = result_set - snap_key_set
            for extra in extras_here:
                result.remove(extra)
                result_set.remove(extra)
        # caching
        self._keys_shared = result
        return result

    def params_global(self, *, recalc=False):
        '''return dict of {key: value} for all keys which have the same value in all snaps.

        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc and hasattr(self, '_params_global'):
            return self._params_global
        # computing result
        if len(self) == 0:
            return dict()
        elif len(self) == 1:
            return self[0].params.copy()
        # else len(self) > 1
        keys = self.keys_shared(recalc=recalc)
        keys = list(keys)  # make a copy to avoid directly editing possibly cached result.
        result = {key: self[0][key] for key in keys}
        for snap in self[1:]:
            for key in keys:
                if snap[key] != result[key]:
                    del result[key]
                    keys.remove(key)
        # caching
        self._params_global = result
        return result

    def keys_global(self, *, recalc=False):
        '''return list of keys whose value is the same in all snaps. Maintains order in which keys appear.

        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc and hasattr(self, '_keys_global'):
            return self._keys_global
        # computing result
        keys = self.keys_shared(recalc=recalc)
        keys = list(keys)  # make a copy to avoid directly editing possibly cached result.
        params_global = self.params_global(recalc=recalc)
        keys_shared_set = set(keys)
        keys_global_set = set(params_global.keys())
        keys_remove_set = keys_shared_set - keys_global_set
        for key in keys_remove_set:
            keys.remove(key)
        # caching
        self._keys_global = keys
        return keys

    def keys_varied(self, *, recalc=False):
        '''return list of keys whose value is different in any snap. Maintains order in which keys appear.

        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc and hasattr(self, '_keys_varied'):
            return self._keys_varied
        # computing result
        keys_all = self.keys(missing_ok=True, recalc=recalc)
        keys_global = self.keys_global(recalc=recalc)
        keys_varied = [key for key in keys_all if key not in keys_global]
        # caching
        self._keys_varied = keys_varied
        return keys_varied

    def params_varied(self, *, recalc=False):
        '''return dict of {key: [values from all snaps]) for all params with different values in any snap.
        If any snaps are missing any keys, use NO_VALUE as the value.

        recalc: bool
            whether to, if possible, return cached value (not a copy of it - don't edit directly!)
        '''
        # caching
        if not recalc and hasattr(self, '_params_varied'):
            return self._params_varied
        # computing result
        keys = self.keys_varied(recalc=recalc)
        result = dict()
        for key in keys:  # looping like this makes debugging easier than list comprehension.
            result[key] = [snap.get(key, NO_VALUE) for snap in self]
        # caching
        self._params_varied = result
        return result

    def iter_param_values(self, key, default=UNSET):
        '''iterate over all values of this param from all snaps.
        If value is the same in all snaps, just yield it once then stop.
        If value is missing from all snaps, yield default if provided else crash.

        default: UNSET or any object
            for snaps missing key, yield default if provided else crash.
        '''
        params_global = self.params_global()
        if key in params_global:
            yield params_global[key]
        else:  # key not global
            keys = self.keys()
            if key in keys:  # key exists in at least 1 snap
                for snap in self:
                    if key in snap.keys():
                        yield snap[key]
                    elif default is UNSET:
                        raise FileContentsConflictError(f'key {key!r} missing from snap {snap}')
                    else:
                        yield default
            else:  # key not in any snaps
                if default is UNSET:
                    raise FileContentsConflictError(f'key {key!r} missing from all snaps.')
                else:
                    yield default

    def list_param_values(self, key, default=UNSET):
        '''list all values of this param from all snaps.
        If value is the same in all snaps, return [value]
        If value is missing from all snaps, return [default] if provided else crash.

        default: UNSET or any object
            for snaps missing key, use default if provided else crash.
        '''
        return list(self.iter_param_values(key, default=default))


''' --------------------- BifrostVarPathsManager --------------------- '''

class BifrostVarPathsManager():
    '''manages filepaths (as abspaths) and readable vars for a BifrostSnap.
    self.kind2path = {kind: path}
    self.kind2vars = {kind: [list of readable vars]}
    self.var2kind = {var: kind}
    self.var2path = {var: path}
    self.path2kind = {path: kind}
    self.path2vars = {path: [list of readable vars]}
    self.var2index = {var: index of var in its path's list of vars}
    
    self.kinds: tuple of kinds with any vars in self.
    self.vars: tuple of all vars in self.
    self.paths: tuple of all paths with any vars in self.

    kinds are: 'snap', 'aux', 'hion', 'helium', 'ooe'.
    if kind has no vars, do not include it in results.

    snap: BifrostSnap
    bcalc: BifrostCalculator
    '''
    KINDS = ('snap', 'aux', 'hion', 'helium', 'ooe')

    def __init__(self, snap, bcalc):
        self.snap = snap
        self.bcalc = bcalc
        self.init_all()

    snap = weakref_property_simple('_snap')  # weakref --> snap caching paths manager would be fine.
    bcalc = weakref_property_simple('_bcalc')  # weakref --> snap caching paths manager would be fine.
    params = alias_child('snap', 'params')
    snapname = alias_key_of('params', 'snapname')
    NNN = property(lambda self: self.snap.file_s(self.bcalc),
            doc='''(str) the NNN part of the snapname_NNN.idl filename.''')
    snapdir = alias_child('bcalc', 'snapdir')

    def snappath(self, filename):
        '''returns os.path.join(self.snapdir, filename)'''
        return os.path.join(self.snapdir, filename)

    def init_all(self):
        '''init all KINDS in self.'''
        self.kind2path = dict()
        self.kind2vars = dict()
        self.var2kind = dict()
        self.var2path = dict()
        self.path2kind = dict()
        self.path2vars = dict()
        self.var2index = dict()
        self.init_snap_kind()
        self.init_aux_kind()
        self.init_hion_kind()
        self.init_helium_kind()
        self.init_ooe_kind()
        self.kinds = tuple(self.kind2vars.keys())
        self.vars = tuple(self.var2kind.keys())
        self.paths = tuple(self.path2vars.keys())

    def _init_kind_vars_path(self, kind, vars, path):
        '''updates self with corresponding kind, vars, and path.'''
        self.kind2vars[kind] = vars
        self.kind2path[kind] = path
        for var in vars:
            if var in self.var2kind:  # var not unique... crash!
                errmsg = f'{type(self).__name__} with multiple vars with same name: {var!r}'
                raise LoadingNotImplementedError(errmsg)
            self.var2kind[var] = kind
            self.var2path[var] = path
        self.path2kind[path] = kind
        self.path2vars[path] = vars
        self.var2index.update({var: i for i, var in enumerate(vars)})

    def init_snap_kind(self):
        '''vars stored in snapname_NNN.snap file.'''
        path = self.snappath(f'{self.snapname}_{self.NNN}.snap')
        if self.params.get('do_mhd', False):
            vars = ('r', 'px', 'py', 'pz', 'e', 'bx', 'by', 'bz')
        else:
            vars = ('r', 'px', 'py', 'pz', 'e')
        self._init_kind_vars_path('snap', vars, path)

    def init_aux_kind(self):
        '''vars stored in snapname_NNN.aux file.'''
        path = self.snappath(f'{self.snapname}_{self.NNN}.aux')
        vars = tuple(self.params.get('aux', '').split())
        if len(vars) > 0:
            self._init_kind_vars_path('aux', vars, path)

    def init_hion_kind(self):
        '''vars stored in snapname.hion_NNN.snap file.'''
        path = self.snappath(f'{self.snapname}.hion_{self.NNN}.snap')
        if self.params.get('do_hion', 0) > 0:
            vars = ('hionne', 'hiontg', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'nh2')
            self._init_kind_vars_path('hion', vars, path)

    def init_helium_kind(self):
        '''vars stored in snapname.helium_NNN.snap file.'''
        path = self.snappath(f'{self.snapname}.helium_{self.NNN}.snap')
        if self.params.get('do_helium', 0) > 0:
            vars = ('nhe1', 'nhe2', 'nhe3')
            self._init_kind_vars_path('helium', vars, path)

    def init_ooe_kind(self):
        '''out of equilibrium vars.'''
        if self.params.get('do_out_of_eq', 0) > 0:
            raise NotImplementedError('loading ooe vars. Got do_out_of_eq > 0')

    # # # DISPLAY # # #
    def __repr__(self):
        return f'{type(self).__name__}(vars={self.vars})'

    def help(self):
        '''print docstring of self...'''
        print(type(self).__doc__)


# tell BifrostSnap about BifrostVarPathsManager
BifrostSnap.var_paths_manager_cls = BifrostVarPathsManager
