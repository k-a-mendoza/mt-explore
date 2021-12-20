from .view_base import ViewContract
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.cm as colormap
import numpy as np
import pandas as pd
import matplotlib.colors as mplcolors
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.img_tiles import Stamen
import collections
from owslib.wmts import TileMatrixSetLink, TileMatrixLimits, _TILE_MATRIX_SET_TAG, _TILE_MATRIX_SET_LIMITS_TAG, _TILE_MATRIX_LIMITS_TAG

class MapView(ViewContract):
    map_position=[0.05,0.5,0.45,0.4]
    base_extent   = [-130,-100,20,50]
    _colormap = colormap.get_cmap('nipy_spectral')

    s1 = 20
    s2 = 50
    s3 = 50
    lw = 0.8
    _legend_kwargs = dict(ncol=5,loc='lower left',fontsize=7)
    _none_color='none'
    _include='green'
    _exclude='red'
    _scatter_kwargs_data   = dict(s=s1,linewidths=lw,zorder=3,marker='o')
    _scatter_kwargs_nodata = dict(s=s1,linewidths=lw,zorder=3,marker='P')
    _selection_kwargs = dict(marker='o',
                             facecolor='none',
                            edgecolor='white',
                            s=s2,
                            zorder=6,
                            linewidths=2)
    _include_kwargs = dict(marker='o',
                             facecolor='none',
                            edgecolor='black',
                            s=s3,
                            zorder=5,
                            linewidths=3)

    _mesh_kwargs = dict(color='white')
    _state_feature = dict(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')
    _nation_feature = dict(
        category='cultural',
        name='admin_0_states_provinces_lines',
        scale='50m',
        facecolor='none')

    def __init__(self,view):
        super().__init__(view)
        self.selection_id=None
        self.selection_handle=None
        self.base_scatter_handles = []
        self.selected_scatter_handle = None
        self.legend = None
        self.extent = [] + self.base_extent
        self._projects=[]
        self._control_points={'x':[],
                              'y':[]}
        self.base_scale = 1.2
        self.gl = None

    def colormap(self,val):
        rgb = self._colormap(val)
        return mplcolors.to_hex(rgb)

    def _configure(self):
        self.ax = self.add_axes(self.map_position,projection=ccrs.PlateCarree())
        states_provinces = cfeature.NaturalEarthFeature(**self._state_feature)
        countries        = cfeature.BORDERS
        url = 'https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'
        layer = 'ASTER_GDEM_Color_Shaded_Relief'
        self.ax.add_wmts(url, layer,alpha=0.8)
        self.ax.coastlines(resolution='50m',zorder=10)
        self.ax.add_feature(states_provinces, edgecolor='black',zorder=2,linewidth=1.5)
        self.ax.add_feature(countries, edgecolor='black', zorder=2, linewidth=2)

   
    def _update_selection(self,station_data):
        if self.selection_handle is not None:
            self._erase_selection()
        if station_data['project'] is None:
            return None
        
        df = station_data['project']
        project = df['project'].values[0]
        station     = df['station'].values[0]

        self.selection_handle = self.ax.scatter(df['longitude'],
                                                df['latitude'],**self._selection_kwargs)
        self.ax.set_title(f'Project: {project}, Station: {station}')

    def _add_xaxis_line(self,x):
        self._control_points['x'].append(x)

    def _add_yaxis_line(self,y):
        self._control_points['y'].append(y)


    def _erase_selection(self):
        if self.selection_handle is not None:
            self.selection_handle.remove()
            del self.selection_handle
            self.selection_handle=None

    def _erase_scatter(self):
        for handle in self.base_scatter_handles:
            handle.remove()
            del handle
        self.scatter_handle=[]
        
    def _erase_scatter_selection(self):
        if self.selected_scatter_handle is not None:
            self.selected_scatter_handle.remove()
            del self.selected_scatter_handle
            self.selected_scatter_handle=None

    def _is_in_axes(self, event):
        if event.inaxes == self.ax:
            return 'map'
        return None
    
    def _map(self,df):
        self.plot_include(df)


    def plot_scatter(self,df):
        if not df.empty:
            df = self.assign_project_colors(df)
            self._erase_scatter()
                
            self.ax.scatter(df['longitude'],df['latitude'],
                                                c=df['color'],**self._scatter_kwargs_data)

            
            
    def plot_include(self,df):
        if not df.empty:
            self._erase_scatter_selection()
            df = df[df.include]
            self.ax.scatter(df['longitude'],df['latitude'],**self._include_kwargs)
            

    def _get_extent(self):
        ylim = self.ax.get_ylim()
        xlim = self.ax.get_xlim()
        return (xlim, ylim)

    def assign_project_colors(self,df):
        df_project = df['project'].unique()
        color_dict = {}
        for ix, project in enumerate(df_project):
            color_dict[project]= self.colormap(ix/len(df_project))

        for key,value in color_dict.items():
            df.at[df['project']==key,'color']=value
        df.at[df['include'] == 0, 'qual color'] = self._none_color
        df.at[df['include'] == 1, 'qual color'] = self._include
        return df

    def prep_legend(self,df):
        items = list(df['project'].unique())
        if self.legend is not None:
            self.legend.remove()
        handles=[]
        for ix, project in enumerate(items):
            color = self.colormap(ix / len(items))
            handle = self.ax.scatter([], [], label=project, c=color, edgecolors='none', s=self.s1,linewidths=self.lw)
            handles.append(handle)

       
        self.legend=self.ax.legend(handles,items,**self._legend_kwargs)

    def set_default_extent(self,df):
        extent = [None,None,None,None]
        if df is not None:
            extent[0]=df['longitude'].min()
            extent[1]=df['longitude'].max()
            extent[2]=df['latitude'].min()
            extent[3]=df['latitude'].max()
            x_delta = extent[1] - extent[0]
            y_delta = extent[3] - extent[2]
            x_delta *= 1.1
            y_delta *= 1.1
            x_left = (extent[0] + extent[1]) / 2.0 - x_delta / 2
            x_right= (extent[0] + extent[1]) / 2.0 + x_delta / 2
            y_down = (extent[2] + extent[3]) / 2.0 - y_delta / 2 - y_delta / 3
            y_up   = (extent[2] + extent[3]) / 2.0 + y_delta / 2
            extent =  [x_left, x_right, y_down, y_up]
            self.ax.set_xlim([x_left,x_right])
            self.ax.set_ylim([y_down,y_up])

    def _set_default_df(self, df):
        self.prep_legend(df)
        self.plot_scatter(df)
        self.set_default_extent(df)

    def _zoom(self,**kwargs):
        self._update_map_extent(**kwargs)

    def _update_map_extent(self, center=None, zoom=None):
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = center[0] # get event x location
        ydata = center[1] # get event y location
        if zoom == 'in':
            # deal with zoom in
            scale_factor = 1/self.base_scale
        elif zoom == 'out':
            # deal with zoom out
            scale_factor = self.base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
          
        # set new limits
        self.ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        self.ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
  


    def get_xyq_values_for_project(self, stations, project):
        x_values = []
        y_values = []
        q_values = []
        for id, entry in stations[project].items():
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

def custom_from_elements(link_elements):
    links = []
    for link_element in link_elements:
        matrix_set_elements = link_element.findall(_TILE_MATRIX_SET_TAG)
        if len(matrix_set_elements) == 0:
            raise ValueError('Missing TileMatrixSet in %s' % link_element)
        elif len(matrix_set_elements) > 1:
            set_limits_elements = link_element.findall(
                _TILE_MATRIX_SET_LIMITS_TAG)
            if set_limits_elements:
                raise ValueError('Multiple instances of TileMatrixSet'
                                  ' plus TileMatrixSetLimits in %s' %
                                  link_element)
            for matrix_set_element in matrix_set_elements:
                uri = matrix_set_element.text.strip()
                links.append(TileMatrixSetLink(uri))
        else:
            uri = matrix_set_elements[0].text.strip()

            tilematrixlimits = {}
            path = '%s/%s' % (_TILE_MATRIX_SET_LIMITS_TAG,
                              _TILE_MATRIX_LIMITS_TAG)
            for limits_element in link_element.findall(path):
                tml = TileMatrixLimits(limits_element)
                if tml.tilematrix:
                    tilematrixlimits[tml.tilematrix] = tml

            links.append(TileMatrixSetLink(uri, tilematrixlimits))
    return links

#TileMatrixSetLink.from_elements = custom_from_elements

