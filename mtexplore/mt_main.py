import os
import sys
sys.path.append(os.getcwd()+os.sep +'mtexplore')
from model.modelcontroller import ModelController
from model import mt_py_facade
from view.view import MainView
from controller.controller import MainController



class Mt_Ex_Main:

    def __init__(self,debug=False,**kwargs):
        mt_facade=mt_py_facade.MtFacade(debug)
        self.controller = MainController()
        self.model = ModelController(mt_facade=mt_facade, **kwargs)
        self.view  = MainView()
        self.controller.add_view_base(self.view)
        self.controller.add_model(self.model)
        self.controller.start()

    def connect_database(self,database_directory):
        self.model.set_database_directory(database_directory)
        self.controller.set_default_frame()
        self.controller.update()
