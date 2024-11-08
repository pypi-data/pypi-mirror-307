"""
File Purpose: various extensions to the Subplots class
"""
import numpy as np
import xarray as xr

from .images import XarrayImage
from .labels import XarraySubplotTitlesInferer, xarray_suptitle_plot_node
from .movies import MoviePlotNode, MovieOrganizerNode, EmptyMovieNode
from .plot_settings import PlotSettings
from .plot_tools import calculate_vlims
from .subplots import Subplots
from ..errors import InputError, InputConflictError, PlottingAmbiguityError
from ..tools import (
    alias, alias_child,
    UNSET,
    pcAccessor, take_along_dimensions,
    Tree,
)


@PlotSettings.format_docstring()
class MovieSubplots(MovieOrganizerNode, Subplots):
    '''MoviePlotNode for organizing a grid of subplots.
    Expects input 2D array (or nested list) or MoviePlotNodes,
        which were all created with init_plot=False
        (to allow MovieSubplots to create & assign the axes).
        For images, probably also want nodes to use add_colorbar=False
        (to allow MovieSubplots to create & assign the colorbar(s)).

    nodes: 2D array-like of MoviePlotNode or None objects
        the MoviePlotNodes associated with each subplot.
        None --> no MoviePlotNode for that subplot.
    name: str
        name for the MovieSubplots node; to be displayed in __repr__.
    parent: None or MoviePlotNode
        if provided, the parent of this node. None -> this node has no parent.
    init_plot: {init_plot}
    add_colorbars: {add_colorbars}

    kwargs which go to Subplots:
    axsize: {axsize}
    figsize: {figsize}
    {kw_subplots_adjust}
    {kw_share_axlike}
    {kw_share_ax}
    max_nrows_ncols: {max_nrows_ncols}
    squeeze: {squeeze}

    additional kwargs go to plt.subplots.

    Roughly equivalent functionality:
        subs = subplots(..., squeeze=False)  # creates a Subplots object
        axs = subs.axs  # the grid of axes in the Subplots
        msubs = MovieOrganizerNode()
        msubs_row0 = MovieOrganizerNode(parent=msubs)
        msubs_row1 = MovieOrganizerNode(parent=msubs)
        # ... as many rows as needed.
        MoviePlotNode(..., ax=axs[0,0], parent=msubs_row0)
        MoviePlotNode(..., ax=axs[0,1], parent=msubs_row0)
        # ...
        MoviePlotNode(..., ax=axs[1,0], parent=msubs_row1)
        MoviePlotNode(..., ax=axs[1,1], parent=msubs_row1)
        # ... as many nodes as needed.
        # --> while msubs wouldn't be a MovieSubplots object,
        #     it would still provide most of the same functionality,
        #     e.g. msubs.save(...) would properly animate & save movie!
    '''
    def __init__(self, nodes, name='', *, parent=None,
                 init_plot=PlotSettings.default('init_plot'),  # <- could go in kw_super, but explicit is nice.
                 add_colorbars=PlotSettings.default('add_colorbars'),
                 **kw_super):
        nodes = np.asanyarray(nodes)
        self.nodes = nodes
        if nodes.ndim != 2:
            raise InputError(f'nodes must be 2D, got shape {nodes.shape}')
        nrows, ncols = nodes.shape

        kw_super.update(nrows=nrows, ncols=ncols,
                init_plot=init_plot,
                add_colorbars=add_colorbars,
                name=name, parent=parent)
        # MovieOrganizerNode won't accidentally init_plot before axs are created,
        #   because it has obj=None so it never calls init_plot during __init__.
        super().__init__(**kw_super)

        if self.plot_settings['init_plot']:
            self.init_plot()

    def init_plot(self):
        '''plot for the first time: call init_plot on all nodes,
        and organize into a nice tree structure which can be indexed like an array.

        This is fundamentally different from MoviePlotNode.init_plot's usual purpose,
            since this is about calling init_plot on the nodes, not on self.obj.
            [TODO] should this function be renamed, for clarity?
        '''
        # checks: skip the usual checks; init_plot on nodes, not self.obj.
        # but, do check if self.init_plot was already called; don't want to call it twice!
        if getattr(self, '_called_init_plot', False):
            errmsg = (f'init_plot was already called; cannot call it again. '
                      f'For {type(self).__name__}(name={self.name!r}) with id={hex(id(self))}')
            raise PlottingAmbiguityError(errmsg)
        # bookkeeping
        name_append = f' {self.name}' if self.name else ''
        axs = self.axs
        # call init_plots on nodes, set up row organizers, & create appropriate node tree.
        for i, row in enumerate(self.nodes):
            row_organizer = MovieOrganizerNode(name=f'(row={i}){name_append}', parent=self)
            for j, node in enumerate(row):
                if node is None:
                    node = EmptyMovieNode()
                else:
                    node._ax_init = axs[i,j]
                    node.init_plot()
                node.parent = row_organizer
        # formatting
        self.remove_redundant_labels()
        add_colorbars = self.plot_settings['add_colorbars']
        if add_colorbars:
            if self.plot_settings.get('add_colorbar', False):
                raise InputConflictError('Can add_colorbars or add_colorbar, but not both!')
            self.colorbars(mode=add_colorbars)

    # # # INHERITANCE FUNNY BUSINESS # # #
    # we want this object to behave sometimes like MoviePlotNode, sometimes like Subplots.
    # Those two classes have mostly non-overlapping methods, but there is some overlap.

    # In particular, both define methods for indexing. Here we want to use Tree-like indexing!
    __getitem__ = Tree.__getitem__
    __iter__ = Tree.__iter__
    # [TODO] if there's a "cleaner" way to do this, that might be nice...


@pcAccessor.register('subplots')
@PlotSettings.format_docstring()
class XarraySubplots(MovieSubplots):
    '''grid of subplots from xarray data. Can be animated as a movie!

    xarray: xarray.DataArray or xarray.Dataset
        the array to plot. up to 5D (row, col, x, y, t).
        (Note that row & col dims should be "not too long" otherwise plot will be very large)
        if dataset, up to 4D; will be converted to DataArray with new dim named 'variable'.
    row: None or str
        dimension to plot ACROSS rows.
        None --> subplots will have ncols=1 (nothing varies across a row --> only 1 column).
        E.g. if row=='fluid', then the i'th COLUMN will be fluid i.
        [TODO] infer row directly from xarray, somehow?
    col: None or str
        dimension to plot DOWN columns.
        None --> subplots will have nrows=1 (nothing varies down a column --> only 1 row).
        E.g. if col='component', then the j'th ROW will be component j.
    x, y: None or str
        dimension name for the x and y axes of an individual subplot.
        None --> infer from the xarray coords. See also: DEFAULTS.PLOT.DIMS_INFER
    t: None or str
        dimension name for the time axis (for movies).
        None --> infer from the xarray coords. See also: DEFAULTS.PLOT.DIMS_INFER

    vmin, vmax: None or value
        if provided, use this value for vmin, vmax for all subplots,
        and ignore share_vlims and robust.
    share_vlims: {share_vlims}
    robust: {robust}

    additional kwargs go to other places [TODO][DOC] fill in the details.
    '''
    def __init__(self, xarray, row=None, col=None, *, x=None, y=None, t=None,
                 sharexlike=True, shareylike=True, fig=None,
                 vmin=None, vmax=None,
                 robust=PlotSettings.default('robust'),  # <- could go in **kw, but explicit is nice.
                 share_vlims=PlotSettings.default('share_vlims'),
                 title=PlotSettings.default('title'),
                 title_y=PlotSettings.default('title_y'),
                 suptitle=PlotSettings.default('suptitle'),
                 suptitle_y=PlotSettings.default('suptitle_y'),
                 aspect=PlotSettings.default('aspect'),
                 layout=PlotSettings.default('layout'),
                 cax_mode=PlotSettings.default('cax_mode'),
                 axsize=PlotSettings.default('axsize'),
                 add_colorbars=PlotSettings.default('add_colorbars'),
                 **kw):
        name = '' if (getattr(xarray, 'name', None) is None) else xarray.name
        if isinstance(xarray, xr.Dataset):
            xarray = xarray.to_array(dim='variable')
        self.array = xarray
        # grid of xarray DataArrays. [col, row] order agrees with definition of row & col kwargs.
        arrs = take_along_dimensions(xarray, [col, row])
        self.arrs = arrs
        # settings -- update kw with settings which are explicitly in function call signature.
        kw.update(title=title, title_y=title_y,
                  suptitle=suptitle, suptitle_y=suptitle_y,
                  aspect=aspect, layout=layout, cax_mode=cax_mode,
                  add_colorbars=add_colorbars, axsize=axsize,
                  sharexlike=sharexlike, shareylike=shareylike,
                  share_vlims=share_vlims, robust=robust)
        init_plot_settings = PlotSettings(**kw)
        # [TODO] infer row & col plot dimensions if not provided.
        self.row_plot_dim = row
        self.col_plot_dim = col
        # vmin and vmax are handled separately in case we are sharing vlims or using robust:
        vlims_arr = self._get_vlims_arr(arrs, vmin=vmin, vmax=vmax, share_vlims=share_vlims, robust=robust)
        # create array of XarrayImage nodes (but don't init_plot or add_colorbar yet!)
        images = np.full(arrs.shape, None, dtype=object)
        for idx, arr in np.ndenumerate(arrs):
            vmin, vmax = vlims_arr[idx]
            image = XarrayImage(arr, t=t, x=x, y=y,
                                vmin=vmin, vmax=vmax,
                                init_plot=False, add_colorbar=False,
                                **kw)
            # ensure arr is 2D or 3D (with an inferred t_plot_dim); else crash with helpful message.
            if not image._has_valid_plot_dims():
                errmsg = (f'failed to infer plot dimensions; image array has dims {image.array.dims!r}.\n'
                          'Most likely, you forgot to specify row, col, x, y, and/or t.')
                raise PlottingAmbiguityError(errmsg)
            images[idx] = image
        # infer subplot titles where not provided
        self.images = images  # <-- must do this before accessing self.t_plot_dim.
        kw_infer_titles = init_plot_settings.get_mpl_kwargs('pc.XarraySubplotTitlesInferer')
        self.titles_inferer = XarraySubplotTitlesInferer(self.array, t=self.t_plot_dim,
                                        row=self.row_plot_dim, col=self.col_plot_dim,
                                        **kw_infer_titles)
        if title is PlotSettings.default('title'):
            for idx, image in np.ndenumerate(images):
                image.plot_settings['title'] = self.titles_inferer.infer_title()
        # init super
        super().__init__(images, fig=fig, name=name, **kw)  # [TODO] does non-None fig work here?

    # # # INIT PLOT # # #
    def init_plot(self):
        '''plot for the first time: call init_plot on all nodes,
        and organize into a nice tree structure which can be indexed like an array.

        This is fundamentally different from MoviePlotNode.init_plot's usual purpose,
            since this is about calling init_plot on the nodes, not on self.obj.
            [TODO] should this function be renamed, for clarity?
        '''
        super().init_plot()
        # add suptitle after super().init_plot() adds children nodes for subplots.
        if self.plot_settings['add_labels']:
            self.plot_suptitle()

    # # # PROPERTIES # # #
    images = alias('nodes')
    image0 = property(lambda self: self.images[0,0], doc='''top-left image; images[0,0].''')
    x_plot_dim = alias_child('image0', 'x_plot_dim')
    y_plot_dim = alias_child('image0', 'y_plot_dim')
    t_plot_dim = alias_child('image0', 't_plot_dim')

    # # # SUPTITLE # # #
    def plot_suptitle(self):
        '''adds suptitle (as a MovieText node)
        raise PlottingAmbiguityError if suptitle already plotted
            (this prevents having multiple suptitle nodes).
        '''
        if hasattr(self, 'suptitle_node'):
            errmsg = (f'suptitle already plotted; cannot plot it again. '
                      f'For {type(self).__name__}(name={self.name!r}) with id={hex(id(self))}')
            raise PlottingAmbiguityError(errmsg)
        suptitle = self.plot_settings['suptitle']
        if suptitle is UNSET:
            suptitle = self.titles_inferer.infer_suptitle()
        if isinstance(suptitle, str):
            kw_suptitle = {**self.plot_settings.kw, 'init_plot': True}
            suptitle_node = xarray_suptitle_plot_node(self.array, suptitle, t=self.t_plot_dim,
                                                      fig=self.fig, parent=self, **kw_suptitle)
            self.suptitle_node = suptitle_node  # <-- for bookkeeping/debugging

    # # # VLIMS # # #
    _calculate_vlims = staticmethod(calculate_vlims)

    @PlotSettings.format_docstring(ntab=2)
    def _get_vlims_arr(self, arrs=None, *, vmin=None, vmax=None, share_vlims=False, robust=UNSET):
        '''return array of vmin, vmax, for each array in arrs.
        arrs: None or array of arrays.
            if None, use self.arrs.
        vmin, vmax: None or value
            if provided, use this value for vmin, vmax for all subplots,
            and ignore share_vlims and robust.
        share_vlims: {share_vlims}
        robust: {robust}
        '''
        # bookkeeping
        if robust is UNSET: robust = PlotSettings.get_default('robust')
        kw_calc_vlims = dict(vmin=vmin, vmax=vmax, robust=robust)
        if arrs is None:
            arrs = self.arrs
        # case: vlims are already provided
        result = np.full(arrs.shape, None, dtype=object)  # array of tuples.
        if vmin is not None and vmax is not None:
            for idx, _ in np.ndenumerate(result): result[idx] = (vmin, vmax)
        # cases: need to calculate vmin and/or vmax.
        if share_vlims is True or share_vlims=='all':
            vmin, vmax = self._calculate_vlims([a.values for a in arrs.flat], **kw_calc_vlims)
            for idx, _ in np.ndenumerate(result): result[idx] = (vmin, vmax)
        elif share_vlims == 'row':
            for i, row in enumerate(arrs):
                vmin, vmax = self._calculate_vlims([a.values for a in row], **kw_calc_vlims)
                for j, _ in enumerate(row): result[i,j] = (vmin, vmax)
        elif share_vlims == 'col':
            for j, col in enumerate(arrs.T):
                vmin, vmax = self._calculate_vlims([a.values for a in col], **kw_calc_vlims)
                for i, _ in enumerate(col): result[i,j] = (vmin, vmax)
        elif not share_vlims:
            for idx, arr in np.ndenumerate(arrs):
                vmin, vmax = self._calculate_vlims(arr.values, **kw_calc_vlims)
                result[idx] = (vmin, vmax)
        else:
            raise InputError(f'invalid share_vlims: {share_vlims}, expected True, False, "all", "row", or "col".')
        return result
