
import numpy as np
from .controller_abstracts import ControllerInterface

class MapController(ControllerInterface):

    click_range = 1/100

    def __init__(self,controller):
        super().__init__(controller)
        self.pressed  = False
        self.delete_gridline=False
        self.location    = None
        self.create_grid = False

    def _key_press_event(self,event):

        if event.key=='h':
            title = "Map Selection Functionality"
            functionality = {
                'select individual station': 'click',
            }
            self.create_help_menu_string(title, functionality)



    def _update(self):
        data = self.model.get_mapping_data()
        self.view.map(data)

    def _button_press_event(self, event):
        axes_label = self.view.get_axes_of_click(event)
        

        if axes_label == 'map':
            lat, lon = event.ydata, event.xdata
            location = np.asarray((lat, lon))
            extent   = self.view.get_extent()
            selection = self.model.get_selection_data(location, extent)
            self.view.update_selection(selection)










