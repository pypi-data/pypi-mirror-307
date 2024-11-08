"""
File Purpose: QuantityLoader, the base class for quantity loaders.

Note: "var" refers to quantity name; "quant" refers to the quantity itself.


Note: MetaQuantTracking predefines some things for tracking calcs, directly in the class namespace.
    E.g., known_var, known_pattern, known_setter.
In case anyone is looking through the codebase to understand these functions,
    this file is the one that defines them, though it doesn't use the usual 'def' notation,
    so, here are some strings that will pop up for searches like that, instead.
        def known_var(...)      # see MetaQuantTracking
        def known_pattern(...)  # see MetaQuantTracking
        def known_setter(...)   # see MetaQuantTracking
    if you landed here by doing command+F on the codebase, see MetaQuantTracking for details.
    (see also: quantity_tools.py, which defines the classes which these are instances of,
        i.e. DecoratingVars, DecoratingPatterns, and DecoratingSetters.)
"""

import xarray as xr

from .caching import VarCacheSingles
from .quant_tree import QuantTree
from .quantity_tools import (
    MatchedQuantity, MatchedVar, MatchedPattern,
    Pattern,
    DecoratingVars, DecoratingPatterns, DecoratingSetters,
    CallDepthMixin,
)
from ..dimensions import BehaviorHaver
from ..errors import (
    InputError, InputConflictError,
    OverrideNotApplicableError, CacheNotApplicableError,
    FormulaMissingError, LoadingNotImplementedError,
    DimensionError,
)
from ..tools import (
    alias, simple_setdefault_property,
    using_attrs, maintaining_attrs,
    format_docstring,
    RESULT_MISSING, UNSET,
    Tree,
    xarray_assign,
    copy_via_pickle,
)
from ..defaults import DEFAULTS


''' --------------------- MetaQuantTracking --------------------- '''

class MetaQuantTracking(type):
    '''metaclass which predefines some things for tracking calcs, in the class namespace:
        KNOWN_VARS - dict of {var: LoadableVar} for all functions decorated with @known_var
        KNOWN_PATTERNS - dict of {pattern: LoadablePattern} for all functions decorated with @known_pattern.
        KNOWN_SETTERS - dict of {var: f} for all functions decorated with @known_setter
        known_var - instance of DecoratingVars; use @known_var or @known_var(name=varname) to decorate functions.
            use this for vars, which require exact match for name.
            E.g. name='n' for number density.
            (Note, if function.__name__ is 'get_{var}', name='{var}' is implied, if not provided explicitly.)
        known_pattern - instance of DecoratingPatterns; use @known_pattern(pattern) to decorate functions.
            use this for patterns, which require regex match for name.
            E.g. pattern='mean_(.+)' for mean of any var.
            decorated functions will be supplied with kwarg _match=re.fullmatch(pattern, var).
        known_setter - instance of DecoratingSetters; use @known_setter or @known_setter(name=varname).
            use this for setters, which are functions that set the value of vars.
            For more details see setvars or set_var.

        Also, copy base classes' KNOWN_VARS, KNOWN_PATTERNS, and KNOWN_SETTERS to this class, if they exist.
    '''
    @classmethod
    def __prepare__(_metacls, _name, bases):
        KNOWN_VARS = dict()  # [TODO] use ordered dict for earlier python (before dict order guaranteed)?
        KNOWN_PATTERNS = dict()
        KNOWN_SETTERS = dict()
        for base in bases:
            # So that keys appear in __mro__ order, must iterate through bases in order.
            # So, the first time a key appears, it points to the earliest (in __mro__ order)
            # implementation, so it should not be overwritten if it appears again.
            #    Hence, avoid dict.update; use dict.setdefault instead.
            #
            # Additionally, need to avoid the following:
            #    'vv' defined in Class0.
            #    Class1 subclasses Class0 but does NOT also define 'vv'.
            #    Class2 subclasses Class0 and defines 'vv' too.
            #    class Class3(Class1, Class2): ...
            #    now, Class3.mro() has [Class1, Class2, Class0], so:
            #      Class3.get_vv uses Class2.get_vv.
            #        (This is good; should use the earliest-in-mro() get_vv to get value.)
            #      Class3.KNOWN_VARS['vv'] uses Class1.KNOWN_VARS['vv'].
            #        (This is bad; should use the KNOWN_VARS attached to get_vv.)
            # To avoid this, below checks where key was defined if it appears in dict already;
            #    if it was defined in a subclass, don't overwrite.
            base_kvars = getattr(base, 'KNOWN_VARS', {})
            if base_kvars:
                for k, v in base_kvars.items():
                    try:
                        existing = KNOWN_VARS[k]
                    except KeyError:  # didn't exist yet
                        KNOWN_VARS[k] = v
                    else:  # existed already
                        # only overwrite if this base is a subclass of where the existing value was defined.
                        if issubclass(base, existing.cls_where_defined):
                            KNOWN_VARS[k] = v
            base_kpats = getattr(base, 'KNOWN_PATTERNS', {})
            if base_kpats:
                for k, v in base_kpats.items():
                    try:
                        existing = KNOWN_PATTERNS[k]
                    except KeyError:
                        KNOWN_PATTERNS[k] = v
                    else:
                        if issubclass(base, existing.cls_where_defined):
                            KNOWN_PATTERNS[k] = v
            base_ksetters = getattr(base, 'KNOWN_SETTERS', {})
            if base_ksetters:
                for k, v in base_ksetters.items():
                    try:
                        existing = KNOWN_SETTERS[k]
                    except KeyError:
                        KNOWN_SETTERS[k] = v
                    else:
                        if issubclass(base, existing.cls_where_defined):
                            KNOWN_SETTERS[k] = v
        known_var = DecoratingVars(KNOWN_VARS)
        known_pattern = DecoratingPatterns(KNOWN_PATTERNS)
        known_setter = DecoratingSetters(KNOWN_SETTERS)
        return dict(KNOWN_VARS=KNOWN_VARS, KNOWN_PATTERNS=KNOWN_PATTERNS, KNOWN_SETTERS=KNOWN_SETTERS,
                    known_var=known_var, known_pattern=known_pattern, known_setter=known_setter)

    def __init__(self, *args, **kw):
        self.known_var.cls_associated_with = self
        for k, v in self.KNOWN_VARS.items():
            if not hasattr(v, 'cls_where_defined'):
                v.cls_where_defined = self
        self.known_pattern.cls_associated_with = self
        for k, v in self.KNOWN_PATTERNS.items():
            if not hasattr(v, 'cls_where_defined'):
                v.cls_where_defined = self
        self.known_setter.cls_associated_with = self
        for k, v in self.KNOWN_SETTERS.items():
            if not hasattr(v, 'cls_where_defined'):
                v.cls_where_defined = self


''' --------------------- QuantityLoader --------------------- '''

class QuantityLoader(BehaviorHaver, CallDepthMixin, metaclass=MetaQuantTracking):
    '''base class for quantity loaders. See self.get or self.__call__ for details.'''
    setvars = simple_setdefault_property('_setvars', lambda: VarCacheSingles(),
            doc='''VarCache of vars set via self.set_var(). Returns these values when appropriate,
            i.e. whenever self.behavior is compatible with the behavior in the cache.
            To empty the cache, use self.setvars.clear() to empty the cache.''')

    get = alias('__call__')

    def __call__(self, var, *args, name=UNSET, item=False, verbose=UNSET, **kw):
        '''returns value of var from self.
        result is probably an xarray.DataArray, but not guaranteed.
        
        var: str or iterable of strs.
            Name of the var(s) to load. E.g. 'n' for number density, or ['n', 'u'] for number density & velocity.
            If multiple vars, result will be an xarray.Dataset, with data_var names the same as the var names.

            Determine how to load each var, as follows:
                - (caching) if var in self.cache, with matching self.behavior_attrs, use value from cache.
                    [TODO] - caching not yet implemented. May allow for better efficiency. 
                - (setvars) if var in self.setvars, with matching self.behavior_attrs, use value from setvars.
                    [TODO] - improve set_var functionality.
                    set_var will allow user to apply PlasmaCalcs calculations to arbitrary values,
                    not just values from one of the hookups. Useful for testing & quick calculations.
                - (KNOWN_VARS) if var in self.KNOWN_VARS,
                    use the corresponding function to get it.
                - (KNOWN_PATTERNS) if var matches a pattern from self.KNOWN_PATTERNS,
                    use the corresponding function to get it.
                - (direct) attempt to load var "directly", via self.load_direct.
                    load_direct will almost always end up loading values directly from a file (e.g., "data").
                    However, there is one more chance for it to get intercepted: via direct_overrides.
                    - (direct_overrides) if var in self.direct_overrides, attempts self.direct_overrides[var].
                        The idea is to use direct_overrides when requiring alternate instructions for
                        what would otherwise be a "base" var.
                        E.g., 'n' may be a "base" var, but if quasineutral then 'ne' is not saved in a file;
                            so, base_overrides[<key for density>] may tell how to get 'ne'.
                        Note: for overrides which depend on current state, use direct_overrides_dynamic.
                        For overrides which are "always" implemented (not toggled by other things), use direct_overrides.
                    - (fromfile) load_direct uses self.load_fromfile whenever direct_overrides is not applicable.

            Those are checked in the order listed.
            If none of those work, raise FormulaMissingError.

        name: UNSET, None, or str
            try to set result.name = name.
            UNSET --> use name = var.
        item: bool
            if True, convert result to single value (e.g., python float) via result.item().
            This will cause crash if result is not a single value;
                it will also cause all metadata stored in the result to be lost.
        verbose: UNSET, bool, or int
            set self.verbose during this call to self.
            UNSET --> use self.verbose (unchanged)
        return_type: 'dataset' or 'dict'
            return type when var is an iterable of vars. Default is 'dataset'.
            See also help(self.get_vars) for more details.

        kw may additionally contain any keys from self.kw_call_options().
            if it does, pop those values, and temporarily set the corresponding attr.
            E.g.: self('n', units='si', fluid=1)
                --> temporarily set units='si', fluid=1, while getting 'n'.

        [EFF] passes _match=re.fullmatch(pattern, var) to the getter function,
            if the match is from KNOWN_PATTERNS (but not if it is from KNOWN_VARS).
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        # handle multiple vars
        if not isinstance(var, str):
            return self.get_vars(var, *args, name=name, item=item, verbose=verbose, **kw)
        # pop kw
        behavior_attrs = self.behavior_attrs
        extra_kw = self._extra_kw_for_quantity_loader_call
        using = {key: kw.pop(key) for key in tuple(kw.keys()) if key in behavior_attrs or key in extra_kw}
        if verbose is not UNSET: using['verbose'] = verbose
        # load the value of var
        with self._increment_call_depth():
            result = RESULT_MISSING
            with self.using(**using):
                # verbose / debugging
                if DEFAULTS.DEBUG >= 7 or getattr(self, 'verbose', False) >= 2:
                    depth = self.call_depth
                    print('| '*depth + f'(call_depth={depth}) get var={var!r}')
                with self.using(_inside_quantity_loader_call_logic=True):
                    if result is RESULT_MISSING:
                        # try to get from cache
                        try:
                            result = self.get_set_or_cached(var)  # [TODO] get_set xarray or simple value here;
                        except CacheNotApplicableError:
                            pass
                    if result is RESULT_MISSING:
                        # try to get from KNOWN_VARS or KNOWN_PATTERNS
                        try:
                            matched_quantity = self.match_var(var)
                        except FormulaMissingError as err0:  # (direct)   # no match in KNOWN_VARS & KNOWN_PATTERNS.
                            # try to get from load_direct
                            try:
                                result = self.load_direct(var, *args, **kw)  # [TODO] get_set array value here.
                            except Exception as err1:
                                raise err1 from err0   # traceback will include info from err0 and err1.
                if result is RESULT_MISSING:
                    # getting from KNOWN_VARS or KNOWN_PATTERNS (self.match_var didn't crash)
                    getter = matched_quantity.get_f(self)
                    _match = matched_quantity._match
                    if _match is None:  # (KNOWN_VARS)
                        result = getter(*args, **kw)
                    else:               # (KNOWN_PATTERNS)
                        result = getter(var, *args, _match=_match, **kw)
                assert result is not RESULT_MISSING, 'if this assertion fails, there is a coding error above.'
                # "post-processing" of result (intentionally still inside self.using(...))
                result = self._call_postprocess(result, var=var, name=name, item=item)
        return result

    def _call_postprocess(self, result, *, var, name=UNSET, item=UNSET, **kw__super):
        '''postprocess result from self.__call__. Called during self.__call__.
        (called inside self._increment_call_depth(); self.call_depth here would tell depth of the current call.)

        result: any value, probably an xarray.DataArray
            result from self.__call__, before postprocessing.
        var, name, item: UNSET or value
            passed directly from self.__call__.
        kw__super: additional kwargs passed to super()._call_postprocess, if it exists, else ignored.
            (more options might be added to _call_postprocess in the future.)

        The implementation here does the following (subclasses might override / add to this):
            - if self.verbose >= 4, print a message about getting var.
            - call super()._call_postprocess, if it exists.
            - result = self.attach_extra_coords(result).
            - if name was provided, set result.name = name, if possible.
            - if item, convert result to single value via result.item().
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        if getattr(self, 'verbose', False) >= 4:
            depth = self.call_depth
            print('/ '*depth + f'(call_depth={depth}) got var={var!r}')
        if hasattr(super(), '_call_postprocess'):
            result = super()._call_postprocess(result, var=var, name=name, item=item, **kw__super)
        result = self.attach_extra_coords(result)
        if name is UNSET:
            name = var
        try:
            result.name = name
        except AttributeError:  # e.g. 'float' object has no attribute 'name'
            if DEFAULTS.DEBUG > 2:
                raise
            # else, pass; it's fine, just don't name the result.
        if item:
            if result.size != 1:
                errmsg = (f'expected result.size==1 when item=True, but got size={result.size}\n'
                          f'This error is likely caused by having a dim with length>1 in self.dims,\n'
                          f'for one of the dims used when getting var={var!r}.')
                raise DimensionError(errmsg)
            result = result.item()
        return result

    @property
    def _extra_kw_for_quantity_loader_call(self):
        '''extra kwargs which can be used to set attrs self during self.__call__.
        (This is in addition to all self.behavior_attrs().). The implementation here just returns [].
        '''
        return []

    def kw_call_options(self):
        '''returns list of kwarg names which can be used to set attrs self during self.__call__.
        (see self.__call__ for more details).
        Here, returns list(self.behavior_attrs) + list(self._extra_kw_for_quantity_loader_call)
        '''
        return list(self.behavior_attrs) + list(self._extra_kw_for_quantity_loader_call)

    def get_vars(self, vars, *args, return_type='dataset', **kw):
        '''returns values of vars from self.
        result is probably an xarray.Dataset, but not guaranteed; also depends on return_type.

        Equivalent to self(vars, *args, return_type='dataset', **kw).
            (Actually, self(vars, ...) will call self.get_vars(vars, ...).)

        vars: iterable of strs
            Names of the vars to load. ['n', 'u'] for number density & velocity.
        return_type: 'dataset' or 'dict'
            if 'dataset', return result as xarray.Dataset.
                the data_var names will be the same as the var names.
            if 'dict', return result as dict of {var: value}.

        additional args & kwargs are passed to self(...).
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        result = dict()
        for var in vars:
            result[var] = self(var, *args, **kw)
        if return_type == 'dataset':
            result = xr.Dataset(result)
        return result

    def _provided_val(self, var, _val=None, _known_vals=dict()):
        '''returns the value of var, either from _known_vals or _val.
        if _val provided, return it; if '_{var}' in _known_vals, return it;
        if both provided, crash with InputConflictError (unless they are the same object),
        else, return None.

        Can use this internally to avoid redundant recalculations. (See e.g. VectorArithmeticLoader)

        '''
        _vstr = f'_{var}'
        if _vstr in _known_vals and (_val is not None) and (_val is not _known_vals[_Astr]):
            raise InputConflictError(f'cannot provide both _val and {_vstr}')
        return _known_vals.get(_vstr, _val)

    # # # ATTRS MANAGEMENT # # #
    using_attrs = using_attrs
    using = alias('using_attrs')
    maintaining_attrs = maintaining_attrs
    maintaining = alias('maintaining_attrs')

    # # # LOAD FROM KNOWN_VARS OR KNOWN_PATTERNS # # #
    quant_tree_cls = QuantTree   # class to use when making quant_tree from self & var.
    matched_var_cls = MatchedVar   # class to use for MatchedVar in self.match_var
    matched_pattern_cls = MatchedPattern   # class to use for MatchedPattern in self.match_var

    @classmethod
    def match_var(cls, var):
        '''match var from cls.KNOWN_VARS or cls.KNOWN_PATTERNS, or raise FormulaMissingError.
        
        returns result=MatchedQuantity(var, loadable, _match=_match) where:
            loadable is the LoadableQuantity associated with this var,
            _match is:
                None, if var in cls.KNOWN_VARS;
                re.fullmatch(pattern, var), if var matches any pattern in cls.KNOWN_PATTERNS.
                    if var matches multiple patterns, only the first matching pattern is used.

            Uses MatchedVar if match from KNOWN_VARS, MatchedPattern if from KNOWN_PATTERNS.
            (note that both MatchedVar and MatchedPattern subclass MatchedQuantity.)

        loadable and _match can be retrieved via result.loadable and result._match.
        '''
        # match in KNOWN_VARS
        try:
            lquant = cls.KNOWN_VARS[var]
        except KeyError:
            pass
        else:
            return cls.matched_var_cls(var, lquant, _match=None)
        # match in KNOWN_PATTERNS
        for pattern, lquant in cls.KNOWN_PATTERNS.items():
            _match = pattern.fullmatch(var)
            if _match:
                return cls.matched_pattern_cls(var, lquant, _match=_match)
        # didn't match.
        raise FormulaMissingError(f"var={repr(var)}; no match in {cls.__name__}.KNOWN_VARS or .KNOWN_PATTERNS")

    def match_var_tree(self=UNSET, var=UNSET):
        '''return QuantTree of MatchedQuantity objects from matching var and all dependencies,
        using self.KNOWN_VARS and self.KNOWN_PATTERNS when searching for matches.

        var must be provided; var=UNSET will raise an error (helpful if tried calling this as a classmethod).

        See also: type(self).cls_var_tree, for the classmethod version of this function.
            Most of the time it is possible to get tree without any details from self,
            but sometimes not. e.g. when getting collision frequencies, self.fluid affects deps.
        '''
        if not isinstance(self, QuantityLoader):
            errmsg = (f'Expected QuantityLoader self, got type(self)={type(self)}.\n'
                      'This might occur if you called cls.match_var_tree, instead of obj.match_var_tree.\n'
                      'Use cls.cls_var_tree() instead of cls.match_var_tree(), to try getting tree from class.\n'
                      '  It should succeed for most vars, but fail for vars whose tree depends on present values.')
            raise InputError(errmsg)
        if var is UNSET:
            raise TypeError("match_var_tree() missing 1 required positional argument: 'var'")
        return self.quant_tree_cls.from_quantity_loader(self, var)

    quant_tree = match_var_tree   # [TODO] use alias instead? (But then it's inaccessible from cls.quant_tree.)

    @classmethod
    def cls_var_tree(cls, var):
        '''return QuantTree of MatchedQuantity objects from matching var and all dependencies,
        using self.KNOWN_VARS and self.KNOWN_PATTERNS when searching for matches.
        '''
        return cls.quant_tree_cls.from_quantity_loader(cls, var)

    def match_var_loading_dims(self, var, **kw_loading_dims):
        '''return dims for loading var across.
        Result will probably vary across these dims (but not guaranteed, if any dependency uses reduces_dims.)
        These are all Dimension dims, not maindims. (E.g. 'fluid' and 'snap', but not 'x', 'y', 'z').

        Equivalent: self.match_var_tree(var).loading_dims(**kw_loading_dims)
        '''
        tree = self.match_var_tree(var)  # in its own line for easier debugging in case of crash.
        return tree.loading_dims(**kw_loading_dims)

    def match_var_result_dims(self, var, **kw_result_dims):
        '''return dims which result of cls(var) will vary across.
        These are all Dimension dims, not maindims. (E.g. 'fluid' and 'snap', but not 'x', 'y', 'z').

        Equivalent: cls.match_var_tree(var).result_dims(**kw_result_dims)
        '''
        tree = self.match_var_tree(var)  # in its own line for easier debugging in case of crash.
        return tree.result_dims(**kw_result_dims)

    def match_var_result_size(self, var, *, maindims=True, **kw_result_dims):
        '''return size (number of elements) which self(var) will have.
        (Efficient; doesn't actually get self(var).)
        Depends on current values of relevant dims. (E.g., self.fluid, not self.fluids)

        maindims: bool
            if True, include maindims_shape when calculating size.
        '''
        result_dims = self.match_var_result_dims(var, **kw_result_dims)
        n_dimpoints = self.current_n_dimpoints(dims=result_dims)
        if maindims:
            maindims_size = getattr(self, 'maindims_size', 1)
            size = n_dimpoints * maindims_size
        else:
            size = n_dimpoints
        return size
        
    # # # LOAD DIRECT # # #
    def load_direct(self, var, *args, check_caches=False, **kw):
        '''load var "directly", from some source which is not known by the main part of PlasmaCalcs.
        Attempt the following, returning the first successful attempt:
            - if check_caches, return value from self.cache or self.setvars
            - return self.direct_overrides[var](self, *args, **kw).
            - return self.direct_overrides_dynamic()[var](self, *args, **kw).
            - use self.load_fromfile.

        return the result (probably a numpy array, but not guaranteed).

        Examples:
            load Bx directly from a file
            load n for H+, using a different module which somehow gives nH+
                (PlasmaCalcs doesn't need to know where the value came from.)

        if used an override, instead of loading from file,
            set self._load_direct_used_override = var.
            Otherwise, set it to None.
            This might be used, e.g., to determine if the output came directly from a file or not.
        '''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        # check for overrides
        override = None
        try:  # direct_overrides  (check this before direct_overrides_dynamic.)
            override = self.direct_overrides[var]
        except KeyError:
            pass
        if override is None:  # direct_overrides_dynamic
            overrides_dynamic = self.direct_overrides_dynamic()
            try:
                override = overrides_dynamic[var]
            except KeyError:
                pass
        if override is not None:  # found an applicable override
            try:
                result = override(self, *args, **kw)
            except OverrideNotApplicableError:
                pass
            else:
                self._load_direct_used_override = var
                return result
        # no override found, or override not applicable.
        self._load_direct_used_override = None
        return self.load_fromfile(var, *args, **kw)

    def load_fromfile(self, var, *args, **kw):
        '''load var directly from a file. Other methods should usually use load_direct, instead.
        the implementation here just raises LoadingNotImplementedError;
        subclasses should implement this method in order to load any values from files.
        '''
        raise LoadingNotImplementedError(f'{type(self).__name__}.load_fromfile')

    @property
    def direct_overrides(self):
        '''dict of {var: override} for all overrides of self which don't depend on behavior_attrs of self.
        For example, if user wants to set an override (or if setvars sets an override?), it will be here.
        '''
        try:
            result = self._direct_overrides
        except AttributeError:
            result = dict()
            self._direct_overrides = result
        return result

    def direct_overrides_dynamic(self):
        '''returns dict of {var: override} for all overrides of self which depend on behavior_attrs of self.'''
        return dict()

    # # # LOAD FROM SETVARS OR CACHED VALUES # # #
    def get_set_or_cached(self, var):
        '''returns var if found in self.setvars or self.cache, with compatible behavior_attrs.
        otherwise, raise CacheNotApplicableError.

        if var is found in self.setvars and has relevant, but not matching behavior_attrs,
            self.load_across_dims will be used to load the value.
        '''
        behavior = self.behavior
        # -- from cache --
        # [TODO] <-- loading from self.cache.
        # -- from setvars --
        # [TODO][FIX] current implementation assumes user will not set var for multiple unit systems,
        #     when using ukey for some of those but not others. This might cause issues?
        relevance, quant = self.setvars.lookup(var, behavior)
        if not relevance:
            errmsg = f'var={var!r} not found in self.setvars, with compatible or relevant behavior_attrs.'
            raise CacheNotApplicableError(errmsg)
        if relevance is True:
            self.setvars.mark_used(var, quant)
            return quant.get_value(units_manager=getattr(self, 'u', None))
        # else: relevance is a list of subdims, i.e., iterable dimensions from self.behavior,
        #       for which there exists at least one point in the cache.
        def setvars_across_dims_loader(var):  # loader for a single dims point.
            result = self(var)
            if not isinstance(result, xr.DataArray):
                result = xr.DataArray(result)
                # [TODO] assign appropriate coords & attrs to this array.
            return result
        return self.load_across_dims(setvars_across_dims_loader, var, dims=relevance)

    # # # SETTING VARS # # #
    def set_var(self, var, value, behavior_attrs=None, forall=[], *, ukey=None, forced=False, **kw_using):
        '''set var in self. When later doing self(var) to get var, return the set value,
        but only if self.behavior is compatible with the relevant parts of self.behavior when var was set.

        This function will use, if it exists:
            self.KNOWN_SETTERS[var](self, value, imposed=behavior_attrs, forall=forall)
        Otherwise, calls:
            self.set_var_internal(var, value, self.behavior_attrs, imposed=behavior_attrs, forall=forall)
        
        var: str
            the var to set in self.
        value: number, xarray, iterable or 1D array, array with shape matching self.maindims_shape.
            the value to set var to.
            number --> set var to this number.
            [TODO](not yet implemented) xarray --> set var to this xarray.
            [TODO](not yet implemented) iterable or 1D array --> set var to these values along dim='testing'.
            [TODO](not yet implemented) array with shape matching self.maindims_shape --> set var to this array.
        behavior_attrs: None or list
            tells which attrs from self control behavior of the set var.
            The set var will only be retrieved when behavior_attrs of self are compatible.
                E.g. set_var('n', ['fluid', 'snap']) --> saves 'n' in cache with current fluid & snap.
                Will only load 'n' if self.fluid and self.snap == cached fluid and snap for 'n'.
        forall: list of strings
            if provided, tells which attrs of self do NOT control the behavior of the set var.
            E.g. forall=['snap'] --> 'snap' will NOT be included in behavior_attrs.
            (anything in behavior_attrs AND forall will be removed from the final behavior_attrs)
        ukey: None or str
            if provided, tells string to give to UnitsManager when converting value's units.
                When ukey is known, setting value in any unit system will enable to read it in all unit systems.
                E.g. set_var('n', 1e10, ..., ukey='n', units='si')
                --> self('n', units='raw') == self('n', units='si') * self.u('u', 'raw', convert_from='si')
            if not provided, value will be associated with current unit system;
                attempted to read value in any other unit system will not used the cached value set here.
                E.g. set_var('u', 1e10, ..., units='si')  # ukey not provided
                --> self('u', units='raw') --> uses self's other logic for getting 'u', not from setvars.
            note: if provided, 'units' will be added to behavior_attrs if not already in there.
        forced: bool, default True
            handles the case where self.KNOWN_SETTERS[var] doesn't exist. In that case...
            True --> set var in self, anyway.
            False --> crash; raise FormulaMissingError

        additional kwargs, if provided, go to self.using(**kw) during the operation.

        returns list of set quantities.
        '''
        with self.using(**kw_using):
            # use KNOWN_SETTERS[var] if possible
            try:
                setter = self.KNOWN_SETTERS[var]
            except KeyError:
                pass
            else:
                return setter(self, value, imposed=behavior_attrs, forall=forall)
            # default (KNOWN_SETTERS[var] not found)
            if forced:
                self_battrs = self.behavior_attrs
                return self.set_var_internal(var, value, self_battrs, imposed=behavior_attrs, forall=forall, ukey=ukey)
            else:
                raise FormulaMissingError(f'set_var for var={var!r}. (when forced=False) (var not in KNOWN_SETTERS)')

    setvar = alias('set_var')
    set = alias('set_var')

    def set_var_internal(self, var, value, default_behavior_attrs, imposed=None, forall=[], *, ukey=None):
        '''set var in self. KNOWN_SETTERS functions may wish to use this method.
        (KNOWN_SETTERS functions should NOT use self.set_var, to avoid recursion issue.)

        This function has the internal logic for self.set_var;
            set_var calls set_var_internal when self.KNOWN_SETTERS[var] not provided.
        
        var: str
            the var to set in self.
        value: number, xarray, iterable or 1D array, array with shape matching self.maindims_shape.
            the value to set var to. See help(self.set_var) for more info.
        default_behavior_attrs: list of strings
            the behavior attrs relevant to setting this var;
            getting var only gives value when current behavior attrs values are compatible with the cached ones.
        imposed: None or list of strings
            if provided, use imposed instead of default_behavior_attrs.
        forall: list of strings
            if provided, tells which behavior attrs do NOT control the behavior of the set var.
            e.g. imposed=['snap', 'fluid'], forall=['snap'] --> use ['fluid'], only.
        ukey: None or str
            if provided, tells string to give to UnitsManager when converting value's units;
            when ukey is provided, can retrieve value in any unit system (probably 'si' or 'raw').
            when ukey not provided, if 'units' in used behavior attrs, can only retrieve value in that unit system.
        '''
        battrs = self._battrs_for_set_var_internal(default_behavior_attrs, imposed, forall, ukey=ukey)
        # set the value.
        if getattr(value, 'ndim', 0) == 0:
            # value is a number
            behavior = self.get_behavior(battrs)
            assign_attrs = dict(units=self.units) if 'units' in battrs else None
            value_as_xarray = behavior.dims.assign_to(value, attrs=assign_attrs, overwrite=False)
            value_as_xarray.name = var
            return self.setvars.append(var, value_as_xarray, behavior, ukey=ukey)
        else:
            # value not a number --> not yet implemented.
            errmsg = f'set_var for var={var!r} for value with ndim={value.ndim}, of type {type(value)}.'
            raise NotImplementedError(errmsg)

    def _battrs_for_set_var_internal(self, default_behavior_attrs, imposed=None, forall=[], *, ukey=None):
        '''returns behavior_attrs which will be used by set_var_internal, given these inputs.
        see help(self.set_var_internal) for details.
        '''
        # decide which behavior attrs to actually use, based on inputs.
        battrs = default_behavior_attrs if imposed is None else imposed
        battrs = set(battrs) - set(forall)
        if ukey is not None:
            battrs.update({'units'})  # put 'units' in battrs if it's not already there.
        return battrs

    def unset_var(self, var, behavior_attrs=[], *, missing_ok=True, **kw_using):
        '''remove var from self.setvars (but only at values stored with relevant behavior).
        [TODO] define rules for which vars unset which other vars...
            e.g. for eppic right now, set_var('n') sets 'den' but not 'n';
            unset_var('n') unsets nothing... but should probably alias to unset_var('den').

        behavior_attrs: list of strings
            only remove cached values where self.behavior matches cached behavior for these attrs.
            if empty, remove all cached values for var, regardless of associated behavior.
        missing_ok: bool
            whether it is okay for there to be zero matching cached values for var.
            raise CacheNotApplicableError if missing_ok=False when there are no matching cached values.
        additional kwargs, if provided, go to self.using(**kw) during the operation.

        return list of CachedQuantity objects which were removed from self.setvars.
        '''
        with self.using(**kw_using):
            return self.unset_var_internal(var, behavior_attrs, missing_ok=missing_ok)

    unset = alias('unset_var')

    def unset_var_internal(self, var, default_behavior_attrs, imposed=None, forall=[], *, ukey=None, missing_ok=True):
        '''unset var from self.setvars.
        KNOWN_SETTERS functions may wish to use this method, to unset dependent values.
            E.g. if u depends on n, and n is changed, may wish to unset the value of u.

        default_behavior_attrs: list of strings
            the behavior attrs relevant to setting this var.
        imposed: None or list of strings
            if provided, use imposed instead of default_behavior_attrs.
        forall: list of strings
            if provided, tells which behavior attrs to ignore when unsetting the var.
        ukey: None or string
            if provided, ignore 'units' behavior attr when unsetting the var
            (due to assuming that ukey was provided when setting the var,
            hence that the set var could be retrieved in any units system)
        missing_ok: bool
            whether it is okay for there to be zero matching cached values for var.
            raise CacheNotApplicableError if missing_ok=False when there are no matching cached values.

        return list of CachedQuantity objects which were removed from self.setvars.
        '''
        battrs = self._battrs_for_unset_var_internal(default_behavior_attrs, imposed, forall, ukey=ukey)
        behavior = self.get_behavior(battrs)
        return self.setvars.remove(var, behavior, missing_ok=missing_ok)

    def _battrs_for_unset_var_internal(self, default_behavior_attrs, imposed=None, forall=[], *, ukey=None):
        '''returns behavior_attrs which will be used by unset_var_internal, given these inputs.
        see help(self.unset_var_internal) for details.
        '''
        # decide which behavior attrs to actually use, based on inputs.
        battrs = default_behavior_attrs if imposed is None else imposed
        battrs = set(battrs) - set(forall)
        if ukey is not None:
            battrs = battrs - {'units'}  # remove 'units' from battrs if it's there.
        return battrs

    # # # HELP WITH QUANTS # # #
    # see quantities.help.py for details. Or, use QuantityLoader.help()

    # # # ATTACH EXTRA COORDINATES TO OUTPUTS # # #
    extra_coords = simple_setdefault_property('_extra_coords', dict,
            doc='''dict of {coord_name: coord_value} to attach to outputs of self(var).
            Useful if planning to join the output of self(var) with output from a different QuantityLoader.
            E.g. self.extra_coords={'run': 'run 0'} and other.extra_coords={'run': 'run 1'},
                then xr.concat([self('n'), other('n')], 'run') gives 'n' from self AND other.
                (this is nice if self and other have same values for dims. Otherwise, might struggle.)''')

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['extra_coords'], plus any behavior_attrs from super().
        '''
        return ['extra_coords'] + list(getattr(super(), 'behavior_attrs', []))

    def attach_extra_coords(self, arr):
        '''attach any self.extra_coords to array arr but only if it is an xarray.DataArray or xarray.Dataset'''
        if isinstance(arr, xr.DataArray):
            arr = xarray_assign(arr, coords=self.extra_coords, overwrite=False)
            # ^ used overwrite=False to avoid overwriting any existing coords with the same name;
            # it's also more efficient and doesn't produce a new array, if all coords are already present.
        return arr

    # # # COPYING # # #
    def copy(self):
        '''returns a deep copy of self.
        [TODO] implement something less hacky than using the pickle module?
        '''
        return copy_via_pickle(self)
