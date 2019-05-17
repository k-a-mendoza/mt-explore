
from controller.controller_abstracts import ControllerInterface

class ScrollController(ControllerInterface):
    def __init__(self,controller):
        super().__init__(controller)

    def _set_default_frame(self):
        df= self.model.get_mapping_data()
        self.view.set_default_df(df)

    def _scroll_event(self, event):
        axes = self.view.get_axes_of_click(event)

        if axes=='map':
            center = [event.xdata, event.ydata]
            if event.button=='up':
                self.view.zoom(center=center,zoom='in')

            elif event.button=='down':
                self.view.zoom(center=center,zoom='out')

            else:
                print(event.button)

    def _key_press_event(self,event):

        if event.key=='h':
            title = "include/exclude Functionality"
            functionality = {
                'zoom in scroll': 'scroll up',
                'zoom out scroll': 'scroll down',
                're-center':'c'
            }
            self.create_help_menu_string(title, functionality)

        elif event.key=='c':
            self.view.zoom()

