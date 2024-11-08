"""
File Purpose: tools related to plotting images or 3D data (e.g. imshow, pcolormesh)
"""
import inspect

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from .labels import xarray_title_plot_node
from .movies import MoviePlotElement, MoviePlotNode
from .plot_settings import PlotSettings
from .plot_tools import (
    update_vlims, set_margins_if_provided, set_lims_if_provided,
    PlotDimsMixin,
    current_axes_or_None, current_figure_exists,
) 
from .subplots import Subplots
from ..errors import (
    InputError, InputConflictError,
    PlottingAmbiguityError, MappableNotFoundError,
    DimensionKeyError,
)
from ..tools import (
    alias_key_of, alias_child, simple_property, simple_setdefault_property,
    format_docstring,
    UNSET,
    pcArrayAccessor,
)

from ..defaults import DEFAULTS


''' --------------------- ImagePlotElement & Image --------------------- '''

_paramdocs_ax = {
    'ax': '''None or Axes
        the attached mpl.axes.Axes object.
        None --> will use self.ax=plt.gca() when getting self.ax for the first time.''',
}

@PlotSettings.format_docstring(**_paramdocs_ax)
class ImagePlotElement(MoviePlotElement):
    '''image on an Axes.
    "image" refers to a matplotlib.cm.ScalarMappable object, e.g. the result of imshow or pcolormesh.

    array: array-like object, probably ndim=2.
        the data to be plotted. will be stored in self.data['array']
    ax: {ax}
    image_mode: {image_mode}

    Additional kwargs can be any PlotSettings; see help(self.plot_settings) for details.
    '''
    def __init__(self, array, *, ax=None,
                 image_mode=PlotSettings.default('image_mode'),  # <- could go in kw_super, but explicit is nice.
                  **kw_super):
        super().__init__(image_mode=image_mode, **kw_super)
        self._ax_init = ax
        self.array = array
        self.init_im()

    array = alias_key_of('data', 'array', doc='''array for plot. Internally, stored at self.data['array']''')
    im = simple_property('_im', doc='''the image object (instance of matplotlib.cm.ScalarMappable)''')
    ax = alias_child('im', 'axes', if_no_child=None, doc='''the axes containing this image''')
    fig = alias_child('ax', 'figure', if_no_child=None, doc='''figure containing this image''')

    # # # PLOTTING THIS ELEMENT # # #
    def init_im(self):
        '''initialize image; actually plot the data.
        stores plotted object in self.im & returns self.im.
        '''
        # plot settings / kwargs / bookkeeping
        image_mode = self.plot_settings['image_mode']
        settings_key_lookup = {'pcolormesh': 'plt.pcolormesh', 'imshow': 'plt.imshow'}
        if image_mode not in settings_key_lookup:
            raise InputError(f'invalid image_mode: {image_mode!r}, expected "pcolormesh" or "imshow".')
        settings_key = settings_key_lookup[image_mode]
        kw_plot = self.plot_settings.get_mpl_kwargs(settings_key)
        kw_plot = update_vlims(self.array, kw_plot)
        # ax to use for plot
        ax = self._ax_init
        if ax is None:
            ax = plt.gca()
        # make plot
        if image_mode == 'pcolormesh':
            self.im = ax.pcolormesh(self.array, **kw_plot)
        else:  # image_mode == 'imshow'
            self.im = ax.imshow(self.array, **kw_plot)
        return self.im

    # # # UPDATING (REQUIRED BY PARENT) # # #
    def update_data(self, data):
        '''update the plot using data['array'].
        return list of all updated matplotlib Artist objects.
        '''
        array = data['array']
        if self.plot_settings['image_mode'] == 'pcolormesh':
            self.im.set_array(array)
        else:  # image_mode == 'imshow'
            self.im.set_data(array)
        self.array = array  # <- updated for bookkeeping/consistency.
        return [self.im]

    # # # DISPLAY # # #
    def __repr__(self):
        array_info = f'{type(self.array).__name__} with shape={self.array.shape}'
        return f'{type(self).__name__}({array_info})'


@PlotSettings.format_docstring(**_paramdocs_ax)
class Image(MoviePlotNode):
    '''stores an ImagePlotElement & has methods for plotting & updating the image!
    "image" refers to a matplotlib.cm.ScalarMappable object, e.g. the result of imshow or pcolormesh.

    array: array-like object, probably ndim=3.
        the data to be plotted. will be stored in self.data['array']
    '''
    def __init__(self, *args__TODO, **kw__TODO):
        raise NotImplementedError('[TODO]: MovieImage. In the meantime, use XarrayImage.')
        # no need to implement this if willing to convert arrays to xarrays before plotting.
        # most of PlasmaCalcs works with xarrays, so code development should focus on XarrayImage.


''' --------------------- XarrayImagePlotElement & XarrayImage --------------------- '''

@PlotSettings.format_docstring(**_paramdocs_ax)
class XarrayImagePlotElement(ImagePlotElement):
    '''image on an Axes, for an xarray.DataArray.
    "image" refers to a matplotlib.cm.ScalarMappable object, e.g. the result of imshow or pcolormesh.

    array: xarray.DataArray, probably ndim=2.
        the data to be plotted.
    ax: {ax}
    image_mode: {image_mode}

    add_colorbar: {add_colorbar}
    add_labels: {add_labels}
    '''
    def __init__(self, array, *, ax=None,
                 image_mode=PlotSettings.default('image_mode'),  # <- could go in kw_super, but explicit is nice.
                 add_colorbar=PlotSettings.default('add_colorbar'),
                 add_labels=PlotSettings.default('add_labels'),
                 **kw_super):
        kw_super.update(image_mode=image_mode, add_colorbar=add_colorbar, add_labels=add_labels)
        super().__init__(array, ax=ax, **kw_super)
    
    def init_im(self):
        '''initialize image on self.ax; actually plot the data.
        stores plotted object in self.im & returns self.im.
        '''
        array = self.array
        image_mode = self.plot_settings['image_mode']
        kw_plot = self.plot_settings.get_mpl_kwargs('xarray.DataArray.plot[image]')
        kw_plot = update_vlims(array, kw_plot)
        plotter = getattr(array.plot, image_mode)  # e.g. array.plot.pcolormesh
        ax = self._ax_init
        if ax is None:
            ax = current_axes_or_None()
            if (ax is None) and (not current_figure_exists()):  # no current axes nor figure.
                kw_fig = self.plot_settings.get_mpl_kwargs('plt.figure')
                fig = plt.figure(**kw_fig)
                # ax = None, still, but plotter can now create ax on current fig as needed.
        self.im = plotter(ax=ax, **kw_plot)
        # labels
        if self.plot_settings['add_labels']:
            self.plot_labels()
        # formatting
        aspect = self.plot_settings['aspect']  # xarray plotter doesn't like 'aspect' kwarg; assign here instead.
        if aspect is not None:
            self.ax.set_aspect(aspect)
        set_margins_if_provided(self.plot_settings, ax=self.ax)
        set_lims_if_provided(self.plot_settings, ax=self.ax)
        return self.im

    def plot_labels(self):
        '''plots xlabel and ylabel from self.plot_settings.
        If xlabel or ylabel not provided:
            - use defaults from xarray's plot method.
            - if array.attrs has 'coords_units', put that in brackets, e.g. 'x [si]'.
        If they are provided, use them, but also .format(**array.attrs).
            (e.g. 'x [{units}]' becomes 'x [si]' if array.attrs['units'] == 'si')
        '''
        xlabel = self.plot_settings.get('xlabel', default=None)
        ylabel = self.plot_settings.get('ylabel', default=None)
        if xlabel is None:
            if 'coords_units' in self.array.attrs:
                coords_units = self.array.attrs['coords_units']
                xlabel = ' '.join((self.ax.get_xlabel(), f'[{coords_units}]'))
                self.ax.set_xlabel(xlabel)
        else:
            xlabel = xlabel.format(**self.array.attrs)
            self.ax.set_xlabel(xlabel)
        if ylabel is None:
            if 'coords_units' in self.array.attrs:
                coords_units = self.array.attrs['coords_units']
                ylabel = ' '.join((self.ax.get_ylabel(), f'[{coords_units}]'))
                self.ax.set_ylabel(ylabel)
        else:
            ylabel = ylabel.format(**self.array.attrs)
            self.ax.set_ylabel(ylabel)


@pcArrayAccessor.register('image')
@PlotSettings.format_docstring(**_paramdocs_ax)
class XarrayImage(MoviePlotNode, PlotDimsMixin):
    '''MoviePlotNode of an xarray.DataArray.
    stores an XarrayImagePlotElement & has methods for plotting & updating the image!
    "image" refers to a matplotlib.cm.ScalarMappable object, e.g. the result of imshow or pcolormesh.

    array: xarray.DataArray, probably ndim=3.
        the data to be plotted. if ndim=2, can still plot, but nothing to animate.
    t: None or str
        the array dimension which frames will index. E.g. 'time'.
        None -> infer from array & any other provided dimensions.
    x, y: None or str
        if provided, tells dimensions for the x, y plot axes.
        None -> infer from array & any other provided dimensions.
    ax: {ax}
    image_mode: {image_mode}
    init_plot: {init_plot}

    {kw_ax_margin}

    title: {title}
    title_font: {title_font}
    title_y: {title_y}
    title_kw: {title_kw}

    # [TODO] example
    '''
    element_cls = XarrayImagePlotElement

    def __init__(self, array, t=None, *, x=None, y=None, ax=None,
                 image_mode=PlotSettings.default('image_mode'),  # <- could go in kw_super, but explicit is nice.
                 init_plot=PlotSettings.default('init_plot'),
                 add_colorbar=PlotSettings.default('add_colorbar'),
                 add_labels=PlotSettings.default('add_labels'),
                 title=PlotSettings.default('title'),
                 **kw_super):
        self.array = array
        self.t = t
        self.x = x
        self.y = y
        self._ax_init = ax
        kw_super.update(image_mode=image_mode, init_plot=init_plot,
                        add_colorbar=add_colorbar, add_labels=add_labels,
                        title=title,
                        )
        self.plot_dims_attrs = self.plot_dims_attrs.copy()  # copy cls attr to avoid overwriting by accident
        super().__init__(**kw_super)

    # # # PROPERTIES # # #
    ax = alias_child('obj', 'ax', doc='''mpl.axes.Axes where this XarrayImage is plotted.''')
    @ax.getter
    def ax(self):  # ax=None if not self.plotted
        return self.obj.ax if self.plotted else None

    fig = alias_child('obj', 'fig', doc='''figure where this XarrayImage is plotted.''')
    @fig.getter
    def fig(self):  # fig=None if not self.plotted
        return self.obj.fig if self.plotted else None

    # # # PLOTTING METHODS (REQUIRED BY PARENT CLASS) # # #
    def init_plot(self):
        '''plot for the first time. Save the XarrayImagePlotElement at self.obj.'''
        self._init_plot_checks()
        frame = self.plot_settings['init_plot_frame']
        data = self.get_data_at_frame(frame)
        # get settings for plot
        kw_plot = self.plot_settings.get_mpl_kwargs('pc.XarrayImagePlotElement')
        # -- determine vlims (based on the entire array, not just this frame)
        kw_plot = update_vlims(self.array, kw_plot)
        # >> actually plot the image <<
        self.obj = self.element_cls(data['array'], ax=self._ax_init, **kw_plot)
        # -- if add_labels, add title:
        if self.plot_settings['add_labels']:
            self.plot_title()
        # bookkeeping
        self.frame = frame

    def get_data_at_frame(self, frame):
        '''returns {'array': array at this frame}, properly transposed & ready for plotting.'''
        t = self.t_plot_dim
        result = self.array
        if t is not None:  # there is a dimension for the time axis.
            result = result.isel({t: frame})
        x, y = self.xy_plot_dims   # (x and y are strings, the dimension names)
        result = result.transpose(y, x)   # transposed to get correct order for plotting
        return {'array': result}

    def get_nframes_here(self):
        '''return the number of frames that could be in the movie, based on this node.'''
        t = self.t_plot_dim
        if t is None:
            return 1
        return len(self.array.coords[t])

    # # # INFERRING DIMS (REQUIRED BY PARENT CLASS) # # #
    plot_dims_attrs = dict(x='x', y='y', t='t', dims='_array_dims', t_necessary_if='_array_is_not_2D')
    _array_dims = property(lambda self: self.array.dims, doc='''the dimensions of the array''')
    # x_plot_dim, y_plot_dim, t_plot_dim are already defined by PlotDimsMixin.

    def _array_is_not_2D(self):
        '''tells whether self.array is not 2D'''
        return self.array.ndim != 2

    def _has_valid_plot_dims(self):
        '''return whether this array is plottable, i.e. all plot_dims can be inferred,
        and array doesn't have more than 3 dims.'''
        if self.array.ndim > 3:
            return False
        try:
            _plot_dims = self.xyt_plot_dims
        except PlottingAmbiguityError:
            return False
        return True

    # # # TITLE # # #
    def plot_title(self):
        '''adds title (as a MovieTextNode) on self.ax.
        raise PlottingAmbiguityError if title already plotted
            (this prevents having multiple title nodes).
        '''
        if hasattr(self, 'title_node'):
            raise PlottingAmbiguityError(f'{type(self).__name__} title was already plotted!')
        title = self.plot_settings['title']
        if title is None:
            plt.title('')  # remove xarray's default title.
        else:
            kw_title = {**self.plot_settings.kw, 'init_plot': True}
            title_node = xarray_title_plot_node(self.array, title, t=self.t_plot_dim,
                                                ax=self.ax, parent=self, **kw_title)
            self.title_node = title_node  # <-- for bookkeeping/debugging
