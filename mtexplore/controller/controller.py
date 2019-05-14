from .map_controller import MapController
from .cycle_controller import CycleController
from .save_controller import SaveController
from mtexplore.view.view import MainView
from .controller_abstracts import ControllerBase
from .selection_controller import SelectionController
import matplotlib.pyplot as plt
from matplotlib import rcParams

class MainController:
    dimensions = (15,10)
    def __init__(self):
        self._print_default_bindings()
        self.fig = plt.figure(figsize=self.dimensions)
        self.fig._key_press_method_for_mtpy      = self.key_press_events
        self.fig._key_release_method_for_mtpy    = self.key_release_events
        self.fig._button_press_method_for_mtpy   = self.button_press_events
        self.fig._button_release_method_for_mtpy = self.button_release_events
        self.fig.canvas.mpl_connect('key_press_event',self.fig._key_press_method_for_mtpy)
        self.fig.canvas.mpl_connect('key_release_event', self.fig._key_release_method_for_mtpy)
        self.fig.canvas.mpl_connect('button_press_event', self.fig._button_press_method_for_mtpy)
        self.fig.canvas.mpl_connect('button_release_event', self.fig._button_release_method_for_mtpy)
        self.fig.show()
        self.controller = SelectionController(
                            SaveController(
                                CycleController(
                                    MapController(
                                        ControllerBase()))))

    def get_figure(self):
        return self.fig

    def add_model(self,model):
        self.controller.connect_model(model)

    def add_view_base(self, view: MainView):
        self.view = view
        self.view.set_figure(self.fig)
        self.controller.connect_view(view.get_view())

    def start(self):
        self.view.start()
        self.controller.update_map()
        self.view.finish()

    def key_press_events(self,event):
        self.controller.key_press_event(event)
        self.view.update()

    def key_release_events(self,event):
        self.controller.key_release_event(event)
        self.view.update()

    def button_press_events(self, event):
        self.controller.button_press_event(event)
        self.view.update()

    def button_release_events(self, event):
        self.controller.button_release_event(event)
        self.view.update()

    def update(self):
        self.controller.update()

    def _print_default_bindings(self):
        rc_keys = ['keymap.fullscreen','keymap.home','keymap.back','keymap.forward','keymap.pan',
                   'keymap.zoom','keymap.save','keymap.quit','keymap.grid','keymap.yscale','keymap.xscale']
        for rc_key in rc_keys:
            try:
                rcParams[rc_key]=[]
            except ValueError:
                print('key {} not in list'.format(rc_key))

