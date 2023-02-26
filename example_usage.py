
from mtexplore import Mt_Ex_Main
import sys
import pandas as pd
import os

class DummyClass:
    
    
    def __init__(self,file,project_override=False):
        self.meta_df    = pd.read_csv(f'{file}')
        if project_override:
            self.meta_df['project']=project_override
        if 'name' in self.meta_df.columns.values:
            self.meta_df['station']=self.meta_df['name']
        
        
    def get_df(self):
        return self.meta_df.copy(deep=True)
    
    def get_mt_object(self,project, station):
        return None
 
    
dummy_database = DummyClass('TA Stations/ks_ta_stations_cleaned.csv')
main_app = Mt_Ex_Main()
main_app.connect_database(dummy_database)
