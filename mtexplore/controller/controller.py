from .map_controller import MapController
import matplotlib.pyplot as plt
class MainController:
    dimensions = (15,10)
    def __init__(self):
        self.fig = plt.figure(figsize=self.dimensions)
        self.fig._key_press_method_for_mtpy = self.key_press_events
        self.fig.canvas.mpl_connect('key_press_event',self.fig._key_press_method_for_mtpy)
        self.fig.show()
        self.map_controller = MapController()

    def get_figure(self):
        return self.fig

    def add_model(self,model):
        self.map_controller.add_model(model)

    def add_view_base(self, view):
        self.view = view

    def start(self):
        self.view.start()
        self.map_controller.update_all_stations()
        self.view.finish()

    def key_press_events(self,event):
        print(event)
        self.map_controller.key_press_event(event)

    def get_map_controller(self)-> MapController:
        return self.map_controller

    def update_all_stations(self):
        self.map_controller.update_all_stations()