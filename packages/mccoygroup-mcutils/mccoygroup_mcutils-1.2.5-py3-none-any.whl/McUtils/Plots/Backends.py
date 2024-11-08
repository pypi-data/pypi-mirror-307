"""
For now, just a super simple Enum of supported backends
Maybe in the future we'll add better support so that the backends themselves can all support a common subset
of features, but I think we'll 90% of the time just want to use MPL or VTK so who knows...
If that happens, lots of the 'if backend == MPL' stuff will change to use a Backend object
"""

__all__ = [
    "GraphicsBackend"
]

import enum, abc, contextlib, numpy as np
from ..Numputils import is_numeric

DPI_SCALING = 72

class GraphicsAxes(metaclass=abc.ABCMeta):
    """
    A wrapper to provide a canonical form for matplotlib.axes.Axes
    so that other backends can plug in cleanly
    """
    @classmethod
    def canonicalize_opts(cls, opts):
        return opts
    @abc.abstractmethod
    def remove(self, *, backend):
        ...
    @abc.abstractmethod
    def clear(self, *, backend):
        ...

    @abc.abstractmethod
    def get_plotter(self, method):
        ...

    @abc.abstractmethod
    def get_plot_label(self):
        ...
    @abc.abstractmethod
    def set_plot_label(self, val, **style):
        ...

    @abc.abstractmethod
    def get_frame_visible(self):
        ...
    @abc.abstractmethod
    def set_frame_visible(self, frame_spec):
        ...
    @abc.abstractmethod
    def get_frame_styke(self):
        ...
    @abc.abstractmethod
    def set_frame_style(self, frame_spec):
        ...
    @abc.abstractmethod
    def get_xlabel(self):
        ...
    @abc.abstractmethod
    def set_xlabel(self, val, **style):
        ...
    @abc.abstractmethod
    def get_ylabel(self):
        ...
    @abc.abstractmethod
    def set_ylabel(self, val, **style):
        ...
    @abc.abstractmethod
    def get_xlim(self):
        ...
    @abc.abstractmethod
    def set_xlim(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_ylim(self):
        ...
    @abc.abstractmethod
    def set_ylim(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_xticks(self):
        ...
    @abc.abstractmethod
    def set_xticks(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_yticks(self):
        ...
    @abc.abstractmethod
    def set_yticks(self, val, **opts):
        ...
    @abc.abstractmethod
    def get_xtick_style(self):
        ...
    @abc.abstractmethod
    def set_xtick_style(self, **opts):
        ...
    @abc.abstractmethod
    def get_ytick_style(self):
        ...
    @abc.abstractmethod
    def set_ytick_style(self, **opts):
        ...
    @abc.abstractmethod
    def set_aspect_ratio(self, ar):
        ...
    @abc.abstractmethod
    def get_bbox(self):
        ...
    @abc.abstractmethod
    def set_bbox(self, bbox):
        ...
    @abc.abstractmethod
    def get_facecolor(self):
        ...
    @abc.abstractmethod
    def set_facecolor(self, fg):
        ...
    @abc.abstractmethod
    def get_padding(self):
        ...

    @abc.abstractmethod
    def draw_line(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_disk(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_rect(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_poly(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_arrow(self, points, **styles):
        ...
    @abc.abstractmethod
    def draw_text(self, points, vals, **styles):
        ...

class GraphicsFigure(metaclass=abc.ABCMeta):
    """
    A wrapper to provide a canonical form for matplotlib.figure.Figure
    so that other backends can plug in cleanly
    """
    Axes = None
    def __init__(self, axes=None):
        self.axes = axes
    @classmethod
    def canonicalize_opts(cls, opts):
        return opts
    @abc.abstractmethod
    def create_axes(self, rows, cols, spans, **kw) -> 'GraphicsAxes':
        ...
    @abc.abstractmethod
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        ...
    def add_axes(self, ax) -> 'GraphicsAxes':
        if self.axes is None: self.axes = []
        if not isinstance(ax, self.Axes): ax = self.Axes(ax)
        self.axes.append(ax)
        return ax
    @abc.abstractmethod
    def clear(self, *, backend):
        ...
    @abc.abstractmethod
    def close(self, *, backend):
        ...

    def get_bboxes(self):
        return [
            a.get_bbox() for a in self.axes
        ]

    @abc.abstractmethod
    def get_size_inches(self):
        ...
    @abc.abstractmethod
    def set_size_inches(self, w, h):
        ...
    @abc.abstractmethod
    def savefig(self, file, **opts):
        ...

class GraphicsBackend(metaclass=abc.ABCMeta):
    Figure = GraphicsFigure
    @abc.abstractmethod
    def create_figure(self, *args, **kwargs) -> 'tuple[GraphicsFigure, tuple[GraphicsAxes]]':
        ...
    def create_axes(self, figure:'GraphicsFigure', *args, **kwargs):
        return figure.create_axes(*args, **kwargs, backend=self)
    def create_inset(self, figure, *args, **kw) -> 'GraphicsAxes':
        return figure.create_inset(*args, **kw)
    def close_figure(self, figure:'GraphicsFigure'):
        return figure.close(backend=self)
    def remove_axes(self, axes:'GraphicsAxes'):
        return axes.remove(backend=self)
    def clear_figure(self, figure:'GraphicsFigure'):
        return figure.clear(backend=self)
    def clear_axes(self, axes:'GraphicsAxes'):
        return axes.clear(backend=self)
    @abc.abstractmethod
    def get_interactive_status(self) -> 'bool':
        ...
    @abc.abstractmethod
    def disable_interactivity(self):
        ...
    @abc.abstractmethod
    def enable_interactivity(self):
        ...
    @abc.abstractmethod
    def show_figure(self, figure, reshow=None):
        ...

    @abc.abstractmethod
    def get_available_themes(self):
        ...
    class ThemeContextManager(metaclass=abc.ABCMeta):
        def __init__(self, theme_spec):
            self.spec = theme_spec
        @abc.abstractmethod
        def __enter__(self):
            ...
        @abc.abstractmethod
        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
    def theme_context(self, spec):
        return self.ThemeContextManager(spec)

    class DefaultBackends(enum.Enum):
        MPL = 'matplotlib'
        MPL3D = 'matplotlib3D'
        VTK = 'vtk'
        VPython = 'vpython'

    registered_backends = {}
    @classmethod
    def get_default_backends(cls):
        return {
            cls.DefaultBackends.MPL.value: MPLBackend,
            cls.DefaultBackends.MPL3D.value: MPLBackend,
            cls.DefaultBackends.VTK.value: VTKBackend,
            cls.DefaultBackends.VPython.value: VPythonBackend
        }
    @classmethod
    def lookup(cls, backend, opts=None) -> 'GraphicsBackend':
        if opts is None: opts = {}
        if not isinstance(backend, GraphicsBackend):
            name = backend
            backend = cls.registered_backends.get(name, None)
            if backend is None:
                backend_key = cls.DefaultBackends(name).value
                backend = cls.get_default_backends().get(backend_key)
        return backend(**opts)

class MPLManager:
    _plt = None
    _patch = None
    _coll = None
    _mpl = None
    _jlab = None

    @classmethod
    def plt_api(cls):
        if cls._plt is None:
            import matplotlib.pyplot as plt
            cls._plt = plt
        return cls._plt
    @classmethod
    def mpl_api(cls):
        if cls._mpl is None:
            import matplotlib as mpl
            cls._mpl = mpl
        return cls._mpl

    @classmethod
    def patch_api(cls):
        if cls._patch is None:
            import matplotlib.patches as patch
            cls._patch = patch
        return cls._patch
    @classmethod
    def collections_api(cls):
        if cls._coll is None:
            import matplotlib.collections as coll
            cls._coll = coll
        return cls._coll
    @classmethod
    def draw_if_interactive(self, *args, **kwargs):
        pass
    @classmethod
    def magic_backend(self, backend):
        try:
            from IPython.core.getipython import get_ipython
        except ImportError:
            pass
        else:
            shell = get_ipython()
            ip_name = type(shell).__name__
            in_nb = ip_name == 'ZMQInteractiveShell'
            if in_nb:
                try:
                    from IPython.core.magics import PylabMagics
                except ImportError:
                    pass
                else:
                    set_jupyter_backend = PylabMagics(shell).matplotlib
                    set_jupyter_backend(backend)

    # This flag will be reset by draw_if_interactive when called
    _draw_called = False
    # list of figures to draw when flush_figures is called
    _to_draw = []
    settings_stack = []
    @contextlib.contextmanager
    @classmethod
    def figure_settings(cls, figure):
        old_backend = None
        was_interactive = None
        drawer = None
        draw_all = None
        old_magic_backend = None
        old_show = None

        mpl = cls.mpl_api()
        plt = cls.plt_api()

        if figure.mpl_backend is not None:
            old_backend = mpl.get_backend()
        was_interactive = plt.isinteractive()

        cls.settings_stack.append((
            old_backend,
            was_interactive,
            drawer,
            draw_all,
            old_magic_backend,
            old_show
        ))
        try:
            if not figure.managed:
                # import matplotlib.pyplot as plt
                # plt.ioff
                # if 'inline' in self.mpl.get_backend():
                #     backend = self.plt._backend_mod
                #     self.plt.show = ...
                #     self._old_show = backend.show
                #     backend.show = self.jupyter_show
                if not figure.interactive:
                    plt.ioff()
                    # manager.canvas.mpl_disconnect(manager._cidgcf)
                    # self._drawer = self.plt.draw_if_interactive
                    # self._draw_all = self.plt.draw_all
                    # self.plt.draw_if_interactive = self.draw_if_interactive
                    # self.plt.draw_all = self.draw_if_interactive
                    # if self.fig.mpl_backend is None:
                    #     self._old_magic_backend = self.mpl.get_backend()
                    #     self.magic_backend('Agg')
                else:
                    plt.ion()
                    # if self.fig.mpl_backend is None:
                    #     self._old_magic_backend = self.mpl.get_backend()
                    #     if 'inline' not in self._old_magic_backend:
                    #         self.magic_backend('inline')

            yield None
        finally:
            (
                old_backend,
                was_interactive,
                drawer,
                draw_all,
                old_magic_backend,
                old_show
            ) = cls.settings_stack.pop()

            if old_backend is not None:
                mpl.use(old_backend)
            if drawer is not None:
                plt.draw_if_interactive = drawer
            if draw_all is not None:
                plt.draw_all = draw_all
            if old_show is not None:
                plt._backend_mod.show = old_show

            if old_magic_backend is not None:
                if 'inline' in old_magic_backend:
                    cls.magic_backend('inline')
                else:
                    mpl.use(old_magic_backend)
            if was_interactive and not plt.isinteractive():
                plt.ion()

    @classmethod
    def mpl_disconnect(cls, graphics):
        # this is a hack that might need to be updated in the future
        if 'inline' in cls.mpl_api().get_backend():
            try:
                from matplotlib._pylab_helpers import Gcf
                canvas = graphics.figure.canvas
                num = canvas.manager.num
                if all(hasattr(num, attr) for attr in ["num", "_cidgcf", "destroy"]):
                    manager = num
                    if Gcf.figs.get(manager.num) is manager:
                        Gcf.figs.pop(manager.num)
                    else:
                        return
                else:
                    try:
                        manager = Gcf.figs.pop(num)
                    except KeyError:
                        return
                # manager.canvas.mpl_disconnect(manager._cidgcf)
                # self.fig.figure.canvas.mpl_disconnect(
                #     self.fig.figure.canvas.manager._cidgcf
                # )
            except:
                pass

    @classmethod
    def mpl_connect(cls, graphics):
        if 'inline' in cls.mpl_api().get_backend():
            # try:
            from matplotlib._pylab_helpers import Gcf
            canvas = graphics.figure.canvas
            manager = canvas.manager
            num = canvas.manager.num
            Gcf.figs[num] = manager
            manager._cidgcf = canvas.mpl_connect(
                "button_press_event", lambda event: Gcf.set_active(manager)
            )
            # manager.canvas.mpl_disconnect(manager._cidgcf)
            # self.fig.figure.canvas.mpl_disconnect(
            #     self.fig.figure.canvas.manager._cidgcf
            # )
            # except:
            #     pass

    @classmethod
    def jupyter_show(cls, close=None, block=None):
        """Show all figures as SVG/PNG payloads sent to the IPython clients.
        Parameters
        ----------
        close : bool, optional
            If true, a ``plt.close('all')`` call is automatically issued after
            sending all the figures. If this is set, the figures will entirely
            removed from the internal list of figures.
        block : Not used.
            The `block` parameter is a Matplotlib experimental parameter.
            We accept it in the function signature for compatibility with other
            backends.
        """

        from matplotlib._pylab_helpers import Gcf
        from IPython.core.display import display
        plt = cls.plt_api()
        mpl_inline = plt._backend_mod

        if close is None:
            close = mpl_inline.InlineBackend.instance().close_figures
        try:
            for figure_manager in [Gcf.get_active()]:
                display(
                    figure_manager.canvas.figure,
                    metadata=mpl_inline._fetch_figure_metadata(figure_manager.canvas.figure)
                )
        finally:
            cls._to_draw = []
            # only call close('all') if any to close
            # close triggers gc.collect, which can be slow
            if close and Gcf.get_all_fig_managers():
                plt.close('all')

class MPLAxes(GraphicsAxes):
    def __init__(self, mpl_axes_object, **opts):
        self.obj = mpl_axes_object
        super().__init__(**self.canonicalize_opts(opts))
    def clear(self, *, backend=None):
        ax = self.obj
        all_things = ax.artists + ax.patches
        for a in all_things:
            a.remove()
    def remove(self, *, backend):
        self.obj.remove()

    def get_plotter(self, method):
        plot_method = getattr(self.obj, method)
        def plot(*data, **styles):
            return plot_method(*data, **styles)
        return plot


    def get_plot_label(self):
        return self.obj.set_title()
    def set_plot_label(self, val, **style):
        self.obj.set_title(val, **style)

    def get_frame_visible(self):
        return (
            (
                self.obj.spines['left'].get_visible(),
                self.obj.spines['right'].get_visible()
            ),
            (
                self.obj.spines['bottom'].get_visible(),
                self.obj.spines['top'].get_visible()
            ),
        )
    def set_frame_visible(self, frame_spec):
        if frame_spec is True or frame_spec is False:
            self.obj.set_frame_on(frame_spec)
        else:
            lr, bt = frame_spec
            if lr is None:
                l = r = None
            elif lr is True or lr is False:
                l = r = lr
            else:
                l,r = lr
            if bt is True or bt is False:
                b = t = bt
            else:
                b,t = bt
            for k,v in [
                ['left', l],
                ['right', r],
                ['bottom', b],
                ['top', t]
            ]:
                if v is not None: self.obj.spines[k].set_visible(v)

    def get_frame_styke(self):
        return (
            (
                self.obj.spines['left'].get(),
                self.obj.spines['right'].get()
            ),
            (
                self.obj.spines['bottom'].get(),
                self.obj.spines['top'].get()
            ),
        )
    def set_frame_style(self, frame_spec):
        if isinstance(frame_spec, dict):
            l, r, b, t = frame_spec
        else:
            lr, bt = frame_spec
            if lr is None:
                l = r = None
            elif lr is True or lr is False:
                l = r = lr
            else:
                l,r = lr
            if bt is True or bt is False:
                b = t = bt
            else:
                b,t = bt
        for k,v in [
            ['left', l],
            ['right', r],
            ['bottom', b],
            ['top', t]
        ]:
            if v is not None: self.obj.spines[k].set(**v)


    def get_xlabel(self):
        return self.obj.get_xlabel()
    def set_xlabel(self, val, **style):
        self.obj.set_xlabel(val, **style)
    def get_ylabel(self):
        return self.obj.get_ylabel()
    def set_ylabel(self, val, **style):
        self.obj.set_ylabel(val, **style)

    def get_xlim(self):
        return self.obj.get_xlim()
    def set_xlim(self, val, **opts):
        self.obj.set_xlim(val, **opts)
    def get_ylim(self):
        return self.obj.get_ylim()
    def set_ylim(self, val, **opts):
        self.obj.set_ylim(val, **opts)

    def get_xticks(self):
        return self.obj.get_xticks()
    def set_xticks(self, val, **opts):
        self.obj.set_xticks(val, **opts)

    def get_yticks(self):
        return self.obj.get_yticks()
    def set_yticks(self, val, **opts):
        self.obj.set_yticks(val, **opts)

    def get_xtick_style(self):
        return self.obj.tick_params(axis='x')
    def set_xtick_style(self, **opts):
        return self.obj.tick_params(axis='x', **opts)
    def get_ytick_style(self):
        return self.obj.tick_params(axis='y')
    def set_ytick_style(self, **opts):
        return self.obj.tick_params(axis='y', **opts)

    def set_aspect_ratio(self, ar):
        self.obj.set_aspect(ar)

    def get_bbox(self):
        bbox = self.obj.get_position()
        if hasattr(bbox, 'get_points'):
            bbox = bbox.get_points()
        bbox = [
            [b*DPI_SCALING for b in bb]
            for bb in bbox
        ]

        return bbox
    def set_bbox(self, bbox):
        if hasattr(bbox, 'get_points'):
            bbox = bbox.get_points()
        else:
            bbox = [
                [b / DPI_SCALING for b in bb]
                for bb in bbox
            ]
        ((lx, by), (rx, ty)) = bbox
        self.obj.set_position([lx, by, rx-lx, ty-by])

    def get_facecolor(self):
        return self.obj.get_facecolor()
    def set_facecolor(self, fg):
        return self.obj.set_facecolor(fg)

    def get_padding(self):
        padding = [
            ['left', 'right'],
            ['bottom', 'top']
        ]
        xlab_padding = None
        ylab_padding = None
        for i, l in enumerate(padding):
            for j, key in enumerate(l):
                spine = self.obj.spines[key]
                viz = spine.get_visible()
                if viz:
                    ((l, b), (r, t)) = bbox = spine.get_window_extent().get_points()
                    if i == 0:
                        base_pad = r - l
                        if xlab_padding is None:
                            xlabs = self.obj.get_xticklabels()
                            if len(xlabs) > 0:
                                min_x = 1e10
                                max_x = -1e10
                                for lab in xlabs:
                                    ((l, b), (r, t)) = lab.get_window_extent().get_points()
                                    min_x = min(l, min_x)
                                    max_x = max(r, max_x)
                                xlab_padding = max_x - min_x
                            else:
                                xlab_padding = 0
                        padding[i][j] = base_pad + xlab_padding
                    else:
                        base_pad = t - b
                        if ylab_padding is None:
                            ylabs = self.obj.get_yticklabels()
                            if len(ylabs) > 0:
                                min_y = 1e10
                                max_y = -1e10
                                for lab in ylabs:
                                    ((l, b), (r, t)) = lab.get_window_extent().get_points()
                                    min_y = min(b, min_y)
                                    max_y = max(t, max_y)
                                ylab_padding = max_y - min_y
                            else:
                                ylab_padding = 0
                        padding[i][j] = base_pad + ylab_padding
                else:
                    padding[i][j] = 0
        return padding

    def draw_line(self, points, **styles):
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('plot')(
            points[:, 0],
            points[:, 1],
            **styles
        )

    def draw_disk(self, points, **styles):
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('scatter')(
            points[:, 0],
            points[:, 1],
            **styles
        )

    def draw_rect(self, points, **styles):
        patches = MPLManager.patch_api()
        coll = MPLManager.collections_api()
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]

        anchors = points[:, 0]
        widths = points[:, 1, 0] - points[:, 0, 0]
        heights = points[:, 1, 1] - points[:, 0, 1]

        rects = coll.PatchCollection([
            patches.Rectangle(a, w, h, **styles)
            for a,w,h in zip(anchors, widths, heights)
        ])

        self.obj.add_patch(rects)

    def draw_poly(self, points, **styles):
        patches = MPLManager.patch_api()
        coll = MPLManager.collections_api()
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]

        polys = coll.PatchCollection([
            patches.Polygon(pt, **styles) for pt in points
        ])

        self.obj.add_patch(polys)

    def draw_arrow(self, points, **styles):
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        return self.get_plotter('arrow')(
            points[:, 0],
            points[:, 1],
            **styles
        )
    def draw_text(self, points, vals, **styles):
        points = np.asanyarray(points)
        if points.ndim == 2:
            points = points[np.newaxis]
        if isinstance(vals, str):
            vals = [vals]
        text_plotter = self.get_plotter('text')
        for pt, txt in zip(points, vals):
            return text_plotter(
                *pt, txt,
                **styles
            )

class MPLFigure(GraphicsFigure):
    Axes = MPLAxes

    _refs = set()
    def __init__(self, mpl_figure_object, **opts):
        if mpl_figure_object in self._refs: raise ValueError(...)
        self._refs.add(mpl_figure_object)
        self.obj = mpl_figure_object
        super().__init__(**self.canonicalize_opts(opts))
    def __hash__(self): # we need weakref to behave right
        return hash(self.obj)
    def create_axes(self, rows, cols, spans, **kw):
        return self.add_axes(
            self.obj.add_subplot((rows, cols, spans), **kw)
        )
    def create_inset(self, bbox, **kw) -> 'GraphicsAxes':
        ((x, y), (X, Y)) = bbox
        return self.add_axes(
            self.obj.add_axes([x, y, X-x, Y-y], **kw)
        )
    def clear(self, *, backend):
        raise NotImplementedError(...)
    def close(self, *, backend):
        return backend.plt.close(self.obj)
    def create_colorbar(self, graphics, axes, norm=None, cmap=None, **kw):
        if graphics is None:
            import matplotlib.cm as cm
            graphics = cm.ScalarMappable(norm=norm, cmap=cmap)
        self.obj.colorbar(graphics, cax=axes.obj, **kw)
        return axes
    def get_figure_label(self):
        return self.obj.suptitle()
    def set_figure_label(self, val, **style):
        self.obj.suptitle(val, **style)

    def get_size_inches(self):
        return self.obj.get_size_inches()
    def set_size_inches(self, w, h):
        self.obj.set_size_inches(w, h)

    def set_extents(self, extents):
        if isinstance(extents, (list, tuple)):
            lr, bt = extents
            if isinstance(lr, (list, tuple)):
                l,r = lr
            else:
                l = r = lr
            if isinstance(bt, (list, tuple)):
                b,t = bt
            else:
                b = t = bt
        else:
            l = r = b = t = extents
        self.obj.subplots_adjust(
            left=l,
            right=r,
            bottom=b,
            top=t
        )  # , hspace=0, wspace=0)

    def set_figure_spacings(self, spacing):
        if isinstance(spacing, (list, tuple)):
            w,h = spacing
        else:
            w = h = spacing
        self.obj.subplots_adjust(wspace=w, hspace=h)

    def get_facecolor(self):
        return self.obj.get_facecolor()

    def set_facecolor(self, fg):
        return self.obj.set_facecolor(fg)

    def savefig(self, file, **opts):
        return self.obj.savefig(file, **opts)

class MPLBackend(GraphicsBackend):
    Figure = MPLFigure
    @property
    def plt(self):
        return MPLManager.plt_api()
    @property
    def mpl(self):
        return MPLManager.mpl_api()
    def create_figure(self, *args, **kwargs):
        Axes = self.Figure.Axes
        figure, axes = MPLManager.plt_api().subplots(*args, **kwargs)
        if isinstance(axes, (np.ndarray, list, tuple)):
            if isinstance(axes[0], (np.ndarray, list, tuple)):
                axes = tuple(tuple(Axes(b) for b in a) for a in axes)
            else:
                axes = tuple(Axes(a) for a in axes)
        else:
            axes = Axes(axes)
        return self.Figure(figure), axes
    def show_all(self):
        self.plt.show()

    class ThemeContextManager(GraphicsBackend.ThemeContextManager):
        def __init__(self, theme_spec):
            super().__init__(theme_spec)
            self.context = MPLManager.plt_api().style.context(theme_spec)
        def __enter__(self):
            return self.context.__enter__()
        def __exit__(self, exc_type, exc_val, exc_tb):
            return self.context.__exit__(exc_type, exc_val, exc_tb)

    def show_figure(self, graphics, reshow=None):
        self.plt.show()
        # return graphics.show_mpl(self, reshow=reshow)

    def get_interactive_status(self) -> 'bool':
        return self.plt.isinteractive()
    def disable_interactivity(self):
        return self.plt.ioff()
    def enable_interactivity(self):
        return self.plt.ion()
    def get_available_themes(self):
        import matplotlib.style as sty
        theme_names = sty.available
        return theme_names

class MPLFigure3D(MPLFigure):
    def create_axes(self, rows, cols, spans, projection='3d', **kw):
        super().create_axes(rows, cols, spans, projection=projection, **kw)
class MPLBackend3D(MPLBackend):
    Figure = MPLFigure3D
    def create_figure(self, *args, subplot_kw=None, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D
        subplot_kw = dict({"projection": '3d'}, **({} if subplot_kw is None else subplot_kw))
        return super().create_axes(*args, subplot_kw=subplot_kw, **kwargs)

class VTKBackend(GraphicsBackend):
    ...

class VPythonBackend(VTKBackend):
    ...
