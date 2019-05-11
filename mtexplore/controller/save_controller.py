from controller.controller_abstracts import ControllerInterface
from view.view_base import ViewContract
from model.model import DatabaseModel

class SaveController(ControllerInterface):

    def __init__(self,controller):
        super().__init__(controller)

    def _key_press_event(self,event):
        if event.key=='j':
            self.model.save()
        elif event.key=='l':
            self.model.load()
        elif event.key=='k':
            self.model.new_df_load()
            data = self.model.get_mapping_data()
            self.view.map(data)
        elif event.key=='h':
            title = "Save & Load Functionality"
            functionality = {
                'Save': 'press j',
                'Load from previous .csv': 'press l',
                'Load from database/*.edi\'s': 'press l'
            }
            self.create_help_menu_string(title, functionality)

