"""
File Purpose: MultiCalculator

[TODO] utilize DataTree instead of DataArray with "run" dimension?
    (maybe, as an option but still keep the DataArray option?
    DataArray is the more natural choice when most of runs' other coords are the same.)

[TODO] class inheritance from Dimension-related classes?
"""
import multiprocessing as mp
import xarray as xr

from ..dimensions import (
    RunHaver, RunList, _paramdocs_runs,
    SnapHaver, ProxySnapList,
)
from ..errors import SnapValueError
from ..plasma_calculator import DimensionlessPlasmaCalculator
from ..tools import (
    format_docstring,
    UNSET,
    alias_child,
    TaskList,
)
from ..defaults import DEFAULTS


_paramdocs_multicalculator = {
    'calculators': '''iterable of PlasmaCalculator objects
        The calculators associated with this MultiCalculator.''',
    'runs': '''UNSET or RunList
        The runs associated with this MultiCalculator.
        if UNSET, infer from calculators.
        (Note - to avoid circular references, run.calculator is a weakref for each run,
            which is why self must store calculators too, instead of just storing runs.)''',
    'join': '''"outer", "inner", "left", "right", "exact", or "override"; default 'inner'.
        String indicating how to combine differing indexes from calculators;
        passed directly to xarray.concat. Relevant docs copied below:
            - "outer": use the union of object indexes
            - "inner": use the intersection of object indexes
            - "left": use indexes from the first object with each dimension
            - "right": use indexes from the last object with each dimension
            - "exact": instead of aligning, raise `ValueError` when indexes to be aligned are not equal
            - "override": if indexes are of same size, rewrite indexes to be those of the first object
                with that dimension. Indexes for the same dimension must have the same size in all objects.''',
    'ncpu': '''None or int
        max number of cpus to use for parallelization (e.g., calculators can be called in parallel).
        None --> use multiprocessing.cpu_count()
        int --> use this value. if 0 or 1, do not use multiprocessing here.''',
}

@format_docstring(**_paramdocs_multicalculator, **_paramdocs_runs)
class MultiCalculator(RunHaver, DimensionlessPlasmaCalculator):
    '''tracks & uses a list of PlasmaCalculator objects when getting values.
    Each PlasmaCalculator will be associated with a Run value in the results.

    CAUTION: initializing this class WILL AFFECT the individual calculators!
        in particular, for each c in calculators, it may adjust:
            c.extra_coords, c.snaps, c.snap.

    runs: {runs}
    join: {join}
    ncpu: {ncpu}


    Additionally, if runs is None, the following are passed to RunList.from_calculators(...):

    titles: {titles}
    common: {common}
    extra_infos: {extra_infos}

    Things overridden here include:
        __call__: instead, __call__ each calculator in self, and concat results along 'run'
        dimensions (snap, fluid, jfluid)...
            plural (e.g. 'snaps') --> depends on join; infer from calculators.
                    when join='inner', only keep values which can be used by all calculators.
            singular (e.g. 'snap') --> setting value will also set the value for all calculators.
                    e.g. self.snap = 10 sets c.snap=10 for all calculators.
            this behavior is defined explicitly here instead of implicitly based on calculator dimensions.
    '''
    run_list_cls = RunList  # use this class when creating runs in classmethods e.g. from_here
    calculator_maker = NotImplemented  # callable of path -> PlasmaCalculator. Required by from_here.

    # # # CREATING / INITIALIZING # # #
    def __init__(self, calculators, runs=UNSET, *, join='inner', ncpu=1,
                 titles=UNSET, common=UNSET, extra_infos=None, **kw_super):
        self.calculators = calculators
        self.join = join
        self.ncpu = ncpu
        if runs is UNSET:
            runs = self.run_list_cls.from_calculators(calculators, titles=titles,
                                                      common=common, extra_infos=extra_infos)
        self.runs = runs
        self._init_runs_calculators()
        self.init_snaps()
        super(DimensionlessPlasmaCalculator, self).__init__(**kw_super)  # skip all PlasmaCalculator-related __init__.

    def _init_runs_calculators(self, runs=UNSET):
        '''assigns self.calculators to all runs from self.runs which had run.calculator=None.
        Additionally, update calculator.extra_coords with run=run for each run.
        runs: UNSET or RunList
            if provided, also set self.runs=runs.

        (This avoids circular references because run.calculator is stored internally as a weakref.)
        '''
        if runs is not UNSET:
            self.runs = runs
        for run, calculator in zip(self.runs, self.calculators):
            if run.calculator is None:
                run.calculator = calculator
            calculator.extra_coords.update(run=run)

    @classmethod
    @format_docstring(**_paramdocs_runs, **_paramdocs_multicalculator, sub_ntab=2)
    def from_here(cls, common_path='', *, join='inner', ncpu=1,
                  valid_only=True, exclude_path_if=None, titles=UNSET, common=UNSET,
                  **kw_calculator_maker):
        '''create MultiCalculator from runs in this directory.
        Equivalent to cls(RunList.from_here(...), ...) with kwargs passed appropriately.

        The RunList will be created using cls.run_list_cls.from_here(...)
        Each run's calculator will be created using cls.calculator_maker(...)

        Parameters which go to RunList.from_here(...):
            common_path: {common_path}
            valid_only: {valid_only}
            exclude_path_if: {exclude_path_if}
            titles: {titles}
            common: {common}

        Some kwargs go to MultiCalculator.__init__:
            join: {join}
            ncpu: {ncpu}

        Additional kwargs go to cls.calculator_maker(...)
        '''
        runs = cls.run_list_cls.from_here(common_path=common_path, valid_only=valid_only,
                                          exclude_path_if=exclude_path_if, titles=titles, common=common)
        if cls.calculator_maker is NotImplemented:
            errmsg = f'{cls.__name__}.calculator_maker, which is required by {cls.__name__}.from_here()'
            raise NotImplementedError(errmsg)
        calculators = [cls.calculator_maker(run.path, **kw_calculator_maker) for run in runs]
        return cls(calculators, runs=runs, join=join, ncpu=ncpu)


    # # # INITIALIZING HELPER FUNCTIONS # # #
    def init_snaps(self):
        '''set self.snaps AND snaps of all calculators in self.
        Note: it is not guaranteed that all calculators would be SnapHavers;
            if none are SnapHavers, this method will instead do nothing.
            if some are SnapHavers but others are not, this method will crash.
            if all are SnapHavers, follows the instructions below.

        Uses ProxySnapList to make list of snaps pointing to shared times;
            each ProxySnap may have details about the corresponding file to load from,
            when loading values at that snap.
        self.snaps will point to the ProxySnapList shared by all runs in self.
        The ProxySnapList creation will depend on self.join,
            for guidance on whether to keep all snaps ('outer') or only those shared by all runs ('inner').
        '''
        is_snaphaver = [isinstance(c, SnapHaver) for c in self.calculators]
        if not all(is_snaphaver):
            if any(not b for b in is_snaphaver):
                raise NotImplementedError('some calculators are SnapHavers, but others are not.')
        # else, all(is_snaphaver).
        proxy_list = ProxySnapList.from_calculators(self.calculators, join=self.join)
        proxy_list.set_in_calculators(self.calculators, reset_current_snap=True)

    # # # DIMENSION PROPERTIES # # #
    @property
    def snaps(self):
        '''snaps; must be the same object in c.snaps for all c in self.calculators.
        raise SnapValueError if not all calculators have the same snaps.
        '''
        snaps = self.calculators[0].snaps
        for c in self.calculators[1:]:
            if c.snaps != snaps:
                raise SnapValueError('not all calculators have the same snaps.')
        return snaps

    @property
    def snap(self):
        '''snap; setting self.snap=v will set c.snap=v for all c in self.calculators.
        getting self.snap will return the unambiguous "current snap", i.e. c.snap,
            but raise SnapValueError if not all calculators have the same snap.
        '''
        snap = self.calculators[0].snap
        for c in self.calculators[1:]:
            if c.snap != snap:
                raise SnapValueError('not all calculators have the same snap.')
        return snap
    @snap.setter
    def snap(self, v):
        for c in self.calculators:
            c.snap = v

    def existing_snaps(self, i):
        '''return self[i].existing_snaps()'''
        return self[i].existing_snaps()

    # # # GETITEM & ITERATION # # #
    def __getitem__(self, i):
        '''returns self.runs.get(i).calculator.
        This is the calculator at run i.
        might be different than self.calculators[i].
        '''
        return self.runs.get(i).calculator

    def __iter__(self):
        '''yield calculator for calculator in self'''
        return iter(self.calculators)

    def __len__(self):
        '''return len(self.calculators)'''
        return len(self.calculators)

    # # # MULTIPROCESSING # # #
    def get_ncpu(self, ncpu=UNSET):
        '''returns ncpu, using self.ncpu if ncpu is UNSET.
        if result would be None, returns multiprocessing.cpu_count() instead.
        '''
        result = self.ncpu if ncpu is UNSET else ncpu
        if result is None:
            result = mp.cpu_count()
        return result

    # # # CALL # # #
    def __call__(self, var, *args, join=UNSET, ncpu=UNSET, run=UNSET, **kw):
        '''concat results from calling each calculator(var, *args, **kw) implied by self.run.

        join: UNSET or str
            tells how to combine different indexes from calculators, during concat.
            UNSET --> use self.join.
        ncpu: UNSET, None, or int
            max number of cpus to use for parallelization (calculators can be called in parallel).
            UNSET --> use self.ncpu
            None --> use multiprocessing.cpu_count()
            int --> use this value. if 0 or 1, do not use multiprocessing here.
            Note: will actually use min(ncpu, self.current_n_run()).
        run: UNSET or any value used to set self.run
            if provided, sets self.run=run before calling calculators, then restores original value afterwards.
        '''
        join = self.join if join is UNSET else join
        ncpu = self.get_ncpu(ncpu)
        using_kw = dict() if run is UNSET else dict(run=run)
        with self.using(**using_kw):

            # if ncpu <= 1:    # note -- SimpleMultiprocessor already avoids multiprocessing if ncpu <= 1.
            #     results = []
            #     for run in self.iter_run():
            #         results.append(run.calculator(var, *args, **kw))
            tasks = TaskList((run.calculator, (var, *args), kw) for run in self.run_list())
            results = tasks(ncpu=ncpu)
        return xr.concat(results, 'run', join=join)

    def _call_single(self, calculator, var, *args, **kw):
        '''return result of calling calculator(var, *args, **kw).'''
        return calculator(var, *args, **kw)
