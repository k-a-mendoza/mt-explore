

class MTControl:

    def __init__(self):
        self._model = None
        self.gen_ended = True

    def add_model(self, model):
        self._model= model.get_database_model()

    def key_press_event(self,event):
        print(event)
        if event.key =='r':
            self.gen_ended=True
        elif event.key=='n':
            self.update_selection()

    def _update_selection(self,*args,**kwargs):
        pass

    def update(self):
        pass

    def update_selection(self):
        selection = self.next_selection()
        self._update_selection(selection)
        self.update()

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
        station_dict = self._model.get_name_loc_mt_dict()
        for survey in station_dict.keys():
            for id, station in station_dict[survey].items():
                yield survey, id, station
        yield False