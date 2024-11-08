"""
File Purpose: misc. tools related to QuantityLoader
"""

import functools
import re

from ..errors import InputError, InputConflictError, InputMissingError
from ..tools import (
    IncrementableAttrManager,
    alias, alias_child,
    format_docstring,
    UNSET,
)
from ..defaults import DEFAULTS


_paramdocs = {
    'fname': '''str
        name of the callable used to calculate this quantity,
        via getattr(obj,fname)(...), where obj is a QuantityLoader.''',
    'var': '''str
        the var matched to this object.''',
    '_match': '''result of re.match
        the result of pattern.fullmatch(var) for the pattern associated with this object.
        None --> no pattern match; either no associated pattern or var is not a match.''',
    'deps': '''list of str/int/callable
        list of dependencies for this quant. Each dependency is one of the following:
            - a str, indicating a known var or pattern name,
            - an int, indicating a group index from a pattern match,
            - a callable of the form f(quantity_loader, var, groups) -> str or iterable,
                which tells the var name(s) associated with this dependency,
                where: quantity_loader is a QuantityLoader instance,
                    var is the matched var,
                    and groups=_match.groups() if _match provided else None.''',
    'dims': '''None or list of strings
        dimensions associated directly with this quantity. E.g. ['fluid', 'snap']
        None --> this quant is not directly associated with any dims.''',
    'ignores_dims': '''list of strings
        dimensions which the result ignores, even if the dependencies don't ignore.
        E.g. 'mod_(.+)' has ignores_dims=['component'],
            because it provides the same result regardless of obj.component.''',
    'reduces_dims': '''list of strings
        dimensions which the result reduces along.
        E.g. 'ldebye_subset' has reduces_dims=['fluid'],
            because the result doesn't have 'fluid' dim even though it depends on obj.fluid.'''
    }


''' --------------------- LoadableQuantity/Var/Pattern --------------------- '''

@format_docstring(**_paramdocs)
class LoadableQuantity():
    '''quantity which can be loaded from a QuantityLoader.
    QuantityLoader.KNOWN_VARS and KNOWN_PATTERNS will be a dict of {{str: LoadableQuantity}} pairs.

    fname: {fname}
    deps: {deps}
    dims: {dims}
    ignores_dims: {ignores_dims}
    reduces_dims: {reduces_dims}
    '''
    def __init__(self, fname, *, deps=[], dims=None, ignores_dims=[], reduces_dims=[], **kw_super):
        self.fname = fname
        self.deps = deps
        self.dims = dims
        self.ignores_dims = ignores_dims
        self.reduces_dims = reduces_dims
        super().__init__(**kw_super)

    # # # DICT-LIKE # # #
    def keys(self):
        '''returns keys whose values can be accessed via self[key].
        i.e.: ('fname', 'deps', 'dims', 'ignores_dims', 'reduces_dims').
        '''
        return ('fname', 'deps', 'dims', 'ignores_dims', 'reduces_dims')

    def items(self):
        '''returns (key, self[key]) for key in self.keys().'''
        return ((key, getattr(self, key)) for key in self.keys())

    def __getitem__(self, key):
        '''returns self.{key}, if key in self.keys().'''
        if key not in self.keys():
            raise KeyError(f'{key!r} not in self.keys()={self.keys()}.')
        return getattr(self, key)

    # # # GETTING THE CALLABLE TO USE # # #
    def get_f(self, quantity_loader):
        '''returns the callable to use to calculate this quantity, for this quantity_loader.'''
        # note: methods outside of this class should not assume other methods will use get_f;
        #   they should feel free to use getattr(quantity_loader, loadable_quantity.fname).
        # However, inside this class, methods should use get_f instead of getattr(...).
        return getattr(quantity_loader, self.fname)

    def get_f_module(self, quantity_loader):
        '''returns the module in which this quantity is defined, for this quantity_loader.'''
        return self.get_f(quantity_loader).__module__

    # # # DISPLAY # # #
    def _repr_deps(self):
        '''return repr for deps in self.'''
        result = []
        for dep in self.deps:
            if callable(dep):
                result.append(f'callable: {dep.__name__}')
            else:
                result.append(repr(dep))
        return '[' + ', '.join(result) + ']'

    def _repr_contents(self):
        '''return contents for __repr__.'''
        contents = [f'{self.fname!r}']
        if len(self.deps) > 0:
            contents.append(f'deps={self._repr_deps()}')
        if self.dims is not None:
            contents.append(f'dims={self.dims!r}')
        if len(self.ignores_dims) > 0:
            contents.append(f'ignores_dims={self.ignores_dims!r}')
        if len(self.reduces_dims) > 0:
            contents.append(f'reduces_dims={self.reduces_dims!r}')
        return contents

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(self._repr_contents())})'


@format_docstring(**_paramdocs)
class LoadableVar(LoadableQuantity):
    '''quantity which can be loaded from a QuantityLoader.
    QuantityLoader.KNOWN_VARS will be a dict of {{str: LoadableVar}} pairs.

    fname: {fname}
    deps: {deps}
        (Note: for LoadableVar, deps will not include ints, since there won't be any pattern match.)
    dims: {dims}
    ignores_dims: {ignores_dims}
    reduces_dims: {reduces_dims}
    '''
    pass  # all functionality inherited from LoadableQuantity.


@format_docstring(**_paramdocs)
class LoadablePattern(LoadableQuantity):
    '''quantity which can be loaded from a QuantityLoader.
    QuantityLoader.KNOWN_PATTERNS will be a dict of {{Pattern: LoadablePattern}} pairs.

    fname: {fname}
    deps: {deps}
    dims: {dims}
    ignores_dims: {ignores_dims}
    reduces_dims: {reduces_dims}
    '''
    pass  # all functionality inherited from LoadableQuantity.


''' --------------------- LoadQuantity/Var/Pattern --------------------- '''

@format_docstring(**_paramdocs)
class MatchedQuantity():
    '''LoadableQuantity matched to a var, which can be loaded from a QuantityLoader.

    var: {var}
    loadable: LoadableQuantity or None
        the LoadableQuantity associated with this MatchedQuantity instance.
        None --> create one from fname, deps, dims, ignores_dims, and reduces_dims,
                using defaults if UNSET. (however, fname must be provided in this case.)
    _match: {_match}

    self.fname aliases to self.loadable.fname.
    similarly for self.deps, self.dims, self.ignores_dims, self.reduces_dims.
    also similarly for self.get_f and self.get_f_module.
    '''
    def __init__(self, var, loadable=None, *, _match=None,
                 fname=None, deps=UNSET, dims=UNSET, ignores_dims=UNSET, reduces_dims=UNSET,
                 **kw_super):
        self.var = var
        if loadable is None:
            if fname is None:
                raise InputMissingError("'fname' is required when loadable=None.")
            kw_loadable = dict(deps=deps, dims=dims, ignores_dims=ignores_dims, reduces_dims=reduces_dims)
            kw_loadable = {k: v for k, v in kw_loadable.items() if v is not UNSET}
            loadable = LoadableQuantity(**kw_loadable)
        self.loadable = loadable
        self._match = _match
        super().__init__(**kw_super)

    fname = alias_child('loadable', 'fname')
    deps = alias_child('loadable', 'deps')
    dims = alias_child('loadable', 'dims')
    ignores_dims = alias_child('loadable', 'ignores_dims')
    reduces_dims = alias_child('loadable', 'reduces_dims')
    get_f = alias_child('loadable', 'get_f')
    get_f_module = alias_child('loadable', 'get_f_module')

    def groups(self, *, default=UNSET):
        '''return self._match.groups().
        default: UNSET or any object
            if _match is None, return default if provided (not UNSET), else raise TypeError.
        '''
        if self._match is None:
            if default is UNSET:
                raise TypeError(f'self.groups() when self._match=None, and default=UNSET.')
            else:
                return default
        return self._match.groups()

    @format_docstring(**_paramdocs, sub_indent=DEFAULTS.TAB)
    def dep_vars(self, quantity_loader=None):
        '''returns list of strings, the var names associated with self.deps.
        Each string will be a quant that QuantityLoader might load;
            might be a KNOWN_VAR or might be a KNOWN_PATTERN.
            (However, this method doesn't know whether the deps are actually loadable).
        self.deps is a {deps}

        quantity_loader: None or QuantityLoader
            if any dep is callable, quantity_loader must be provided,
            and is used to get string for dep via dep(quantity_loader, self.var, self.groups(default=None))
        '''
        result = []
        for dep in self.deps:
            if isinstance(dep, str):
                dep_var = dep
                result.append(dep_var)
            elif isinstance(dep, int):
                groups = self.groups()
                dep_var = groups[dep]
                result.append(dep_var)
            elif callable(dep):
                if quantity_loader is None:
                    raise InputMissingError(f'quantity_loader, when one or more deps are callable. (Got dep={dep}).')
                groups = self.groups(default=None)
                dep_var = dep(quantity_loader, self.var, groups)
                if isinstance(dep_var, str):
                    result.append(dep_var)
                else:
                    result.extend(dep_var)  # iterable dep_var.
            else:
                errmsg = f'type(dep)={type(dep)}. Expected str or int. (when var={self.var!r})'
                raise TypeError(errmsg)
            
        return result

    # # # DICT-LIKE # # #
    def keys(self):
        '''returns keys whose values can be accessed via self[key].
        i.e.: ('var', 'loadable', '_match', 'fname', 'deps', 'dims', 'ignores_dims', 'reduces_dims').
        '''
        return ('var', 'loadable', '_match', 'fname', 'deps', 'dims', 'ignores_dims', 'reduces_dims')

    def items(self):
        '''returns (key, self[key]) for key in self.keys().'''
        return ((key, getattr(self, key)) for key in self.keys())

    def __getitem__(self, key):
        '''returns self.{key}, if key in self.keys().'''
        if key not in self.keys():
            raise KeyError(f'{key!r} not in self.keys()={self.keys()}.')
        return getattr(self, key)

    # # # DISPLAY # # #
    def _repr_contents(self):
        '''return contents for __repr__'''
        contents = [f'{self.var!r}']
        contents.extend(self.loadable._repr_contents())
        if self._match is not None:
            contents.append(f'groups={list(self.groups())!r}')
        return contents

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(self._repr_contents())})'


@format_docstring(**_paramdocs)
class MatchedVar(MatchedQuantity):
    '''LoadableVar matched to a var, which can be loaded from a QuantityLoader.

    var: {var}
    loadable: LoadableVar or None
        the LoadableVar associated with this MatchedVar instance.
        None --> create one from fname, deps, dims, ignores_dims, and reduces_dims,
                using defaults if UNSET. (however, fname must be provided in this case.)
    _match: {_match}

    self.fname aliases to self.loadable.fname.
    similarly for self.deps, self.dims, self.ignores_dims, self.reduces_dims.
    also similarly for self.get_f and self.get_f_module.
    '''
    pass  # all functionality inherited from MatchedQuantity


@format_docstring(**_paramdocs)
class MatchedPattern(MatchedQuantity):
    '''LoadableVar matched to a var, which can be loaded from a QuantityLoader.

    var: {var}
    loadable: LoadablePattern or None
        the LoadablePattern associated with this MatchedPattern instance.
        None --> create one from fname, deps, dims, ignores_dims, and reduces_dims,
                using defaults if UNSET. (however, fname must be provided in this case.)
    _match: {_match}

    self.fname aliases to self.loadable.fname.
    similarly for self.deps, self.dims, self.ignores_dims, self.reduces_dims.
    also similarly for self.get_f and self.get_f_module.
    '''
    pass  # all functionality inherited from MatchedQuantity


''' --------------------- Pattern --------------------- '''

class Pattern():
    '''stores re.Pattern and represents it nicely. Use self.pattern to get re.Pattern object.
    Use self.str to get str object.
    Intended to be used in an immutable way; don't change pattern or str after creating.

    pattern: str or re.Pattern object
        will be compiled to re.Pattern object if str.
    '''
    # note: ideally, would've just subclassed re.Pattern.
    #   However, that seems to fail due to re.Pattern implementation.
    def __init__(self, pattern):
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.pattern = pattern
        self.str = pattern.pattern

    def match(self, s, *args_match, **kw_match):
        '''returns self.pattern.match(s, *args, **kw). Equivalent to re.match(self.pattern, s, ...).'''
        return self.pattern.match(s, *args_match, **kw_match)

    def fullmatch(self, s, *args_fullmatch, **kw_fullmatch):
        '''returns self.pattern.fullmatch(s, *args, **kw). Equivalent to re.fullmatch(self.pattern, s, ...).'''
        return self.pattern.fullmatch(s, *args_fullmatch, **kw_fullmatch)

    # # # EQUALITY & HASHING # # #
    def __eq__(self, other):
        '''return whether self and other are equal.
        equal if both are Pattern objects with the same str.
        [TODO] also allow pattern == s if isinstance(s,str) and s == pattern.str?
        '''
        if not isinstance(other, Pattern):
            return False
        return self.str == other.str

    def __hash__(self):
        '''return hash for self: hash((type(self), self.str))'''
        return hash((type(self), self.str))
        
    # # # DISPLAY # # #
    def __repr__(self):
        return f'{type(self).__name__}({self.str!r})'


''' --------------------- DecoratingCalcs/Vars/Patterns/Setters --------------------- '''

class DecoratingCalcs():
    '''Decorating functions to put loadable quantities into a dict (self.known_calcs).

    known_calcs: None or dict
        will store known calcs; dict of {name: LoadableQuantity} pairs.

    Not intended for direct use; see DecoratingVars or DecoratingPatterns instead.
    '''
    loadable_quantity_cls = LoadableQuantity  # class used for making new LoadableQuantity instances.

    def __init__(self, known_calcs=None):
        if known_calcs is None: known_calcs = dict()
        self.known_calcs = known_calcs

    def track_f(self, f, *, name=None, deps=[], aliases=[],
                  dims=None, load_across_dims=None, ignores_dims=[], reduces_dims=[]):
        '''add f to self.known_calcs as a LoadableQuantity.
        See help(self.decorator) for details on parameters.
        '''
        fname = f.__name__
        if name is None:
            START = 'get_'
            assert fname.startswith(START), f'f.__name__ must start with "{START}"'
            varname = fname[len(START):]
        else:
            varname = name
        lq = self.loadable_quantity_cls(fname, deps=deps, dims=dims,
                                        ignores_dims=ignores_dims, reduces_dims=reduces_dims)
        if getattr(self, 'cls_associated_with', None) is not None:
            lq.cls_where_defined = self.cls_associated_with
        self.known_calcs[varname] = lq
        for alias in aliases:
            self.known_calcs[alias] = lq

    @format_docstring(**_paramdocs, sub_indent=DEFAULTS.TAB)
    def decorator(self, *, name=None, deps=[], aliases=[],
                  dims=None, load_across_dims=None, ignores_dims=[], reduces_dims=[]):
        '''returns decorator for quant calculator f(self, *args, **kw), which returns f unchanged...
        but also sets self.known_calcs[name] = LoadableQuantity(f.__name__, deps=deps)
            (note - actually uses self.loadable_quantity_cls instead of LoadableQuantity)

        name: None or str
            if provided, tells name of this quantity (i.e., the key in self.known_calcs)
            None --> use {{name}} from f.__name__ which looks like "get_{{name}}".
        deps: {deps}
        aliases: list
            if any aliases are provided, also add, for alias in aliases:
                self.known_calcs[alias] = self.known_calcs[name]
        dims: {dims}
        load_across_dims: None or list of strings
            if provided, the returned decorator(f) will actually wrap f to use load_across_dims:
                result(f)(self, ...) returns self.load_across_dims(f, ..., dims=load_across_dims).
            To indicate dim dependencies without adjusting f, use kwarg `dims`, instead.
        ignores_dims: {ignores_dims}
        reduces_dims: {reduces_dims}
        '''
        # check for input conflicts:
        if load_across_dims is not None:
            if dims is not None:
                errmsg = f'cannot provide both dims={dims!r} and load_across_dims={load_across_dims!r}.'
                raise InputConflictError(errmsg)
            if any(d in ignores_dims for d in load_across_dims):
                errmsg = (f'ignores_dims cannot include any of the same dims as load_across_dims, but got: '
                          f'ignores_dims={ignores_dims!r} and load_across_dims={load_across_dims!r}.')
                raise InputConflictError(errmsg)
        # result (if load_across_dims is None)
        def return_f_after_some_bookkeeping(f):
            '''returns f, unchanged, after calling self.track_f(f, ...) to add it to self.known_calcs.
            (Also adds aliases to self.known_calcs if provided; see help(DecoratingCalcs) for details)
            '''
            self.track_f(f, name=name, deps=deps, aliases=aliases,
                         dims=dims, ignores_dims=ignores_dims, reduces_dims=reduces_dims)
            return f
        # return result (immediately, if load_across_dims is None):
        if load_across_dims is None:
            return return_f_after_some_bookkeeping
        else:  # do more things before returning result.
            dims = load_across_dims
            def direct_decorator(f):
                '''returns a decorator for f, which wraps f to use load_across_dims,
                after calling self.track_f(f, ...)
                '''
                f = return_f_after_some_bookkeeping(f)
                @functools.wraps(f)
                def f_but_load_across_dims(self_, *args, **kw):
                    '''f but using load_across_dims.'''
                    __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
                    # self_ gets passed as an arg because f is the method before it is bound to self_.
                    with self_.using(ncpu=1, pool=None):
                        # ncpu=1, pool=None is necessary because f (going to load_across_dims) is not pickleable!
                        # that's because the f going to load_across_dims is the f before applying the decorator,
                        #   but the module-level (or class-level) f is the output of the decorator
                        #   (which is a different object from the f inside here)
                        #   and pickle only works on module-level or class-level objects.
                        return self_.load_across_dims(f, self_, *args, dims=dims, **kw)
                return f_but_load_across_dims
            return direct_decorator

    def __repr__(self):
        return f'{type(self).__name__}({self.known_calcs})'


class DecoratingVars(DecoratingCalcs):
    '''Decorating functions to put loadable vars into a dict (self.known_calcs).
    (e.g., self.known_calcs will be QuantityLoader.KNOWN_VARS; see MetaQuantTracking for details.)

    known_calcs: None or dict
        will store known calcs; dict of {name: LoadableVar} pairs.

    Example: known_var = DecoratingCalcs(storage_dict)
        @known_var
        def get_var1(...):
            ...
        @known_var(name='coolvar', deps=['var1'])
        def get_var2(...):
            ...
        # at this point, we have:
        #   known_var.known_calcs == {'var1': LoadableQuantity('get_var1'),
        #                             'coolvar': LoadableQuantity('get_var2', deps=['var1'])}.
    '''
    loadable_quantity_cls = LoadableVar  # class used for making new LoadableQuantity instances.
    
    def __call__(self, f=None, *, name=None, deps=[], aliases=[],
                 dims=None, load_across_dims=None, ignores_dims=[], reduces_dims=[], **kw_decorator):
        '''if f is provided, return self.decorator(**kw)(f). Otherwise, return self.decorator(**kw).
        This enables instances to be used as decorators directly, i.e. "@self",
            or used as decorators after providing kwargs, e.g. "@self(name='varname', deps=['var2'])"
        See help(type(self)) for examples.
        '''
        kw = dict(name=name, deps=deps, aliases=aliases, dims=dims,
                  load_across_dims=load_across_dims, ignores_dims=ignores_dims, reduces_dims=reduces_dims,
                  **kw_decorator)
        if f is None:
            return self.decorator(**kw)
        else:
            return self.decorator(**kw)(f)


class DecoratingPatterns(DecoratingCalcs):
    '''DecoratingVars but for patterns; name should be an re.Pattern (or str; and will apply re.compile()),
    and decorated functions will always be provided a value for kwarg _match=re.match(name, var).

    deps values might contain ints; that indicates the dependency is at that group index.
    E.g. '(.*)_([xyz])' would put deps=[0] since it matches {var}_{x} and depends on {var}.
    '''
    loadable_quantity_cls = LoadablePattern  # class used for making new LoadableQuantity instances.

    def decorator(self, name=None, deps=[], *, aliases=[],
                  dims=None, load_across_dims=None, ignores_dims=[], reduces_dims=[]):
        '''decorates f(self, var, *, _match=None) like DecoratingCalcs.decorator, but also:
            - name is treated as a Pattern (re.compile() it if necessary)
            - returned function will determine _match via Pattern.fullmatch, if necessary.
                (This way, the function can be called directly, though that is usually discouraged.)
        '''
        pattern = Pattern(name)
        kw_decorator = dict(deps=deps, aliases=aliases,
                            dims=dims, load_across_dims=load_across_dims,
                            ignores_dims=ignores_dims, reduces_dims=reduces_dims,)
        def direct_decorator(f):
            @super(DecoratingPatterns, self).decorator(name=pattern, **kw_decorator)
            @functools.wraps(f)
            def f_with_match_provided(self_, var, *, _match=None, **kw):
                __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
                if _match is None:
                    _match = pattern.fullmatch(var)
                    if _match is None:
                        # (var doesn't match pattern. Probably called f directly, instead of self(var))
                        raise InputError(f'var={var!r} does not match pattern {pattern!r}.')
                return f(self_, var, _match=_match, **kw)
            return f_with_match_provided
        return direct_decorator

    __call__ = alias('decorator')


class DecoratingSetters():
    '''Decorating functions to put them into a dict (self.known_setters).

    known_setters: None or dict
        will store known settables; dict of {name: callable}

    Example: known_setter = DecoratingCalcs(storage_dict)
        @known_setter
        def set_var1(...):
            ...
        @known_setter(name='coolvar')
        def set_var2(...):
            ...
        # at this point, we have:
        #   known_setter.known_setters == {'var1': set_var1, 'coolvar': set_var2}.

    '''
    def __init__(self, known_setters=None):
        if known_setters is None: known_setters = dict()
        self.known_setters = known_setters

    def decorator(self, name=None):
        '''returns decorator for quant setter f(self, *args, **kw), which returns f unchanged...
            but also, tracks things appropriately:
                add name to self.known_setters,
        if name is not provided, use {name} from f.__name__ which looks like "set_{name}".
        '''
        def return_f(f):
            '''returns f, unchanged, after adding name to self.setters'''
            if name is None:
                START = 'set_'
                fname = f.__name__
                assert fname.startswith(START), f'f.__name__ must start with "{START}"'
                varname = fname[len(START):]
            else:
                varname = name
            self.known_setters[varname] = f
            return f
        return return_f

    def __call__(self, f=None, *, name=None):
        '''if f is provided, return self.decorator(**kw)(f). Otherwise, return self.decorator(**kw).
        This enables instances to be used as decorators directly, i.e. "@self",
            or used as decorators after providing kwargs, e.g. "@self(name='varname', deps=['var2'])"
        See help(type(self)) for examples.
        '''
        if f is None:
            return self.decorator(name)
        else:
            return self.decorator(name)(f)

    def __repr__(self):
        return f'{type(self).__name__}({self.known_setters})'


''' --------------------- CallDepthMixin --------------------- '''

class CallDepthMixin():
    '''Mixin class for tracking call depth.
    call depth == number of times self has been called inside other calls to self.
    see help(type(self).call_depth) for details.

    subclasses should include "with self._increment_call_depth():" inside of __call__, e.g.:
        def __call__(self, *args, **kw):
            with self._increment_call_depth():
                # do stuff; possibly including calling self again.
    '''
    @property
    def call_depth_manager(self):
        '''stores the value of call_depth, and helps to manage attrs dependent on call_depth value.'''
        try:
            result = self._call_depth_manager
        except AttributeError:
            result = IncrementableAttrManager(self, default=0, step=1)
            self._call_depth_manager = result
        return result

    @property
    def call_depth(self):
        '''depth of the current call to self. depth = number of calls to self from within self.

        E.g., call_depth while calculating gyrofrequency:
            # call_depth == 0, for any code run here (outside any call to self).
            self('gyrof')
                # call_depth == 1, for any code run here (inside 'gyrof' call but not inside deeper calls).
                q = self('q') 
                    # call_depth == 2, for code inside 'q' call.
                mod_B = self('mod_B')
                    # call_depth == 2, for code inside 'mod_B' call.
                    self('B')
                        # call_depth == 3, for code inside 'B' call.
                m = self('m')
                    # call_depth == 2, for code inside 'm' call.
                result = q * mod_B / m

        Cannot be set directly; can only be manipulated via self.call_depth_manager.
        '''
        return int(self.call_depth_manager)

    def _increment_call_depth(self):
        '''context manager for incrementing call_depth.

        use "with self._increment_call_depth():" inside of __call__, e.g.:
            def __call__(self, *args, **kw):
                with self._increment_call_depth():
                    # do stuff; possibly including calling self again.

        Equivalent to self.call_depth_manager.increment()
        '''
        return self.call_depth_manager.increment()        

    def using_at_call_depth(self, depth, **attrs_and_values):
        '''context manager for setting attrs_and_values but only while call_depth == depth.

        E.g.:
            with self.using_at_call_depth(3, verbose=3):
                self('sgyrof')
                # while self.call_depth == 3 inside of this 'with' block, uses self.verbose=3.
                #   but everywhere else, uses original value of verbose.
            # assuming originally verbose=False (or unset), this example will print:
            | | (call_depth=2) get var='q'
            | | (call_depth=2) get var='mod_B'
            | | (call_depth=2) get var='m'
            
            # compare this to simply using self.verbose=3, which would print:
            | (call_depth=1) get var='sgyrof'
            | | (call_depth=2) get var='q'
            | | (call_depth=2) get var='mod_B'
            | | | (call_depth=3) get var='B_dot_B'
            | | | | (call_depth=4) get var='B_xyz'
            | | | | | (call_depth=5) get var='B'
            | | (call_depth=2) get var='m'

        Equivalent to self.call_depth_manager.using_obj_attrs_at(depth, **attrs_and_values)
        '''
        return self.call_depth_manager.using_obj_attrs_at(depth, **attrs_and_values)

    def using_at_next_call_depth(self, **attrs_and_values):
        '''context manager for setting attrs_and_values but only while call_depth == self.call_depth + 1

        Equivalent to self.using_at_call_depth(self.call_depth + 1, **attrs_and_values).
        (Also equivalent to self.call_depth_manager.using_obj_attrs_at_next(**attrs_and_values).)
        '''
        return self.using_at_call_depth(self.call_depth + 1, **attrs_and_values)
