import glob
import pandas as  pd
from mtpy.core import mt
import numpy as np
import os

def absolute_path(main_directory,row):
    if row['filepath']=='':
        row['filepath']=np.nan
        return row
    if pd.isna(row['filepath']):
        return row
    file = row['filepath'].split(os.sep)[-1]
    row['filepath']= main_directory + os.sep + file
    return row
    
    
def clean_incoming_files_and_create_df(filepath):
    file_previous = filepath.split(os.sep)
    directory=os.getcwd() 
    for s in file_previous[:-1]:
        directory= directory + os.sep + s
        
    df = pd.read_csv(filepath)
    if 'location_on_disk' in df.columns:
            df.rename(columns={"location_on_disk": "filepath"},inplace=True)
    if 'filepath' not in df.columns:
            df['filepath']=np.nan
            return df
    
    df = df.apply(lambda x : absolute_path(directory,x),axis=1)

    return df

class DatabaseModel:
    _columns= ['latitude','longitude','station','project','include']

    click_precision=0.05

    def __init__(self):
        self._station_df        = None
        self._survey_cycler     = None
        self._selection_cycler  = None
        self._databases          = []
        self._mtexplore_metadata = None

    def add_database(self,database):
        self._databases.append(database)
        new_df = database.get_df()
        new_df['include'] = False
        if self._mtexplore_metadata is not None:
            self._mtexplore_metadata = pd.concat([self._mtexplore_metadata,new_df],
                                                 ignore_index=True)
        else:
            self._mtexplore_metadata = new_df

    def get_mapping_data(self):
        """

        Returns
        -------
        pandas dataframe with columns ['latitude', 'longitude', 'survey', 'include']

        """
        if self._mtexplore_metadata is not None:
            subframe =  self._mtexplore_metadata.copy(deep=True)
            return subframe
        return pd.DataFrame(columns=['latitude', 'longitude', 'project','station', 'include'])

    def get_included_stations(self):
        df = self._mtexplore_metadata.copy(deep=True)
        df = df[df.include]
        df = df[self._columns]
        return df
    
    def set_included_stations(self,df):
        for index, row in df.iterrows():
            self._mtexplore_metadata[
                    (df['project']==self._mtexplore_metadata['project']) & 
                    (df['station']==self._mtexplore_metadata['station']),['include']]=True
      

    def get_unique_projects(self):
        return self.df['project'].unique().tolist()

    def get_closest_row(self,location,extent):
        df = self._mtexplore_metadata.copy(deep=True)
        delta_x = extent[0][1]-extent[0][0]
        delta_y = extent[1][1]-extent[1][0]
        max_delta = np.amax([delta_x,delta_y])
        lon = location[1]-df['longitude']
        lat = location[0]-df['latitude']
        dist_condition = lon**2 + lat**2 
        df['distance2']=dist_condition
        upper_limit = (self.click_precision*max_delta)**2
        
        indices = df[dist_condition<upper_limit].index
        if indices.empty:
            print('isempty')
            return None
        sub_frame = df[df.distance2==df.distance2.min()]
        sub_frame.drop(columns=['distance2'],inplace=True)
        return sub_frame
        
    def get_mtobj(self, target_frame):
        if len(target_frame)==0:
            return None
        else:
            project = target_frame['project'].values[0]
            station = target_frame['station'].values[0]
            for database in self._databases:
                mt_object = database.get_mt_object(project,station)
                if mt_object is not None:
                    break
            return mt_object

        
    def update_selection(self,frame,value):
        self._mtexplore_metadata.at[frame.index[0], 'include']= value
        
    
       
