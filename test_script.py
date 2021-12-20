from mtexplore import Mt_Ex_Main
import sys
import pandas as pd
import os
sys.path.append(os.path.join('/home','kevin','Desktop','thesis work','python','egi_utils_remote','egi_utils'))
import egi_utils.h5mt as h5mt
#%%
class PandasFacade:
    
    
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
    
actual_database   = h5mt.H5MTExperiment('../../../Database/Organized_TFs/western_us_experiment')
all_locations = PandasFacade('../../../../thesis work/python/Western_US_Mesh/locations/'+\
                                 'dataless_site_locations.csv')
    
# alternate spline control = 'starting_data/spline_control_points.csv'
#spline_control = PandasFacade('../../../../thesis work/python/Western_US_Mesh/starting_data/'+\
#                                 'new_cleaned_spline_control_points.csv',project_override='spline control')
    
ks_ta = PandasFacade('../../../../thesis work/python/Western_US_Mesh/locations/TA Stations'+\
                                 '/ks_ta_stations_cleaned.csv')

    #%%
# try this
main_app = Mt_Ex_Main()
#main_app.connect_database(ks_ta)
main_app.connect_database(actual_database)
#main_app.connect_database(all_locations)
#main_app.connect_database(spline_control)
#main_app.connect_selection('../../../../thesis work/python/Western_US_Mesh/notebook_7/off_transect_stations.csv')
#%%
