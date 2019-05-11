
from controller.controller_abstracts import ControllerInterface

class SelectionController(ControllerInterface):
    def __init__(self,controller):
        super().__init__(controller)

    def _key_press_event(self, event):
        if event.key=='i':
            self.model.update_selection(1)
            self.remap()
        elif event.key=='o':
            self.model.update_selection(0)
            self.remap()
        elif event.key=='h':
            title = "include/exclude Functionality"
            functionality = {
                'include selected station': 'press i',
                'exclude selected station': 'press o'
            }
            self.create_help_menu_string(title, functionality)
    def remap(self):
        data = self.model.get_mapping_data()
        self.view.map(data)