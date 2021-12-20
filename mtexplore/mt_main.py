import os
import sys
sys.path.append(os.getcwd()+os.sep +'mtexplore')
from .model.modelcontroller import ModelController
from .view.view import MainView
from .controller.controller import MainController



class Mt_Ex_Main:

    def __init__(self,debug=False,**kwargs):
        self.controller = MainController()
        self.model = ModelController( **kwargs)
        self.view  = MainView()
        self.controller.add_view_base(self.view)
        self.controller.add_model(self.model)
        self.controller.start()

    def connect_database(self,database):
        self.model.add_database(database)
        self.controller.set_default_frame()
        self.controller.update()
        
    def connect_selection(self,selection_file):
        self.model.connect_selection(selection_file)
        self.controller.update()
