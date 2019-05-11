from mtexplore.view.view_base import BaseView
from mtexplore.view.map_view import MapView
from mtexplore.view.mt_view import MTView

base_view_dimensions = (15,10)

def get_view_stack():
    return MTView(
            MapView(
                BaseView(base_view_dimensions)))

class MainView:

    def __init__(self):
        self.view  = get_view_stack()

    def get_view(self):
        return self.view

    def start(self):
        self.view.configure()
        self.view.update()

    def set_figure(self,fig):
        self.view.set_figure(fig)

    def finish(self):
        self.view.finish()

    def update(self):
        self.view.update()