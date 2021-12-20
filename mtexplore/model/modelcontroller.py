
from .database_model import DatabaseModel
import pandas as pd

class ModelController:

    def __init__(self,mt_facade=None,**kwargs):
        self.database_model    = DatabaseModel()
        self.selection_df      = None

    def add_database(self,database):
        self.database_model.add_database(database)


    def get_mapping_data(self)-> pd.DataFrame:
        return self.database_model.get_mapping_data()
    
    def get_selection_data(self,location, extent):
        target_frame = self.database_model.get_closest_row(location,extent)
        self.selection_df=target_frame
        if target_frame is None:
            return {'project':None, 'mt obj': None}
        else:
            mt_obj = self.database_model.get_mtobj(target_frame)
            return {'project':target_frame, 'mt obj': mt_obj}
        
    def save_selection(self):
        df = self.database_model.get_included_stations()
        df.to_csv('included_stations_all.csv')
        
    def update_selection(self,update):
        if self.selection_df is not None:   
            self.database_model.update_selection(self.selection_df, update)
            
    def connect_selection(self,selection_file):
        df = pd.read_csv(selection_file)
        self.database_model.set_included_stations(df)
        
 

