from .map_controller import MapController

class MainController:

    def __init__(self):
        self.map_controller = MapController()


    def add_model(self,model):
        self.map_controller.add_model(model)

    def add_view_base(self, view):
        self.view = view

    def start(self):
        self.view.start()
        self.map_controller.update_all_stations()
        self.view.finish()

    def set_events(self,figure):
        self.map_controller.connect_figure_event(figure)

    def get_map_controller(self)-> MapController:
        return self.map_controller

    def update_all_stations(self):
        self.map_controller.update_all_stations()