"""
File Purpose: statistics (e.g. mean, std, min, max)
"""
import warnings

from ..quantity_loader import QuantityLoader
from ...errors import MemorySizeError
from ...tools import (
    xarray_where_finite, xarray_stats,
    simple_property, UNSET,
)
from ...defaults import DEFAULTS

class StatsLoader(QuantityLoader):
    '''statistics, e.g. mean, std, min, max. Applied only along self.stat_dims_for(array).
    By default, stat_dims(array) returns only the self.maindims which appear in the array.
    '''
    # # # LOGIC / PROPERTIES / HELPER METHODS # # #
    @property
    def stat_dims(self):
        '''the dims over which to possibly apply statistics (StatsLoader methods).
        will only apply statics along these dims for an array if they actually appear in the array.
        None --> use self.maindims. (this is the default.)
        See also: self.stat_dims_for(array).
        '''
        if getattr(self, '_stat_dims', None) is None:
            return getattr(self, 'maindims', [])
        else:
            return self._stat_dims
    @stat_dims.setter
    def stat_dims(self, value):
        self._stat_dims = value

    @property
    def behavior_attrs(self):
        '''return dict of attrs which affect the behavior of this QuantityLoader.
        The implementation here returns ['stat_dims'] + any values from super().
        '''
        return ['stat_dims'] + getattr(super(), 'behavior_attrs', [])

    def stat_dims_for(self, array):
        '''return the dims to apply statistics over, for this array.
        Here, returns tuple of d from self.stat_dims if d in array.dims.
        '''
        return tuple(d for d in self.stat_dims if d in array.dims)

    stats_dimpoint_wise = simple_property('_stats_dimpoint_wise', default=None,
        doc='''whether to apply stat calculations at each DimPoint, or after loading the full array.
        [EFF] this setting is just for efficiency; it doesn't affect results (when no MemorySizeError crash).

        True --> apply stat calculations to each array (at each DimPoint) before joining arrays.
                e.g., self('mean_n') gets 'mean_n' at each fluid & snap, then joins results.
        False --> join arrays across all DimPoints before applying stat calculations.
                e.g., self('mean_n') gets 'n' (which varies across fluid & snap), then takes mean.
        None --> if result.size will be > DEFAULTS.STATS_DIMPOINT_WISE_MIN_N / self.get_ncpu(), use True.
                otherwise try using False, then use True if MemorySizeError is raised.
                (True seems to be faster for large arrays but slower for small arrays.
                But also, when ncpu>1, loading across dimpoints is faster due to parallelization.)

        regardless of this setting, stat calculations are applied only along self.stat_dims(array).''')

    @property
    def _extra_kw_for_quantity_loader_call(self):
        '''extra kwargs which can be used to set attrs self during self.__call__.
        The implementation here returns ['stats_dimpoint_wise'] + any values from super().
        '''
        # 'stats_dimpoint_wise' doesn't affect numerical results, just efficiency,
        #   which is why it's not in self.behavior_attrs. But, user might still want to set it during __call__.
        return ['stats_dimpoint_wise'] + super()._extra_kw_for_quantity_loader_call

    def _print_or_warn(self, msg, debug_thresh=1):
        '''if DEBUG>=debug_thresh, print msg. Else, warnings.warn(msg).'''
        if DEFAULTS.DEBUG >= debug_thresh:
            print(msg)
        else:
            warnings.warn(msg)

    def _get_stat_var(self, var, statfunc):
        '''returns result of applying statfunc to self(var), possibly one dimpoint at a time then joining results.
        see help(type(self).stats_dimpoint_wise) for details.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        if self.stats_dimpoint_wise is None:
            # if result will be a certain size or larger, use True (faster for large arrays).
            ncpu = self.get_ncpu() if hasattr(self, 'get_ncpu') else 1
            min_n = DEFAULTS.STATS_DIMPOINT_WISE_MIN_N
            size_threshold = min_n / ncpu
            if size_threshold is not None:
                result_size = self.match_var_result_size(var, maindims=True)
                if result_size > size_threshold:
                    if DEFAULTS.DEBUG >= 1 or getattr(self, 'verbose', False) >= 1:
                        warnmsg = (f'temporarily using stats_dimpoint_wise=True for efficiency; predicted '
                                   f'result_size ({result_size}) > DEFAULTS.STATS_DIMPOINT_WISE_MIN_N (={min_n}) / ncpu (={ncpu}).')
                        self._print_or_warn(warnmsg, debug_thresh=1)
                    return self._get_stat_var_dimpoint_wise_true(var, statfunc)
            # else, try with False first (faster for small arrays). Switch to True if MemorySizeError when False.
            try:
                return self._get_stat_var_dimpoint_wise_false(var, statfunc)
            except MemorySizeError:
                if DEFAULTS.DEBUG >= 1 or getattr(self, 'verbose', False) >= 1:
                    warnmsg = (f'MemorySizeError when avoiding dimpoint_wise stats due to stats_dimpoint_wise=None. '
                               f'Will use stats_dimpoint_wise=True instead. (var={var!r}) '
                               f'(Might want to adjust DEFAULTS.ARRAY_MBYTES_MAX, '
                               f'or explicity set stats_dimpoint_wise=False to see the MemorySizeError crash.)')
                    self._print_or_warn(warnmsg, debug_thresh=1)
                return self._get_stat_var_dimpoint_wise_true(var, statfunc)
        elif self.stats_dimpoint_wise:
            return self._get_stat_var_dimpoint_wise_true(var, statfunc)
        else:
            return self._get_stat_var_dimpoint_wise_false(var, statfunc)

    def _get_stat_var_dimpoint_wise_false(self, var, statfunc):
        '''returns result of applying statfunc to self(var). (Used when self.stats_dimpoint_wise=False.)'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        value = self(var)
        return statfunc(value)
    
    def _get_statfunc_of_var(self, var, statfunc):
        '''load this stat, for self(var).'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        value = self(var)
        return statfunc(value)

    def _get_stat_var_dimpoint_wise_true(self, var, statfunc, min_split=UNSET):
        '''returns result of applying statfunc to self(var). (Used when self.stats_dimpoint_wise=True.)
        min_split: UNSET or int
            [EFF] min length of dimension before actually applying dimpointwise stats along it.
            1 --> no minimum. If MemorySizeError when min_split > 1, try again but with min_split=1.
            UNSET --> use DEFAULTS.STATS_DIMPOINT_WISE_MIN_SPLIT.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        def loading_stat():
            '''loads this stat, for self(var), at a single dimpoint.'''
            __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
            var_value = self(var)
            return statfunc(var_value)
        if min_split is UNSET: min_split = DEFAULTS.STATS_DIMPOINT_WISE_MIN_SPLIT
        try:
            value = self.load_across_dims_implied_by(var,
                        self._get_statfunc_of_var, var, statfunc,   # loader & *args_loader
                        _min_split=min_split)
        except MemorySizeError:
            if min_split == 1:
                raise
            # else
            if DEFAULTS.DEBUG >= 5 or getattr(self, 'verbose', False) >= 4:
                warnmsg = (f'MemorySizeError when min_split={min_split}, during stats_dimpoint_wise=True. '
                           f'Trying min_split=1 instead. var={var!r}. (Might want to adjust DEFAULTS.ARRAY_MBYTES_MAX.)')
                if not (DEFAULTS.DEBUG >= 5):
                    warnings.warn(warnmsg)  # only verbose, not DEBUG.
                else:
                    print(warnmsg)  # DEBUG --> print, not warn.
            return self._get_stat_var_dimpoint_wise_true(var, statfunc, min_split=1)
        return value

    # # # LOADABLE QUANTITIES # # #
    # 'mean_{var}'
    @known_pattern(r'mean_(.+)', deps=[0])
    def get_mean(self, var, *, _match=None):
        '''mean. mean(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_mean)
    def _stat_dims_mean(self, array):
        return array.mean(dim=self.stat_dims_for(array))

     # 'std_{var}'
    @known_pattern(r'std_(.+)', deps=[0])
    def get_std(self, var, *, _match=None):
        '''standard deviation. std(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_std)
    def _stat_dims_std(self, array):
        return array.std(dim=self.stat_dims_for(array))

    # 'min_{var}'
    @known_pattern(r'min_(.+)', deps=[0])
    def get_min(self, var, *, _match=None):
        '''minimum. min(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_min)
    def _stat_dims_min(self, array):
        return array.min(dim=self.stat_dims_for(array))

    # 'max_{var}'
    @known_pattern(r'max_(.+)', deps=[0])
    def get_max(self, var, *, _match=None):
        '''maximum. max(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_max)
    def _stat_dims_max(self, array):
        return array.max(dim=self.stat_dims_for(array))

    # 'median_{var}'
    @known_pattern(r'median_(.+)', deps=[0])
    def get_median(self, var, *, _match=None):
        '''median. median(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_median)
    def _stat_dims_median(self, array):
        return array.median(dim=self.stat_dims_for(array))

    # 'rms_{var}'
    @known_pattern(r'rms_(.+)', deps=[0])
    def get_rms(self, var, *, _match=None):
        '''root mean square. sqrt(mean(var**2)). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_rms)
    def _stat_dims_rms(self, array):
        return (array**2).mean(dim=self.stat_dims_for(array))**0.5

    # 'delta_{var}'
    @known_pattern(r'delta_(.+)', deps=[0])
    def get_delta(self, var, *, _match=None):
        '''perturbation. var - mean(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_delta)
    def _stat_dims_delta(self, array):
        return array - array.mean(dim=self.stat_dims_for(array))

    # 'deltafrac_{var}'
    @known_pattern(r'deltafrac_(.+)', deps=[0])
    def get_deltafrac(self, var, *, _match=None):
        '''perturbation. (var - mean(var)) / mean(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_deltafrac)
    def _stat_dims_deltafrac(self, array):
        return (array / array.mean(dim=self.stat_dims_for(array))) - 1  # == (array - mean) / mean

    # 'meannormed_{var}'
    @known_pattern(r'meannormed_(.+)', deps=[0])
    def get_meannormed(self, var, *, _match=None):
        '''normalized by mean. var / mean(var). Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_meannormed)
    def _stat_dims_meannormed(self, array):
        return array / array.mean(dim=self.stat_dims_for(array))

    # 'weighted_{weights}_mean_{var}'
    @known_pattern(r'weighted_(.+)_mean_(.+)', deps=[0, 1])
    def get_weighted_mean(self, weights_var, *, _match=None):
        '''mean, weighted by weights. mean(weights*var)/mean(weights).
        E.g. 'weighted_n_mean_T' --> mean(n * T) / mean(n).
            (see also: 'nmean_[var]', which is a shorthand for 'weighted_n_mean_[var]')
        Applied only along any self.stat_dims in array.
        '''
        weights, var = _match.groups()
        return self(f'mean_({var}*meannormed_{weights})')  # mean(T*n/mean(n)) equivalent to mean(n*T)/mean(n).

    # 'stats_{var}'
    @known_pattern(r'stats_(.+)', deps=[0])
    def get_stats(self, var, *, _match=None):
        '''return dataset of stats for var
        stats include: mean, std, min, max, median, rms.
        Applied only along any self.stat_dims in array.
        '''
        var, = _match.groups()
        return self._get_stat_var(var, self._stat_dims_stats)
    def _stat_dims_stats(self, array):
        return xarray_stats(array, dim=self.stat_dims_for(array))

    # # # FINITE VALUES ONLY - e.g. "nanmean" # # #
    @known_pattern(r'finite_(.+)', deps=[0])    # 'finite_{var}'
    def get_finite(self, var, *, _match=None):
        '''var, masked with NaN wherever values are not finite.'''
        var, = _match.groups()
        value = self(var)
        return xarray_where_finite(value)

    @known_pattern(r'nanmean_(.+)', deps=[0])    # 'nanmean_{var}'
    def get_nanmean(self, var, *, _match=None):
        '''mean. mean(var), ignoring NaNs AND infs. Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self(f'mean_finite_{var}')

    @known_pattern(r'nanstd_(.+)', deps=[0])    # 'nanstd_{var}'
    def get_nanstd(self, var, *, _match=None):
        '''standard deviation. std(var), ignoring NaNs AND infs. Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self(f'std_finite_{var}')

    @known_pattern(r'nanmin_(.+)', deps=[0])    # 'nanmin_{var}'
    def get_nanmin(self, var, *, _match=None):
        '''minimum. min(var), ignoring NaNs AND infs. Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self(f'min_finite_{var}')

    @known_pattern(r'nanmax_(.+)', deps=[0])    # 'nanmax_{var}'
    def get_nanmax(self, var, *, _match=None):
        '''maximum. max(var), ignoring NaNs AND infs. Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self(f'max_finite_{var}')

    @known_pattern(r'nanmedian_(.+)', deps=[0])    # 'nanmedian_{var}'
    def get_nanmedian(self, var, *, _match=None):
        '''median. median(var), ignoring NaNs AND infs. Applied only along any self.stat_dims in array.'''
        var, = _match.groups()
        return self(f'median_finite_{var}')

    @known_pattern(r'nanrms_(.+)', deps=[0])    # 'nanrms_{var}'
    def get_nanrms(self, var, *, _match=None):
        '''root mean square. sqrt(mean(var**2)), ignoring NaNs AND infs.
        Applied only along any self.stat_dims in array.
        '''
        var, = _match.groups()
        return self(f'rms_finite_{var}')

    @known_pattern(r'nandelta_(.+)', deps=[0])    # 'nandelta_{var}'
    def get_nandelta(self, var, *, _match=None):
        '''perturbation. var - mean(var), ignoring NaNs AND infs.
        Applied only along any self.stat_dims in array.
        '''
        var, = _match.groups()
        return self(f'delta_finite_{var}')

    @known_pattern(r'nandeltafrac_(.+)', deps=[0])    # 'nandeltafrac_{var}'
    def get_nandeltafrac(self, var, *, _match=None):
        '''perturbation. (var - mean(var)) / mean(var), ignoring NaNs AND infs.
        Applied only along any self.stat_dims in array.
        '''
        var, = _match.groups()
        return self(f'deltafrac_finite_{var}')
