
from .database_model import DatabaseModel

class Model:

    def __init__(self,mt_facade=None, working_directory=None,source_directory=None,**kwargs):
        self.database_model = DatabaseModel(mt_facade,source_directory)

    def get_database_model(self):
        """
        gets a database model
        :rtype: DatabaseModel
        :return: a database model
        """
        return self.database_model

