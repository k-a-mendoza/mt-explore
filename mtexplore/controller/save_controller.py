from .controller_abstracts import ControllerInterface
from ..view.view_base import ViewContract
from ..model.modelcontroller import DatabaseModel

class SaveController(ControllerInterface):

    def __init__(self,controller):
        super().__init__(controller)

    def _key_press_event(self,event):
        if event.key=='j':
            self.model.save_selection()
        elif event.key=='h':
            title = "Save & Load Functionality"
            functionality = {
                'Save': 'press j',
            }
            self.create_help_menu_string(title, functionality)

