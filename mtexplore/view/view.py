from .view_base import BaseView, ViewContract
from .map_view import MapView
from ..controller.controller import MainController
base_view_dimensions = (15,10)

def get_view_stack():
    return MapView(
            BaseView(base_view_dimensions))

class MainView:

    def __init__(self):
        self.view  = get_view_stack()

    def add_controller(self, controller: MainController):
        self.view.add_controller(controller)
        controller.add_view_base(self)

    def start(self):
        self.view.configure()
        self.view.update()

    def update(self):
        self.view.update()

    def finish(self):
        self.view.finish()