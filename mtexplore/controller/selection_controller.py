
from controller.controller_abstracts import ControllerInterface

class SelectionController(ControllerInterface):
    def __init__(self,controller):
        super().__init__(controller)

    def _key_press_event(self, event):

        if event.key=='i':
            self.model.update_selection(1)
            self.remap()
        elif event.key=='I':
            self.model.update_cycle_selection(1)
            self.remap()
        elif event.key=='o':
            self.model.update_selection(0)
            self.remap()
        elif event.key=='O':
            self.model.update_cycle_selection(0)
            self.remap()

        elif event.key=='h':
            title = "include/exclude Functionality"
            functionality = {
                'include selected station': 'press i',
                'exclude selected station': 'press o',
                'hold shift to apply en-batch':'press \'shift\''
            }
            self.create_help_menu_string(title, functionality)

    def _key_release_event(self,event):
        pass

    def remap(self):
        data = self.model.get_mapping_data()
        self.view.map(data)

