"""
File Purpose: misc tricks related to plotting

stuff that's sometimes easy to forget, but super useful if you remember it.
"""

import matplotlib.pyplot as plt

def ax_outline(ax=None, *, color='black', linewidth=1):
    '''draw a box around the axes'''
    if ax is None:
        ax = plt.gca()
    ax.patch.set(linewidth=linewidth, edgecolor=color)

def fig_outline(fig=None, *, color='red', linewidth=1):
    '''draw a box around the figure'''
    if fig is None:
        fig = plt.gcf()
    fig.patch.set(linewidth=linewidth, edgecolor=color)

def ax_remove_ticks(ax=None):
    '''remove ticks from the axes!'''
    if ax is None:
        ax = plt.gca()
    ax.set(xticks=[], yticks=[])

def ax_remove_ticklabels(ax=None):
    '''remove ticklabels from the axes (but don't remove ticks)!'''
    if ax is None:
        ax = plt.gca()
    ax.set(xticklabels=[], yticklabels=[])

# # size of a drawn artist (e.g., textbox, axes...) # #
# artist.get_window_extent()

# # convenient locations to have for reference: # # 
PLOT_LOCATION_NAMES = \
    ''''outer upper left',    'above upper left', 'above upper center', 'above upper right', 'outer upper right',
    'outside upper left',  'upper left',       'upper center',       'upper right',       'outside upper right',
    'outside center left', 'center left',      'center',             'center right',      'outside center right',
    'outside lower left',  'lower left',       'lower center',       'lower right',       'outside lower right',
    'outer lower left',    'below lower left', 'below lower center', 'below lower right', 'outer lower right'.'''

def plot_locations(margin=0.03):
    '''dict of xy=(x,y) in axes coordinates (0=left/bottom, 1=right/top) for various locations;
    also includes nice values for ha & va to use for aligning text.

    margin: number, probably between 0 and 0.25
        margin to add to the plot locations. E.g. use 0+margin for bottom instead of 0.

    The locations are as follows, with outer/above/outside/below referring to locations outside the axes.
    'outer upper left',    'above upper left', 'above upper center', 'above upper right', 'outer upper right',
    'outside upper left',  'upper left',       'upper center',       'upper right',       'outside upper right',
    'outside center left', 'center left',      'center',             'center right',      'outside center right',
    'outside lower left',  'lower left',       'lower center',       'lower right',       'outside lower right',
    'outer lower left',    'below lower left', 'below lower center', 'below lower right', 'outer lower right'.
    '''
    result = {
        # inside the axes:
        'upper left':   dict(xy=(0+margin, 1-margin), ha='left',   va='top'),
        'upper center': dict(xy=(0.5     , 1-margin), ha='center', va='top'),
        'upper right':  dict(xy=(1-margin, 1-margin), ha='right',  va='top'),
        'center left':  dict(xy=(0+margin, 0.5     ), ha='left',   va='center'),
        'center':       dict(xy=(0.5     , 0.5     ), ha='center', va='center'),
        'center right': dict(xy=(1-margin, 0.5     ), ha='right',  va='center'),
        'lower left':   dict(xy=(0+margin, 0+margin), ha='left',   va='bottom'),
        'lower center': dict(xy=(0.5     , 0+margin), ha='center', va='bottom'),
        'lower right':  dict(xy=(1-margin, 0+margin), ha='right',  va='bottom'),
        # outside the axes - top row:
        'outer upper left':     dict(xy=(0-margin, 1+margin), ha='right',  va='bottom'),
        'above upper left':     dict(xy=(0+margin, 1+margin), ha='left',   va='bottom'),
        'above upper center':   dict(xy=(0.5     , 1+margin), ha='center', va='bottom'),
        'above upper right':    dict(xy=(1-margin, 1+margin), ha='right',  va='bottom'),
        'outer upper right':    dict(xy=(1+margin, 1+margin), ha='left',   va='bottom'),
        # outside the axes - left & right columns
        'outside upper left':   dict(xy=(0-margin, 1-margin), ha='right',  va='top'),
        'outside upper right':  dict(xy=(1+margin, 1-margin), ha='left',   va='top'),
        'outside center left':  dict(xy=(0-margin, 0.5     ), ha='right',  va='center'),
        'outside center right': dict(xy=(1+margin, 0.5     ), ha='left',   va='center'),
        'outside lower left':   dict(xy=(0-margin, 0+margin), ha='right',  va='bottom'),
        'outside lower right':  dict(xy=(1+margin, 0+margin), ha='left',   va='bottom'),
        # outside the axes - bottom row:
        'outer lower left':     dict(xy=(0-margin, 0-margin), ha='right',  va='top'),
        'below lower left':     dict(xy=(0+margin, 0-margin), ha='left',   va='top'),
        'below lower center':   dict(xy=(0.5     , 0-margin), ha='center', va='top'),
        'below lower right':    dict(xy=(1-margin, 0-margin), ha='right',  va='top'),
        'outer lower right':    dict(xy=(1+margin, 0-margin), ha='left',   va='top'),
        }
    return result

def plot_note(note, xy='upper left', *, margin=0.03, **kw_annotate):
    '''add this note to the current plot at the indicated position.
    For more detailed control, use plt.annotate instead.

    xy: str or tuple
        position in axes coords.
        str -> also sets horizontal & vertical alignment (via 'ha' & 'va' kwargs).
        See below for valid strings.
    margin: number, probably between 0 and 0.25
        margin to add to the plot locations. E.g. use 0+margin for bottom instead of 0.

    Valid strings are (with outer/above/outside/below being outside the axes):
    'outer upper left',    'above upper left', 'above upper center', 'above upper right', 'outer upper right',
    'outside upper left',  'upper left',       'upper center',       'upper right',       'outside upper right',
    'outside center left', 'center left',      'center',             'center right',      'outside center right',
    'outside lower left',  'lower left',       'lower center',       'lower right',       'outside lower right',
    'outer lower left',    'below lower left', 'below lower center', 'below lower right', 'outer lower right'.
    '''
    defaults = plot_locations(margin=margin)
    if isinstance(xy, str):
        if xy not in defaults:
            raise ValueError(f"Invalid xy string: {xy!r}. Expected one of:\n    {PLOT_LOCATION_NAMES}")
        kw_annotate = {**defaults[xy], **kw_annotate}
    else:
        kw_annotate['xy'] = xy
    kw_annotate.setdefault('xycoords', 'axes fraction')
    return plt.annotate(note, **kw_annotate)
