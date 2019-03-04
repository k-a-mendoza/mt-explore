from ..model.model import  Model

class MapController:

    def __init__(self):
        self.gen_ended = True

    def button_press_event(self,event):
        print(event)

    def key_press_event(self,event):
        print(event)
        if event.key =='r':
            self.update_all_stations()
        elif event.key=='n':
            self.update_selection()

    def add_model(self, model: Model):
        self._model = model.get_database_model()

    def _update_all_stations(self,*args,**kwargs):
        pass

    def _update_extent(self,*args,**kwargs):
        pass

    def _update_selection(self,*args,**kwargs):
        pass

    def update(self):
        pass

    def update_all_stations(self,*args,**kwargs):
        station_dict = self._model.get_name_loc_dict()
        if station_dict is not None:
            self._update_all_stations(stations=station_dict)
            extent = self._get_extent(station_dict)
            self._update_extent(extent=extent)
        self.update()

    def update_selection(self):
        selection = self.next_selection()
        self._update_selection(selection)
        self.update()

    def _get_extent(self,dict_of_dicts):
        x_values = []
        y_values = []
        for survey in dict_of_dicts.keys():
            for station,latlon in dict_of_dicts[survey].items():
                x_values.append(latlon[1])
                y_values.append(latlon[0])

        x_min = min(x_values)
        x_max = max(x_values)
        y_min = min(y_values)
        y_max = max(y_values)
        extent = [x_min, x_max, y_min, y_max]
        return extent

    def next_selection(self):
        if self.gen_ended:
            self.new_generator = self.station_generator()
            self.gen_ended=False
        next_item = next(self.new_generator)
        if next_item is False:
            self.gen_ended = True
            return self.next_selection()
        else:
            return next_item

    def station_generator(self):
        station_dict = self._model.get_name_loc_dict()
        for survey in station_dict.keys():
            for station, location in station_dict[survey].items():
                yield survey, station, location
        yield False

