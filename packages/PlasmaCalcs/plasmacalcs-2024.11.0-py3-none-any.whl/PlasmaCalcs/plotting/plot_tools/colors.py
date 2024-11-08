"""
File purpose: tools related to colors (see also: colorbar.py)

End-users: see help(PlasmaCalcs.get_cmap); you'll probably just use that function.
"""

import collections

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


from ...tools import (
    simple_setdefault_property,
    NO_VALUE,
)
from ...errors import InputConflictError


''' --------------------- BaseColormap --------------------- '''

ColormapExtremes = collections.namedtuple('ColormapExtremes', ('under', 'over', 'bad'))

class BaseColormap(mpl.colors.Colormap):
    '''matplotlib.colors.Colormap class with more methods, and some properties.'''
    def __init__(self, *args_super, **kw_super):
        super().__init__(*args_super, **kw_super)
        self._default_extremes = self.extremes

    # # # PROPERTIES / METHODS FOR HANDLING EXTREMES # # #
    colorbar_extend_settings = simple_setdefault_property('_colorbar_extend_settings', dict,
            doc='''the current dict(under=bool, over=bool) corresponding to colorbar_extend.''')

    @property
    def colorbar_extend(self):
        '''defaults instructions for whether to extend colorbars using this colormap.
        One of the following values:
            'neither' --> do not extend colorbar.
            'both' --> extend colorbar in both directions.
            'min' --> extend colorbar in the direction of the minimum value.
            'max' --> extend colorbar in the direction of the maximum value.
        When setting self.colorbar_extend=value, value can be:
            str --> use value (must be 'neither', 'both', 'min', or 'max').
            True --> use 'both'
            False --> use 'neither'
        '''
        settings = self.colorbar_extend_settings
        under = settings.get('under', False)
        over = settings.get('over', False)
        if under and over: return 'both'
        elif under: return 'min'
        elif over: return 'max'
        else: return 'neither'
    @colorbar_extend.setter
    def colorbar_extend(self, value):
        '''set the value of colorbar_extend. See help(type(self).colorbar_extend) for details.'''
        if value is True:
            value = 'both'
        elif value is False:
            value = 'neither'
        if value not in ('neither', 'both', 'min', 'max'):
            raise ValueError(f'invalid value for colorbar_extend: {value}')
        settings = self.colorbar_extend_settings
        if value == 'both':
            settings['under'], settings['over'] = True, True
        elif value == 'min':
            settings['under'], settings['over'] = True, False
        elif value == 'max':
            settings['under'], settings['over'] = False, True
        elif value == 'neither':
            settings['under'], settings['over'] = False, False

    under = property(lambda self: self.get_under(),
                     lambda self, val: self.set_under(val),
            doc='''the color for low out-of-range values.
            when setting self.under = value, value can be:
                str --> use this color.
                None --> use the default color (bottom of the colormap).
                if not None, also sets self.colorbar_extend_settings['under'],
                    to True if (str or True), else False.''')
    def set_under(self, color=None, alpha=None, **kw_super):
        '''set the color for low out-of-range values. See help(type(self).under) for details.'''
        color_bool = True if not (color is None or color is False) else color
        if any(color is b_ for b_ in (None, True, False)):
            color = self._default_extremes.under
        super().set_under(color, alpha, **kw_super)
        if isinstance(color_bool, bool):
            self.colorbar_extend_settings['under'] = color_bool

    over = property(lambda self: self.get_over(),
                    lambda self, val: self.set_over(val),
                    lambda self: self.del_over(),
            doc='''the color for high out-of-range values.
            when setting self.over = value, value can be:
                str --> use this color.
                None or bool --> use the default color (top of the colormap).
                if not None, also sets self.colorbar_extend_settings['over'],
                    to True if (str or True), else False.''')
    def set_over(self, color=None, alpha=None, **kw_super):
        '''set the color for high out-of-range values. See help(type(self).over) for details.'''
        color_bool = True if not (color is None or color is False) else color
        if any(color is b_ for b_ in (None, True, False)):
            color = self._default_extremes.over
        super().set_over(color, alpha, **kw_super)
        if isinstance(color_bool, bool):
            self.colorbar_extend_settings['over'] = color_bool

    bad = property(lambda self: self.get_bad(),
                   lambda self, val: self.set_bad(val),
                   lambda self: self.del_bad(),
            doc='''the color for masked values. Use self.bad=None to restore default.''')
    def set_bad(self, color=None, alpha=None, **kw_super):
        '''set the color for masked values. See help(type(self).bad) for details.'''
        if color is None:
            color = self._default_extremes.bad
        super().set_bad(color, alpha, **kw_super)

    extremes = property(lambda self: self.get_extremes(),
                        lambda self, value: self._set_extremes_implied(),
            doc='''(under, over, bad), as a ColormapExtremes namedtuple.
            setting self.extremes = value is possible, but to avoid ambiguity:
                value must have keys "under", "over", and/or "bad",
                or attributes "under", "over", and/or "bad".
            e.g. self.extremes = dict(under='blue')
                (equivalent to self.under='blue')
            Use None to reset to default, e.g. self.extremes = None,
                (equivalent to self.under=None, self.over=None, self.bad=None)
            or for any keys, e.g. self.extremes = dict(under='blue', over=None)
                (equivalent to self.under='blue', self.over=None, but not adjusting self.bad)''')

    def get_extremes(self):
        '''return (under, over, bad) colors, as a ColormapExtremes namedtuple.'''
        return ColormapExtremes(self.under, self.over, self.bad)

    def _set_extremes_implied(self, extremes):
        '''set under, over, bad colors, based on extremes. see help(type(self).extremes) for details.'''
        if extremes is None:
            self.set_extremes(under=None, over=None, bad=None)
            return
        has_keys = False
        result = dict()
        # check keys, first
        for under in ('under', 'over', 'bad'):
            try:
                val = extremes[under]
            except (KeyError, TypeError):
                pass
            else:
                result[under] = val
                has_keys = True
        if not has_keys:
            # check attrs (only if no keys were found)
            for under in ('under', 'over', 'bad'):
                try:
                    under = getattr(extremes, key)
                except AttributeError:
                    pass
                else:
                    result[key] = under
        self.set_extremes(**result)

    def set_extremes(self, *, under=NO_VALUE, over=NO_VALUE, bad=NO_VALUE):
        '''set under, over, bad colors, based on keywords.
        see help(type(self).extremes) for details.
        '''
        if under is not NO_VALUE:
            self.set_under(under)
        if over is not NO_VALUE:
            self.set_over(over)
        if bad is not NO_VALUE:
            self.set_bad(bad)

    def __copy__(self):
        '''return a copy of self. (used by self.copy()'''
        result = super().__copy__()
        result._default_extremes = self._default_extremes
        result.colorbar_extend_settings = self.colorbar_extend_settings.copy()
        return result

    # # # DISPLAY # # #
    def _repr_contents(self):
        '''return list of contents to go in repr of self.'''
        contents = []
        if self.name is not None:
            contents.append(f'name={self.name!r}')
        if self.N is not None:
            contents.append(f'N={self.N}')
        if self.colorbar_extend != 'neither':
            contents.append(f'colorbar_extend={self.colorbar_extend!r}')
        if not np.all(self.under == self._default_extremes.under):
            contents.append(f'under={self.under!r}')
        if not np.all(self.over == self._default_extremes.over):
            contents.append(f'over={self.over!r}')
        if not np.all(self.bad == self._default_extremes.bad):
            contents.append(f'bad={self.bad!r}')
        return contents

    def __repr__(self):
        '''return repr(self)'''
        contents = ", ".join(self._repr_contents())
        return f'{type(self).__name__}({contents})'


''' --------------------- Colormap (from ListedColormap) --------------------- '''

class Colormap(BaseColormap, mpl.colors.ListedColormap):
    '''matplotlib.colors.ListedColormap with some extra methods.
    
    under: NO_VALUE, None, str, or other specifier for a color.
        the color for low out-of-range values.
        if provided (not NO_VALUE), sets self.under = under.
    over: NO_VALUE, None, str, or other specifier for a color.
        the color for high out-of-range values.
        if provided (not NO_VALUE), sets self.over = over.
    bad: NO_VALUE, None, str, or other specifier for a color.
        the color for masked values.
        if provided (not NO_VALUE), sets self.bad = bad.

    see help(mpl.colors.ListedColormap) for more details on __init__.
    '''
    # # # CREATION / INITIALIZATION # # #
    def __init__(self, *args_super, under=NO_VALUE, over=NO_VALUE, bad=NO_VALUE, **kw_super):
        super().__init__(*args_super, **kw_super)
        self.set_extremes(under=under, over=over, bad=bad)

    @classmethod
    def from_cmap(cls, cmap, **kw):
        '''return Colormap from cmap.
        cmap: Colormap or matplotlib.colors.ListedColormap
            [TODO] or matplotlib.colors.LinearSegmentedColormap
        additional kwargs go to cls.__new__ and cls.__init__.
        '''
        if kw.get('under', NO_VALUE) is NO_VALUE: kw['under'] = cmap.get_under()
        if kw.get('over',  NO_VALUE) is NO_VALUE: kw['over']  = cmap.get_over()
        if kw.get('bad',   NO_VALUE) is NO_VALUE: kw['bad']   = cmap.get_bad()
        try:
            colors = cmap.colors
        except AttributeError:  # LinearSegmentedColormap...
            colors = cmap(np.linspace(0, 1, cmap.N))
        return cls(colors, name=cmap.name, N=cmap.N, **kw)

    @classmethod
    def get_cmap(cls, based_on=None, N=None, *, colors=None, name=None, reversed=False,
                 under=NO_VALUE, over=NO_VALUE, bad=NO_VALUE,
                 **kw_init):
        '''Get a Colormap instance, possibly based on a default colormap from matplotlib.
        based_on: matplotlib.colors.Colormap, str, or None
            the colormap to base the result on.
            None --> use the default colormap (from matplotlib rc; image.cmap)
                    (or, if colors are provided, use colors to make a new colormap instead).
            str --> use the colormap with this name from matplotlib.
                    (or, if colors are provided, set this to the name of the new colormap).
            Colormap --> base the result on this colormap.
                    (mutually exclusive with providing a value for colors)
        N: None or int
            number of colors to use.
            None --> use the number of colors in based_on.
            int --> resample to this many colors.
        colors: None or array-like of colors
            None --> ignore this parameter
            array-like --> provide these to make a new Colormap.
                    (mutually exclusive with providing a Colormap for based_on)
        name: None or str
            the name for the new Colormap.
            if None, infer name from the old colormap or the provided value of based_on.
        reversed: bool
            whether to return result.reversed(), instead.
        under: NO_VALUE, None, str, or other specifier for a color.
            the color for low out-of-range values.
            if provided (not NO_VALUE), sets result.under = under.
        over: NO_VALUE, None, str, or other specifier for a color.
            the color for high out-of-range values.
            if provided (not NO_VALUE), sets result.over = over.
        bad: NO_VALUE, None, str, or other specifier for a color.
            the color for masked values.
            if provided (not NO_VALUE), sets result.bad = bad.
        
        additional kwargs are passed to cls(...) when creating the result.
        '''
        if based_on is None:
            base_name, base_cmap = None, None
        elif isinstance(based_on, str):
            base_name, base_cmap = based_on, None
        else:
            base_name, base_cmap = None, based_on
        if colors is not None and base_cmap is not None:
            raise InputConflictError('cannot provide both Colormap (for based_on) and colors.')
        if base_cmap is None:
            # get matplotlib colormap
            if colors is None:
                base_cmap = plt.get_cmap(base_name, N)
            else:
                base_cmap = mpl.colors.ListedColormap(colors, name=base_name, N=N)
        result = cls.from_cmap(base_cmap, under=under, over=over, bad=bad, **kw_init)
        if name is not None:
            result.name = name
        if N is not None:
            result = result.resampled(N)
        if reversed:
            result = result.reversed()
        return result

    # # # matplotlib isn't nice about subclassing, so we must redefine methods here: # # #
    def resampled(self, N, **kw__super):
        '''return a copy of self, resampled to size N.'''
        result = super().resampled(N, **kw__super)
        return self.from_cmap(result)

    def reversed(self, name=None, **kw__super):
        '''return a copy of self, with reversed colors.
        if name is None, use name = self.name + "_r".
        '''
        result = super().reversed(name=name, **kw__super)
        return self.from_cmap(result)

    def at(self, fractions):
        '''return copy of self but only keep colors at self(fractions).
        E.g. self.at([0.1, 0.5, 0.9]) gives cmap with N=3,
            and colors at 10%, 50%, and 90% of the way along self.
        '''
        colors = self(fractions)
        self_attrs = dict(name=self.name, under=self.under, over=self.over, bad=self.bad)
        return type(self)(colors, N=len(fractions), **self_attrs)

    def shrink(self, min=0, max=1, N=None):
        '''return copy of self but only keep colors between min and max.
        E.g. self.shrink(0.2, 0.7) only keeps colors between 20% and 70% of the way along self.
        N: None or int
            number of colors to use for the result.
            None --> keep similar spacing of colors as in self
        '''
        if not (0 <= min <= max <= 1):
            raise ValueError(f'expect 0 <= min <= max <= 1, but got min={min}, max={max}')
        if N is None:
            N = int(self.N * (max - min))  # [TODO] maybe +-1 to get to same exact spacing as self.
        colors = self(np.linspace(min, max, N))
        self_attrs = dict(name=self.name, under=self.under, over=self.over, bad=self.bad)
        return type(self)(colors, N=N, **self_attrs)


cmap = Colormap.get_cmap  # alias to Colormap.get_cmap
get_cmap = Colormap.get_cmap  # alias to Colormap.get_cmap