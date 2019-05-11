import glob
import pandas as  pd
import itertools
import os
from tkinter import filedialog
import tkinter as tk
class DatabaseModel:
    _columns= ['latitude','longitude','elevation','easting','northing','utm zone','rotation angle','station id',
                   'survey','include','file','mt obj']
    extension ='.edi'

    click_precision=(0.05,0.05)

    def __init__(self,mt_facade,source_directory):
        self.mt_facade=mt_facade
        self.source_directory = source_directory
        self._station_df        = None
        self._survey_cycler     = None
        self._selection_cycler  = None

    def set_directory(self,source_directory):
        self.source_directory = source_directory
        self._create_station_df()

    def save(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select .csv save location")
        file = file_path + os.sep + 'df.csv'
        if self._station_df is not None:
            df = self._station_df.drop(columns='mt obj')
            df.to_csv(file)

    def new_df_load(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title = "Select .edi database directory")
        self.source_directory=file_path
        self._create_station_df()

    def load(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title = "Select .csv database")
        try:
            df   = pd.read_csv(file_path)
            mt_obj_handle = self.mt_facade.get_MT_obj()
            df['mt obj'] = df['file'].apply(lambda x: mt_obj_handle(x))
            self._station_df = df
        except:
            print('something is wrong. could not read df.csv')

    def _create_station_df(self):
        files = [f for f in glob.glob(self.source_directory + '**/*'+self.extension,recursive=True)]
        mt_obj_handle = self.mt_facade.get_MT_obj()
        mt_obj_list = [(mt_obj_handle(f),f) for f in files]
        def create_row(mt):
            row = [mt[0].lat, mt[0].lon, mt[0].elev, mt[0].east, mt[0].north, mt[0].utm_zone, mt[0].rotation_angle, mt[0].station,
                    mt[0].survey,0,mt[1],mt[0]]
            return row

        data = [create_row(mt) for mt in mt_obj_list]

        self._station_df = pd.DataFrame(data=data, columns=self._columns)
        self._station_df.sort_values(['latitude','longitude'],inplace=True)

    def get_mapping_data(self):
        """

        Returns
        -------
        pandas dataframe with columns ['latitude', 'longitude', 'survey', 'include']

        """
        if self._station_df is not None:
            return self._station_df[['latitude','longitude','survey','include']]
        return pd.DataFrame(columns=['latitude', 'longitude', 'survey', 'include'])


    def next_selection(self):
        if self._survey_cycler is None:
            self.create_survey_cycler()

        if self._selection_cycler is None:
            self.create_selection_cycler()
        self._selection_cycler.next()

    def next_survey(self):
        if self._survey_cycler is None:
            self.create_survey_cycler()
        self._survey_cycler.next()
        self.create_selection_cycler()

    def create_survey_cycler(self):
        unique_surveys = list(self._station_df['survey'].unique())
        self._survey_cycler = ListCycler(unique_surveys)

    def create_selection_cycler(self,extent=None):
        if extent is None:
            sub_df = self._station_df[self._station_df['survey']==self._survey_cycler.get_selected()]
            self._selection_cycler = DfCycler(sub_df)
        else:
            df = self._station_df
            latitudes = [extent[0],extent[1]]
            longitudes =[extent[2],extent[3]]
            longitudes.sort()
            latitudes.sort()
            df = df[(df['latitude']  > latitudes[0])  & (df['latitude']  < latitudes[1]) & \
                    (df['longitude'] > longitudes[0]) & (df['longitude'] < longitudes[1])]
            self._selection_cycler = DfCycler(df)


    def get_selection(self):
        selected = self._selection_cycler.get_selected()
        return selected

    def get_clicked_selection(self,lat,lon,radius):
        latp =lat + radius
        latm =lat - radius
        lonp =lon + radius
        lonm =lon - radius
        df = self._station_df[(self._station_df['latitude'] < latp) & (self._station_df['latitude'] > latm) & \
                              (self._station_df['longitude'] < lonp) & (self._station_df['longitude'] > lonm)]
        if df.empty:
            return None
        else:
            return df.iloc[0]

    def update_selection(self,value):
        selected = self._selection_cycler.get_selected()
        station = selected['station id']
        survey  = selected['survey']
        index = self._station_df[(self._station_df['station id']==station) & (self._station_df['survey']==survey)].index.values
        self._station_df.at[index[0], 'include'] = value

class ListCycler:
    def __init__(self, lt):
        self.list = lt
        self.generator = self.cycle()
        self.selected  = next(self.generator)

    def cycle(self):
        if self.is_empty():
            for row in itertools.cycle(self.get_iter()):
                yield self.row_ops(row)
        else:
            while True:
                yield None


    def get_iter(self):
        return self.list

    def is_empty(self):
        return self.list

    def row_ops(self,row):
        return row

    def next(self):
        self.selected = next(self.generator)

    def get_selected(self):
        return self.selected

class DfCycler(ListCycler):

    def __init__(self,df):
        super().__init__(df)

    def row_ops(self,row):
        return row[1]

    def is_empty(self):
        return not self.list.empty

    def get_iter(self):
        return self.list.iterrows()
