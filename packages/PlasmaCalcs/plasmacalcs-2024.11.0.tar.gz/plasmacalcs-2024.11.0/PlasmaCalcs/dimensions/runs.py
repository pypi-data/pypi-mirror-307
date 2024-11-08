"""
File Purpose: Run, RunList, RunDimension, RunHaver

"Run" refers to input from a single simulation run,
or analogous grouping of non-simulation data.
"""
import os
import re

from .dimension_tools import (
    DimensionValue, DimensionValueList,
    Dimension, DimensionHaver,
)
from ..errors import RunKeyError, RunValueError
from ..tools import (
    alias, elementwise_property, weakref_property_simple,
    UNSET,
    format_docstring,
    get_paths_with_common_start,
    xarray_rename,
)

''' --------------------- Run & RunList --------------------- '''

_paramdocs_runs = {
    'title': '''None or str
        title for this run. Can be shorthand; doesn't need to be the full file path.''',
    'i': '''None or int
        index for this run. If None, cannot convert to int.''',
    'path': '''None or str
        file path to this run. internally, run.path will always store the absolute path (unless None).''',
    'common': '''None or str
        common start to run's full title, which has not been included in run.title.
        allows title to be abbreviated without loss of info about run.''',
    'calculator': '''None or PlasmaCalculator
        the PlasmaCalculator associated with this run.
        (internally, uses weakref, to avoid circular references in case calculator points to Run as well.)''',
    'paths': '''iterable of str
        paths to runs. Can be input as relpath or abspath; internally will always use abspath.''',
    'titles': '''UNSET, None, str, or iterable of UNSET/None/str with same length as paths.
        indicate titles for runs at paths.
        UNSET --> infer title(s) based on common & path(s).
        None --> use title=None, for all runs.
        str --> use title=str.
        iterable --> at each paths[i], use titles[i].''',
    'common_sep': '''str, default '_'
        used to infer common and/or titles when needed.
        To ensure words & concepts aren't cut into pieces by accident,
            look back to the last slash or the last common_sep in path,
            whichever makes a longer common. E.g. if common_sep='_':
                'runtype_run0', 'runtype_run1' --> 'runtype_', ['run0', 'run1']
                'rundir/run0', 'rundir/run1' --> 'runtype/', ['run0', 'run1']''',
    'valid_only': '''bool
        whether to only keep valid runs. True --> only keep runs with run.is_valid().''',
    'missing_ok': '''bool
        whether to allow missing paths. False --> crash if any path doesn't exist.''',
    'extra_infos': '''None or list of dicts
        if provided, use these dicts as additional info for each Run,
            and len(infos) should be equal to len(paths).''',
    'exclude_path_if': '''None or callable of str -> bool
        if provided, exclude any paths with exclude_path_if(os.path.abspath(path)).''',
    'common_path': '''str
        any path string which is the start of any number of runs in dir.
        if abspath, compare to abspaths from dir, else compare to relpaths from dir.''',
}

@format_docstring(**_paramdocs_runs)
class Run(DimensionValue):
    '''run... input from a single simulation run, or analogous grouping of non-simulation data.
    title: {title}
    i: {i}
    path: {path}
    common: {common}
    calculator: {calculator}

    other kwargs are stored as attributes of self, and keys stored in self.other_info_keys.

    subclasses may wish to implement Run.is_valid(); here, Run.is_valid() always returns True.
    '''
    def __init__(self, title=None, i=None, *, path=None, common=None, calculator=None, **other_info):
        super().__init__(title, i)
        self.path = os.path.abspath(path) if path is not None else None
        self.common = common
        self.calculator = calculator
        self.other_info_keys = list(other_info.keys())
        for kw, val in other_info.items():
            setattr(self, kw, val)

    @classmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def from_path(cls, path, *, common=None, title=UNSET, **other_info):
        '''return Run from file path. Infer title from path & common., unless title is provided.
        path: {path}
        common: {common}
            if common is None, title=path. Otherwise, look for common at beginning of abspath.
            If common found, title = the other part of path.
        title: UNSET or {title}
            if UNSET, infer title from path & common.
        '''
        path = os.path.abspath(path)
        if common is None:
            common = ''
        if title is UNSET:
            if path.startswith(common):
                title = path[len(common):]
            else:
                title = path
        return cls(title=title, path=path, common=common, **other_info)

    title = alias('s')

    dirname = property(lambda self: os.path.dirname(self.path) if self.path is not None else None,
                        '''os.path.dirname(self.path) if possible, else None.''')

    basename = property(lambda self: os.path.basename(self.path) if self.path is not None else None,
                        '''os.path.basename(self.path) if possible, else None.''')

    @property
    def full_title(self):
        '''full title of self. self.title + self.common.
        If either is None, return the other one. If both are None, return None.
        '''
        if self.title is None:
            return self.common
        elif self.common is None:
            return self.title
        else:
            return self.common + self.title

    @property
    def exists(self):
        '''tells whether self.path actually exists.'''
        return os.path.exists(self.path)

    @property
    def isdir(self):
        '''tells whether self.path is actually a directory.'''
        return os.path.isdir(self.path)

    calculator = weakref_property_simple('_calculator')

    def __repr__(self):
        contents = [repr(val) for val in [self.title, self.i] if val is not None]
        return f'{type(self).__name__}({", ".join(contents)})'

    def is_valid(self):
        '''returns whether self represents a valid run.
        Here, returns True. subclasses may wish to override.
        '''
        return True

    # # # PICKLING # # #
    def __getstate__(self):
        '''return state for pickling. (pickle can't handle weakrefs. pickling is required by multiprocessing.)'''
        state = self.__dict__.copy()
        # follow weakrefs. state['_calculator'] might be a weakref;
        #   self.calculator would be the result of following this weakref (see weakref_property_simple).
        state['_calculator'] = self.calculator
        return state

    def __setstate__(self, state):
        '''set state from pickling. (pickle can't handle weakrefs. pickling is required by multiprocessing.)'''
        self.__dict__.update(state)
        # set up weakrefs. state['_calculator'] might be a calculator but should be a weakref instead;
        #   setting self.calculator = state['_calculator'] internally stores the value as a weakref.
        self.calculator = state['_calculator']


class RunList(DimensionValueList):
    '''list of runs'''
    _dimension_key_error = RunKeyError
    value_type = Run

    title = elementwise_property('title')
    full_title = elementwise_property('full_title')
    path = elementwise_property('path')
    dirname = elementwise_property('dirname')
    basename = elementwise_property('basename')
    exists = elementwise_property('exists')
    isdir = elementwise_property('isdir')
    calculator = elementwise_property('calculator')

    @classmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def from_infos(cls, infos, *, valid_only=False, **common_info):
        '''return cls instance from iterable of dicts. (i will be determined automatically.)
        dicts may contain any kwargs to pass to __init__ except for 'i'.

        valid_only: {valid_only}
        '''
        if not valid_only:
            return super().from_infos(infos, **common_info)
        # else, valid_only:
        for info in infos:
            assert 'i' not in infos, 'i is determined automatically when using from_infos'
        i = 0
        values = []
        for info in infos:
            value = cls.value_type(**info, i=i, **common_info)
            if value.is_valid():
                values.append(value)
                i += 1
        return cls(values)

    @staticmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def infer_common_and_titles(paths, *, common=UNSET, common_sep='_', titles=UNSET):
        '''infer titles and common.

        common: UNSET or {common}
            if provided, use titles = [(path[len(common):] if path.startswith(common) else path) for path in paths],
            AFTER converting paths to abspaths.
            if common is None, return (None, [abspath(path) for path in paths]).
            if common is not an abspath, convert common to abspath first.
        titles: {titles}
        common_sep: {common_sep}

        "inferring titles and common" means:
            inferred common will be the common start to all paths, which will not be included in titles.
                if common is provided, use common instead of inferring it.
            inferred titles will be the rest of each path (as an abspath), after common.

        but, replace any empty string in result (common or any title) with None instead.
        return (common, titles)
        '''
        paths = [os.path.abspath(p) for p in paths]
        if common is UNSET:  # use common_sep to infer common.
            common = os.path.commonprefix(paths)
            # look back to last slash or last common_sep.
            # but, use os.path instead of '/', in case of different operating systems.
            cdir, cname = os.path.split(common)
            if cname == '':    # common already ends with a slash;
                pass  # no need to look for common_sep or a slash.
            elif common_sep in cname:  # look back to the last common_sep.
                common = common[:common.rindex(common_sep) + 1]
            else:  # look back to the last slash.
                common = common[:common.rindex(cname)]
        elif common is not None:
            if not os.path.isabs(common):
                common = os.path.abspath(common)
        # get titles
        if titles is UNSET or titles is None or isinstance(titles, str):
            titles = [titles for _ in paths]
        for i, (title, path) in enumerate(zip(titles, paths)):
            if title is UNSET:
                if path.startswith(common):
                    titles[i] = path[len(common):]
                    if titles[i][0] == os.path.sep:
                        titles[i] = titles[i][1:]
                else:
                    titles[i] = path
            if title == '':
                titles[i] = None
            # else, don't change title.
        # replace empty strings with None
        if common == '':
            common = None
        titles = [None if title == '' else title for title in titles]
        return common, titles

    @classmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def from_paths(cls, paths, *, titles=UNSET, common=UNSET, common_sep='_', valid_only=True,
                   missing_ok=False, extra_infos=None, exclude_path_if=None, **shared_info):
        '''return RunList from iterable of paths. (i will be determined automatically.)
        paths: {paths}
        titles: {titles}
        common: UNSET or {common}
            if UNSET, infer from paths & common_sep.
        common_sep: {common_sep}
        valid_only: {valid_only}
        missing_ok: {missing_ok}
        extra_infos: {extra_infos}
        exclude_path_if: {exclude_path_if}

        additional kwargs will be passed to __init__ for each Run.
        '''
        paths = [os.path.abspath(p) for p in paths]
        if exclude_path_if is not None:
            paths = [p for p in paths if not exclude_path_if(p)]
        if not missing_ok:
            for path in paths:
                if not os.path.exists(path):
                    raise FileNotFoundError(f'path does not exist: {path!r}')
        common, titles = cls.infer_common_and_titles(paths, common_sep=common_sep, common=common, titles=titles)
        infos = [dict(path=path, title=title, common=common) for path, title in zip(paths, titles)]
        if extra_infos is not None:
            for info, extra_info in zip(infos, extra_infos):
                info.update(extra_info)
        return cls.from_infos(infos, valid_only=valid_only, **shared_info)

    @classmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def from_calculators(cls, calculators, *, titles=UNSET, common=UNSET, common_sep='_',
                         extra_infos=None, **shared_info):
        '''return RunList from iterable of calculators. (i will be determined automatically.)
        will also assign run.calculator = calculator for each run.

        calculators: iterable of PlasmaCalculator objects
            calculators associated with these runs.
            paths = c.dirname for c in calculators.
        titles: {titles}
        common: {common}
            if UNSET, infer from paths & common_sep.
        common_sep: {common_sep}
        extra_infos: {extra_infos}

        additional kwargs will be passed to __init__ for each Run.
        '''
        paths = [c.dirname for c in calculators]
        extra = [dict(calculator=c) for c in calculators]
        if extra_infos is not None:
            for info, extra_info in zip(extra, extra_infos):
                info.update(extra_info)
        return cls.from_paths(paths, titles=titles, common_sep=common_sep, extra_infos=extra, **shared_info)

    @classmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def from_common_path(cls, common_path='', *, dir=os.curdir, valid_only=True,
                         titles=UNSET, common=UNSET, common_sep='_', exclude_path_if=None, **other_info):
        '''return RunList of all existing runs starting with common_path.
        common_path: {common_path}
        dir: str
            directory to look in for existing runs starting with common_path.
        valid_only: {valid_only}
        titles: {titles}
        common: {common}
            if UNSET, infer from paths & common_sep.
        common_sep: {common_sep}
        exclude_path_if: {exclude_path_if}

        additional kwargs will be passed to __init__ for each Run.
        '''
        paths = get_paths_with_common_start(common_path, dir=dir, exclude_if=exclude_path_if)
        return cls.from_paths(paths, titles=titles, common_sep=common_sep, common=common,
                              exclude_path_if=exclude_path_if, valid_only=valid_only, **other_info)

    @classmethod
    @format_docstring(**_paramdocs_runs, sub_ntab=1)
    def from_here(cls, common_path='', *, titles=UNSET, common=UNSET,
                  valid_only=True, exclude_path_if=None,
                  **kw_from_common_path):
        '''return RunList of all existing runs in current directory.
        Equivalent to cls.from_common_path(common_path, dir=os.curdir, **kw).

        common_path: {common_path}
        titles: {titles}
        common: {common}
            if UNSET, infer from paths & common_sep.
        valid_only: {valid_only}
        exclude_path_if: {exclude_path_if}
        '''
        return cls.from_common_path(common_path=common_path, dir=os.curdir,
                                    titles=titles, common=common,
                                    valid_only=valid_only, exclude_path_if=exclude_path_if,
                                    **kw_from_common_path)


''' --------------------- RunDimension, RunHaver --------------------- '''

class RunDimension(Dimension, name='run', plural='runs',
                   value_error_type=RunValueError, key_error_type=RunKeyError):
    '''run dimension, representing current value AND list of all possible values.
    Also has various helpful methods for working with this Dimension.
    '''
    pass  # behavior inherited from Dimension.


@RunDimension.setup_haver
class RunHaver(DimensionHaver, dimension='run', dim_plural='runs'):
    '''class which "has" a RunDimension. (RunDimension instance will be at self.run_dim)
    self.run stores the current run (possibly multiple). If None, use self.runs instead.
    self.runs stores "all possible runs" for the RunHaver.
    Additionally, has various helpful methods for working with the RunDimension,
        e.g. current_n_run, iter_runs, take_run.
        See RunDimension.setup_haver for details.
    '''
    def __init__(self, *, run=None, runs=None, **kw):
        super().__init__(**kw)
        if runs is not None: self.runs = runs
        self.run = run
