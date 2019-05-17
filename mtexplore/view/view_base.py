import matplotlib.pyplot as plt
import pandas as pd

class ViewContract:

    def __init__(self,view,*args,**kwargs):
        self.view = view

    def add_axes(self,*args,**kwargs):
        return self.view.add_axes(*args,**kwargs)

    def map(self,df: pd.DataFrame):
        self._map(df)
        self.view.map(df)

    def update(self):
        self._update()
        self.view.update()

    def finish(self):
        self._finish()
        self.view.finish()

    def set_default_df(self, df):
        self._set_default_df(df)
        self.view.set_default_df(df)

    def get_axes_of_click(self,event):
        in_axes = self._is_in_axes(event)
        if in_axes is None:
            return self.view.get_axes_of_click(event)
        else:
            return in_axes

    def update_selection(self,series):
        self._update_selection(series)
        self.view.update_selection(series)

    def get_figure(self) -> plt.Figure:
        return self.view.get_figure()

    def set_figure(self,fig):
        self.view.set_figure(fig)

    def configure(self):
        self.view.configure()
        self._configure()

    def get_extent(self):
        extent = self._get_extent()
        if extent is None:
            return self.view.get_extent()
        return extent

    def zoom(self,**kwargs):
        self._zoom(**kwargs)
        self.view.zoom(**kwargs)

    def _finish(self):
        pass

    def _update_selection(self,series):
        pass

    def _get_extent(self):
        return None

    def _map(self,df):
        pass

    def _configure(self):
        pass

    def _update(self):
        """
        do any self updating of views. DONT USE THIS to call flush or draw
        :return:
        """
        pass

    def get_axes(self,*args,**kwargs) -> plt.Axes:
        """
        allows inherited objects to get an axis instance from the main figure

        see: https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html for args & kwargs
        :param args: 
        :param kwargs:

        :return: a matplotlib axis instance
        """
        return self.view.get_axes(*args,**kwargs)

    def _is_in_axes(self, event):
        pass

    def _set_default_df(self, df):
        pass

    def _zoom(self,**kwargs):
        pass

class BaseView(ViewContract):

    def __init__(self,dimensions):
        super().__init__(None)


    def configure(self):
        pass

    def update(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def add_axes(self, *args, **kwargs):
        return self.fig.add_axes(*args, **kwargs)

    def get_figure(self):
        return self.fig

    def set_figure(self,fig):
        self.fig = fig

    def map(self,df):
        pass

    def zoom(self,**kwargs):
        pass

    def finish(self):
        self.fig.canvas.draw()

    def update_selection(self, series):
        self.update()

    def is_in_axes(self, event):
        return 'background'

    def set_default_df(self, df):
        pass