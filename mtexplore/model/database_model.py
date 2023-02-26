import glob
import pandas as  pd
from mtpy.core import mt
import numpy as np
import os
import matplotlib.colors as mplcolors
import matplotlib.cm as mplcolormap

def get_hexmap(fraction):
    rgb = mplcolormap.get_cmap('nipy_spectral')(fraction)
    return mplcolors.to_hex(rgb)

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

class SelectionCycler:

    def __init__(self, metadata_df, lat_0, lat_1, lon_0, lon_1):
        self.selection_index = 0
        self.sub_df = metadata_df[(metadata_df.latitude>lat_0) & (metadata_df.latitude<lat_1) &\
                             (metadata_df.longitude>lon_0) & (metadata_df.longitude<lon_1)].copy()
        self.sub_df.reset_index(names=['global_index'],inplace=True)
        self.sub_df=self.sub_df['global_index']

    def get_selection(self):
        return self.sub_df.iloc[[self.selection_index]].values[0]

    def next_index(self):
        self.selection_index+=1
        if self.selection_index>=len(self.sub_df):
            self.selection_index=0
            
            
            
class DatabaseModel:
    _columns= ['latitude','longitude','station','project','include','project_color']

    click_precision=0.05

    def __init__(self):
        self._station_df        = None
        self._survey_cycler     = None
        self._selection_cycler  = None
        self._databases          = []
        self._mtexplore_metadata = None

    def create_cycler(self,lat_0, lat_1, lon_0, lon_1):
        self._selection_cycler = SelectionCycler(self._mtexplore_metadata,lat_0, lat_1, lon_0, lon_1)

    def add_database(self,database):
        self._databases.append(database)
        new_df = database.get_df()
        new_df['include'] = False
        if self._mtexplore_metadata is not None:
            self._mtexplore_metadata = pd.concat([self._mtexplore_metadata,new_df],
                                                 ignore_index=True)
        else:
            self._mtexplore_metadata = new_df

        df_project = self._mtexplore_metadata['project'].unique()
        colors     = [get_hexmap(ix / len(df_project)) for ix in range(len(df_project))]
        for project, color in zip(df_project, colors):
            self._mtexplore_metadata.loc[self._mtexplore_metadata['project'] == project, 'project_color'] = color

    def get_mapping_data(self):
        """

        Returns
        -------
        pandas dataframe with columns ['latitude', 'longitude', 'survey', 'include']

        """
        if self._mtexplore_metadata is not None:
            subframe =  self._mtexplore_metadata.copy(deep=True)
            return subframe
        return pd.DataFrame(columns=self._columns)

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
            if isinstance(target_frame['project'],str):
                project = target_frame['project']
                station = target_frame['station']
            else:   
                project = target_frame['project'].values[0]
                station = target_frame['station'].values[0]
            for database in self._databases:
                mt_object = database.get_record(project, station,type='mtpy')
                if mt_object is not None:
                    break
            return mt_object

        
    def update_selection(self,frame,value):
        print(frame)
        print(value)
        print(frame.index)
        self._mtexplore_metadata.at[frame.index[0], 'include']= value

    def next_cycler_selection(self):
        if self._selection_cycler is not None:
            self._selection_cycler.next_index()
            
    def get_cycler_row(self):
        if self._selection_cycler is not None:
            index = self._selection_cycler.get_selection()
            return self._mtexplore_metadata.iloc[[index]]
        else:
            return None

        
    
       
