import pandas as pd
import pyproj
import numpy as np

class GridModel:
    letters = ['C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X']
    geod = pyproj.Geod(ellps='WGS84')
    def __init__(self):
        self.grid_df = pd.DataFrame(columns=['latitude','longitude',
                                             'northing','easting',
                                             'utm_zone','utm_band',
                                             'point_type'])

        self.zones = self.create_zones()

    def create_zones(self):
        zones = {}
        for zone in range(1,61):
            zones[str(zone)]=pyproj.Proj(proj='utm', zone=zone, ellps='WGS84', preserve_units=True)
        return zones


    def add_control_point(self,type,location):
        self.grid_df=self.grid_df.append(self._create_row_from_data(type,location),ignore_index=True)


    def _create_row_from_data(self,type,location):
        row = {
            'point_type': type,
            'latitude' : location[1],
            'longitude': location[0],
            'utm_zone' : None,
            'utm_band' : None,
            'northing' : None,
            'easting'  : None
        }
        if type=='x':
            del row['latitude']
        else:
            del row['longitude']
        return row

    def zone_number(self,longitude):
        return str(int(np.round((longitude + 180)/6)))

    def zone_letter(self,latitude):
        latitude_index = int(np.floor((latitude + 80)/8))
        return self.letters[latitude_index]

    def get_gridpoints(self):
        grid_x = self.grid_df[self.grid_df['point_type']=='x']['longitude'].tolist()
        grid_y = self.grid_df[self.grid_df['point_type']=='y']['latitude'].tolist()

        return grid_x, grid_y


    def create_easting_northing(self,point):
        print(point)
        zone_number = self.zone_number(point[0])
        zone_letter = self.zone_letter(point[1])
        print('{}{}'.format(zone_letter,zone_number))
        easting, northing = self.zones[zone_number](*point)

        return int(zone_number), zone_letter, easting, northing



    def load_grid(self,file):
        df = pd.read_csv(file)
        x_unique = df['longitude'].unique().tolist()
        y_unique = df['latitude'].unique().tolist()
        for x in x_unique:
            df=df.append({'longitude':x,'point_type':'x'})
        for y in y_unique:
            df=df.append({'latitude':y,'point_type':'y'})
        self.grid_df=df



    def save_grid(self, file_path):
        df = self.grid_df.copy()
        points = self.create_full_grid(df)
        print(points)
        data = []
        for point in points:
            print(point)
            zone_number, zone_letter, easting, northing = self.create_easting_northing(point)
            row={
            'latitude' : point[1],
            'longitude': point[0],
            'easting'  : int(easting),
            'northing' : int(northing),
            'utm_zone' : zone_number,
            'utm_band' : zone_letter
            }
            data.append(row)

        df = pd.DataFrame(data,columns=list(data[0].keys()))
        df.to_csv(file_path)

    def create_full_grid(self, df):
        points = []
        for y in df['latitude'].dropna().tolist():
            for x in df['longitude'].dropna().tolist():

                points.append((x, y))
        return points

    def delete_closest_gridline(self, location):
        x = location[0]
        y = location[1]
        print('1')
        df = self.grid_df.copy()
        df['latitude']=df['latitude']-y
        df['longitude']=df['longitude']-x
        lat_diff = df['latitude'].min()
        lon_diff = df['longitude'].min()
        print('2')
        # problem is that deleting is hard to do
        if lat_diff > lon_diff:
            index_to_drop = df['longitude'].idxmin()
        else:
            index_to_drop = df['latitude'].idxmin()
        print('3')

        print(index_to_drop)

        self.grid_df.drop(labels=index_to_drop,inplace=True)
        print('4')

