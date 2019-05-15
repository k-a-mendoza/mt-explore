
from controller.controller_abstracts import ControllerInterface

class CycleController(ControllerInterface):
    selection_distance = (0.01,0.01)
    def __init__(self,controller):
        super().__init__(controller)

    def _key_press_event(self,event):
        if event.key=='n':
            self.model.next_selection()
            self._update_selection()

        if event.key=='m':
            self.model.next_survey()
            self._update_selection()

        if event.key=='h':
            title = "Cycle Selection Functionality"
            functionality = {
                'next station in group':'press n',
                'next survey group':'press m'
            }
            self.create_help_menu_string(title, functionality)

    def _update_selection(self):
        selection = self.model.get_selection()
        self.view.update_selection(selection)
