from .model.model import Model
from .view.view import MainView
from .controller.controller import MainController

class Main:

    def __init__(self,**kwargs):
        self.model = Model(**kwargs)
        self.view  = MainView()
        self.controller = MainController()

        self.view.add_controller(self.controller)
        self.controller.add_model(self.model)
        self.controller.start()

    def connect_database(self,database_directory):
        self.model.get_database_model().set_directory(database_directory)
        self.controller.update_all_stations()