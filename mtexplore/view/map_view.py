from view.view_base import ViewContract
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.cm as colormap
import matplotlib.colors as mplcolors
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.img_tiles import Stamen
import collections
class MapView(ViewContract):
    map_position=[0.05,0.5,0.4,0.4]
    extent   = [-130,-100,20,50]
    _colormap = colormap.get_cmap('hsv')

    s1 = 20
    s2 = 50
    lw = 0.8
    _none_color='none'
    _include='green'
    _exclude='red'
    _scatter_kwargs = dict(s=s1,linewidths=lw,zorder=3,label=None)
    _selection_kwargs = dict(marker='o',
                            edgecolor='red',
                            s=s2,
                            zorder=5,
                            facecolor='None',
                            linewidths=2)
    _cult_feature_nat_earth = dict(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')

    def __init__(self,view):
        super().__init__(view)
        self.selection_id=None
        self.selection_handle=None
        self.scatter_handle = None
        self.legend = None
        self._surveys=[]

    def colormap(self,val):
        rgb = self._colormap(val)
        return mplcolors.to_hex(rgb)

    def _configure(self):
        self.ax = self.add_axes(self.map_position,projection=ccrs.PlateCarree())
        states_provinces = cfeature.NaturalEarthFeature(**self._cult_feature_nat_earth)
        url = 'https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'
        layer = 'ASTER_GDEM_Color_Shaded_Relief'
        self.ax.add_wmts(url, layer,alpha=0.8)
        self.ax.coastlines(resolution='50m',zorder=10)
        self.ax.add_feature(states_provinces, edgecolor='black',zorder=2,linewidth=2)

    def _update_selection(self,station_data):
        if self.selection_handle is not None:
            self._erase_selection()

        survey = station_data['survey']
        id     = station_data['station id']

        self.selection_handle = self.ax.scatter(station_data['longitude'],station_data['latitude'],**self._selection_kwargs)
        self.ax.set_title('Survey: {}, Station: {}'.format(survey,id))

    def _erase_selection(self):
        self.selection_handle.remove()
        del self.selection_handle
        self.selection_handle=None

    def _erase_scatter(self):
        self.scatter_handle.remove()
        del self.scatter_handle
        self.scatter_handle=None

    def _is_in_axes(self, event):
        x,y = event.x, event.y
        if event.inaxes == self.ax:
            return 'map'
        return None


    def map(self,df):
        if not df.empty:
            df = self.assign_survey_colors(df)
            if self.scatter_handle is not None:
                self._erase_scatter()
            self.scatter_handle=self.ax.scatter(df['longitude'],df['latitude'],edgecolors=df['color'],c=df['qual color'],**self._scatter_kwargs)
            self._check_legend(df)
            self.update_extent(df)

    def _get_extent(self):
        ylim = self.ax.get_ylim()
        xlim = self.ax.get_xlim()
        return (xlim, ylim)

    def assign_survey_colors(self,df):
        df_survey = df['survey'].unique()
        color_dict = {}
        for ix, survey in enumerate(df_survey):
            color_dict[survey]= self.colormap(ix/len(df_survey))

        for key,value in color_dict.items():
            df.at[df['survey']==key,'color']=value
        df.at[df['include'] == 0, 'qual color'] = self._none_color
        df.at[df['include'] == 1, 'qual color'] = self._include
        return df

    def _check_legend(self,df):
        items = collections.Counter(df['survey'].unique())
        if self.legend is not None:
            self.legend.remove()
        handles=[]
        for ix, survey in enumerate(items):
            color = self.colormap(ix / len(items))
            handle = self.ax.scatter([], [], label=survey, edgecolors=color, c='none', s=self.s1,linewidths=self.lw)
            handles.append(handle)

        self.ax.scatter([], [], label='exclude station',  edgecolors='black',   c=self._none_color)
        self.ax.scatter([], [], label='include station', edgecolors='black', c=self._include)
        ncols = int((len(items)+3)/3)
        self.legend=self.ax.legend(handles,items,ncol=ncols,loc='lower left')


    def update_extent(self,df):
        extent = [x for x in self.extent]
        if df is not None:
            extent[0]=df['longitude'].min()
            extent[1]=df['longitude'].max()
            extent[2]=df['latitude'].min()
            extent[3]=df['latitude'].max()

        x_max, x_min, y_max, y_min = self._get_plot_extent(extent)
        self.ax.set_extent([x_min,x_max,y_min,y_max],crs=ccrs.PlateCarree())
        self.set_latlon_grids()
        self.update()

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
        y_min = (extent[2] + extent[3]) / 2.0 - y_delta / 2 - y_delta / 3
        y_max = (extent[2] + extent[3]) / 2.0 + y_delta / 2
        return x_max, x_min, y_max, y_min

    def get_xyq_values_for_survey(self, stations, survey):
        x_values = []
        y_values = []
        q_values = []
        for id, entry in stations[survey].items():
            q_values.append(self.get_color_value(entry[1]))
            x_values.append(entry[0][1])
            y_values.append(entry[0][0])
        return x_values, y_values, q_values

    def get_color_value(self,value):
        if value is None:
            return self._none_color
        elif value=='1':
            return self._passing_color
        elif value=='2':
            return self._marginal_color
        else:
            return self._failing_color

