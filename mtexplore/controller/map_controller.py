
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
        print('\nbutton press event\n')
        axes_label = self.view.get_axes_of_click(event)
        print(axes_label)
        if axes_label == 'map':
            print('assigning initial click')
            lat, lon = event.ydata, event.xdata
            self.location = np.asarray((lat, lon))

    def _button_release_event(self, event):
        print('\nbutton release event\n')
        axes_label = self.view.get_axes_of_click(event)
        print(axes_label)
        if axes_label != 'map':
            return None
        lat, lon = event.ydata, event.xdata

        deltay = abs(self.location[0]-lat)
        deltax = abs(self.location[1]-lon)

        extent = self.view.get_extent()
        xlim = extent[0]
        ylim = extent[1]

        xfrac = deltax / (xlim[1]-xlim[0])
        yfrac = deltay / (ylim[1]-ylim[0])
        print('made selection')
        if xfrac<0.001 and yfrac<0.001:
            print('single station selector')
            selection = self.model.get_selection_data(np.asarray((lat, lon)), extent)
            print(selection)
            self.view.update_selection(selection)
        else:
            print('multi station selector')
            self.model.create_cycler(self.location,np.asarray((lat, lon)))










