import glob
from mtpy.core.mt import MT

class DatabaseModel:

    extension ='.edi'
    def __init__(self,source_directory):
        self.source_directory = source_directory
        self.stations =None

    def set_directory(self,source_directory):
        self.source_directory = source_directory
        self.create_station_list()

    def create_station_list(self):
        files = [f for f in glob.glob(self.source_directory + '**/*'+self.extension,recursive=True)]
        self.stations = [MT(f) for f in files]

    def get_name_loc_dict(self):
        if self.stations is not None:
            return self.create_station_dict_list()
        else:
            return None

    def create_station_dict_list(self):
        station_dict = {}
        for station in self.stations:
            survey = station.Notes.info_dict['SURVEY']
            if survey not in station_dict.keys():
                station_dict[survey] = {}
            key = station.Site.id
            latlon = (station.lat, station.lon)
            station_dict[survey][key] = latlon
        return station_dict