from .view_base import ViewContract
from ..controller.controller import MainController
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.cm as colormap
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

class MapView(ViewContract):
    map_position=[0.1,0.3,0.6,0.8]
    extent   = [-180,180,-90,90]
    colormap = colormap.get_cmap('hsv')
    s1 = 10
    s2 = 40

    def __init__(self,view):
        super().__init__(view)
        self.selection_id=None
        self.selection_handle=None

    def _add_controller(self,controller: MainController):
        controller.get_map_controller()._update_all_stations = self.plot_stations
        controller.get_map_controller()._update_extent       = self.update_extent
        controller.get_map_controller()._update_selection    = self.update_selection
        controller.get_map_controller().update = self.update

    def _configure(self):
        self.ax = self.add_axes(self.map_position,projection=ccrs.PlateCarree())
        self.ax.set_extent(self.extent,crs=ccrs.PlateCarree())
        states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')

        self.ax.coastlines(resolution='50m')
        self.ax.stock_img()
        self.ax.add_feature(cfeature.LAND)
        self.ax.add_feature(states_provinces, edgecolor='gray')

    def update_selection(self,station_data):
        if self.selection_handle is not None:
            self._erase_selection()
            print('erased selection')

        survey = station_data[0]
        id     = station_data[1]
        latlon = station_data[2]
        scatter_handle = self.ax.scatter(latlon[1],latlon[0],
                                         marker='o',
                                         edgecolor='red',
                                         s=self.s2,
                                         zorder=5,
                                         facecolor='None',
                                         linewidths=2)
        print("printing{}:{}".format(latlon[1],latlon[0]))
        self.ax.set_title('Survey: {}, Station: {}'.format(survey,id))
        self.selection_handle = scatter_handle

    def _erase_selection(self):
        self.selection_handle.remove()


    def plot_stations(self,stations=None, x_values=[], y_values=[]):
        survey_length = float(len(stations.keys()))
        for index, survey in enumerate(stations.keys()):
            x_values, y_values = self.get_xy_values_for_survey(stations, survey)
            color = self.colormap(index/survey_length)
            self.ax.scatter(x_values,y_values,label=survey,edgecolor='black',facecolor=color,s=self.s1)

        ncols = int(survey_length/3)
        self.ax.legend(ncol=ncols,loc='lower left')

    def update_extent(self,extent=[-180,180,-90,90]):
        x_max, x_min, y_max, y_min = self._get_plot_extent(extent)

        self.ax.set_xlim([x_min,x_max])
        self.ax.set_ylim([y_min,y_max])
        self.set_latlon_grids()

    def set_latlon_grids(self):
        gl = self.ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                               alpha=0.5, linestyle='--', color='black')
        gl.xlabels_top = False
        gl.xlocator = mticker.AutoLocator()
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

    def _get_plot_extent(self, extent):
        x_delta = extent[1] - extent[0]
        y_delta = extent[3] - extent[2]
        x_delta *= 1.1
        y_delta *= 1.1
        x_min = (extent[0] + extent[1]) / 2.0 - x_delta / 2
        x_max = (extent[0] + extent[1]) / 2.0 + x_delta / 2
        y_min = (extent[2] + extent[3]) / 2.0 - y_delta / 2 - y_delta / 4
        y_max = (extent[2] + extent[3]) / 2.0 + y_delta / 2
        return x_max, x_min, y_max, y_min

    def get_xy_values_for_survey(self, stations, survey):
        x_values = []
        y_values = []
        for key, latlon in stations[survey].items():
            x_values.append(latlon[1])
            y_values.append(latlon[0])
        return x_values, y_values
