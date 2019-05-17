
from .database_model import DatabaseModel
import itertools
from tkinter import filedialog
import tkinter as tk
import pandas as pd

class ModelController:

    def __init__(self,mt_facade=None, working_directory=None,source_directory=None,**kwargs):
        self.database_model    = DatabaseModel(mt_facade,source_directory)
        self._survey_cycler    = None
        self._selection_cycler = None

    def set_database_directory(self,directory):
        self.database_model.set_directory(directory)

    def add_new_edi_folder(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(title='select .edi database directory')
        self.database_model.add_new_edi_folder(file_path)

    def save(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(title="Select .csv save location")
        self.database_model.save(file_path)

    def load(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Select .csv database")
        self.database_model.load(file_path)

    def new_df_load(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(title="Select .edi database directory")
        self.database_model.new_df_load(file_path)

    def get_mapping_data(self)-> pd.DataFrame:
        return self.database_model.get_mapping_data()

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
        unique_surveys      = self.database_model.get_unique_surveys()
        self._survey_cycler = ListCycler(unique_surveys)

    def create_selection_cycler(self,extent=None):
        if extent is None:
            survey = self._survey_cycler.get_selected()
            survey_indices = self.database_model.get_survey_indices(survey)
            self._selection_cycler = ListCycler(survey_indices)
        else:
            station_indices = self.database_model.get_indices_matching_extent(extent)
            self._selection_cycler = ListCycler(station_indices)


    def get_selection(self):
        selected_index = self._selection_cycler.get_selected()
        return self.database_model.get_series_at_index(selected_index)


    def update_selection(self,value):
        selected_index = self._selection_cycler.get_selected()
        self.database_model.set_include(selected_index,value)


    def update_cycle_selection(self,value):
        indices = self._selection_cycler.list
        print('selection {}'.format(indices))
        self.database_model.set_include(indices,value)


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
