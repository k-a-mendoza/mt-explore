import glob
import pandas as  pd
import itertools
import os

class DatabaseModel:
    _columns= ['latitude','longitude','elevation','easting','northing','utm zone','rotation angle','station id',
                   'survey','include','file','mt obj']
    extension ='.edi'

    click_precision=(0.05,0.05)

    def __init__(self,mt_facade,source_directory):
        self.mt_facade = mt_facade
        self.source_directory = source_directory
        self._station_df        = None
        self._survey_cycler     = None
        self._selection_cycler  = None

    def set_directory(self,source_directory,facade_class):
        self.source_directory = source_directory
        self._create_station_df(facade_class)

    def save(self,file_path):
        if '.csv' not in file_path:
            file_path=file_path+'.csv'
        if self._station_df is not None:
            df = self._station_df.drop(columns=['mt obj','Unnamed: 0'])
            df.to_csv(file_path)

    def add_new_edi_folder(self,file_path):
        if os.path.isdir(file_path):
            new_df = self._create_df(file_path)
        elif os.path.isfile(file_path):
            new_df = self._create_single_row(file_path)

        df= pd.concat([new_df,self._station_df])
        df.sort_values(['latitude', 'longitude'], inplace=True)
        df.reset_index(inplace=True)
        self._station_df=df

    def new_df_load(self,file_path):
        self.source_directory=file_path
        self._create_station_df()

    def load(self,file_path):
        try:
            df   = pd.read_csv(file_path)
            mt_obj_handle = self.mt_facade.get_MT_obj()
            df['mt obj'] = df['file'].apply(lambda x: mt_obj_handle(x))
            self._station_df = df
        except:
            print('something is wrong. could not read df.csv')
            
    def _get_survey(self,mt_obj):
        #some hacky stuff due to non standard .edi fields
        if not hasattr(mt_obj,'survey'):
            survey_keys = ['survey id','survey']
            key  = None
            keys = list(mt_obj.Notes.info_dict.keys())
            for index, info_dict_key in enumerate(keys):
                if info_dict_key.lower().strip() in survey_keys:
                    key = keys[index]
                    break
            if key is None:
                survey = mt_obj.Site.project
            else:
                survey  = mt_obj.Notes.info_dict[key]
                
            if survey is None:
                survey = 'unknown'
                
        else:
            survey = mt_obj.survey
        
        return survey

    def _create_single_row(self,file):
        mt_obj_handle = self.mt_facade.get_MT_obj()
        mt_obj = mt_obj_handle(file)
        mt_obj.survey = self._get_survey(mt_obj)

        def create_row(mt):
            row = [mt[0].lat, mt[0].lon, mt[0].elev, mt[0].east, mt[0].north, mt[0].utm_zone, mt[0].rotation_angle,
                   mt[0].station,
                   mt[0].survey, 0, mt[1], mt[0]]
            return row

        data = create_row(mt_obj)
        df   = pd.DataFrame(data=data, columns=self._columns)
        df.sort_values(['latitude','longitude'],inplace=True)
        return df

    def _create_df(self, directory,facade_class):
        if isinstance(directory,list):
            files = directory
        else:
            files = [f for f in glob.glob(directory + '**/*' + self.extension, recursive=True)]
        if facade_class is not None:
            mt_handle = facade_class
        else:
            mt_handle = self.mt_facade.get_MT_obj()
        mt_obj_list = [(mt_handle(f), f) for f in files]

        def create_row(mt):
            mt[0].survey = self._get_survey(mt[0])
            row = [mt[0].lat, mt[0].lon, mt[0].elev, mt[0].east, mt[0].north, mt[0].utm_zone, mt[0].rotation_angle,
                   mt[0].station,
                   mt[0].survey, 0, mt[1], mt[0]]
            return row

        data = [create_row(mt) for mt in mt_obj_list]

        df = pd.DataFrame(data=data, columns=self._columns)
        df.sort_values(['latitude', 'longitude'], inplace=True)
        return df

    def _create_station_df(self,facade_class):
        df=self._create_df(self.source_directory,facade_class)
        self._station_df = df


    def get_mapping_data(self):
        """

        Returns
        -------
        pandas dataframe with columns ['latitude', 'longitude', 'survey', 'include']

        """
        if self._station_df is not None:
            return self._station_df[['latitude','longitude','survey','include']]
        return pd.DataFrame(columns=['latitude', 'longitude', 'survey', 'include'])

    def get_included_stations(self):
        df = self.get_mapping_data()
        df = df[df['include']==1]
        return df[['latitude', 'longitude']].copy()

    def get_unique_surveys(self):
        return self._station_df['survey'].unique().tolist()

    def get_survey_indices(self, survey):
        indices = self._station_df.index[self._station_df['survey']==survey].tolist()
        return indices

    def get_indices_matching_extent(self, extent):
        """

        Parameters
        ----------
        extent: list
            lat_minus, lat_plus, lon_minus, lon_plus

        Returns
        -------

        """
        extent['latitude'].sort()
        extent['longitude'].sort()
        indices = self._station_df.index[   (self._station_df['latitude']  > extent['latitude'][0])
                                          & (self._station_df['latitude']  < extent['latitude'][1])

                                          & (self._station_df['longitude'] > extent['longitude'][0])
                                          & (self._station_df['longitude'] < extent['longitude'][1])]

        return indices.tolist()

    def get_series_at_index(self, index):
        if index is not None:
            return self._station_df.loc[index]
        return None

    def set_include(self, selected_index, value):
        self._station_df.loc[selected_index,'include']=value
