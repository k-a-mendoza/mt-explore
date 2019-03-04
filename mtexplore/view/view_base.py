import matplotlib.pyplot as plt


class ViewContract:

    def __init__(self,view,*args,**kwargs):
        self.view = view

    def add_axes(self,*args,**kwargs):
        return self.view.add_axes(*args,**kwargs)

    def add_controller(self,controller):
        self._add_controller(controller)
        self.view.add_controller(controller)

    def _add_controller(self,controller):
        pass

    def update(self):
        self._update()
        self.view.update()

    def finish(self):
        self._finish()
        self.view.finish()

    def _finish(self):
        pass

    def get_figure(self) -> plt.Figure:
        return self.view.get_figure()

    def configure(self):
        self.view.configure()
        self._configure()

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

class BaseView(ViewContract):

    def __init__(self,dimensions):
        super().__init__(None)
        self.fig = plt.figure(figsize=dimensions)
        self.fig.canvas.mpl_connect('key_press_event',self.test_event)

    def configure(self):
        pass

    def add_controller(self,controller):
        controller.set_events(self.fig)

    def test_event(self,event):
        print(event)

    def update(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def add_axes(self, *args, **kwargs):
        return self.fig.add_axes(*args, **kwargs)

    def get_figure(self):
        return self.fig

    def finish(self):
        print('showing fig')
        self.fig.canvas.draw()
