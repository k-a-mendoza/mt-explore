
from .controller_abstracts import ControllerInterface

class SelectionController(ControllerInterface):
    def __init__(self,controller):
        super().__init__(controller)

    def _key_press_event(self, event):

        if event.key=='i':
            self.model.update_selection(True)
            self.remap()
        elif event.key=='o':
            self.model.update_selection(False)
            self.remap()
        elif event.key=='x':
            self.model.save_selection()

        elif event.key=='h':
            title = "include/exclude Functionality"
            functionality = {
                'include selected station': 'press i',
                'exclude selected station': 'press o',
                'save selected stations': 'press x'
            }
            self.create_help_menu_string(title, functionality)

    def _key_release_event(self,event):
        pass

    def remap(self):
        data = self.model.get_mapping_data()
        self.view.map(data)

