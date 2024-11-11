import os
from skimage import transform
import numpy as np
import netCDF4 as nc
import requests


file_path = os.path.dirname(__file__)

vgg_url = 'https://topex.ucsd.edu/pub/global_grav_1min/curv_32.1.nc'


class Vgg:
    def __init__(self, kwargs):
        """
        A worker for providing vgg data with
            latitude range -79.99166667~79.99166667
            longitude range -179.99166667~179.99166667
        :param kwargs:
            :parameter lat_up in [-79.99166667, 79.99166667 ]
            :parameter lat_down in [-79.99166667, lat_up]
            :parameter lon_left in [-179.99166667, 179.99166667]
            :parameter lon_right in [lon_left, 179.99166667]
        :return self a factory for providing vertical gravity gradient data
        """
        self.lat_up = kwargs.get('lat_up')
        self.lat_down = kwargs.get('lat_down')
        self.lon_left = kwargs.get('lon_left')
        self.lon_right = kwargs.get('lon_right')

    def vgg(self):
        """
        fetch vertical gravity gradient data
        :return: matrix with resolutioin of 1'×1'
        """
        if not os.path.exists(file_path + '/dataset/curv_32.nc'):
            print("download vgg data from https://topex.ucsd.edu/pub/global_grav_1min/curv_32.1.nc...\n"
                  "We strongly recommend you download the vgg data yourself and put the file curv_32.nc into\n"
                  "the dataset directory in package multi-interface-inversion. If not, please wait 10mins for\n"
                  "the first time and make sure the directory dataset be writable!\n")
            response = requests.get(vgg_url)
            with open(file_path + '/dataset/curv_32.nc', 'wb') as file:
                file.write(response.content)
        vgg_nc = nc.Dataset(file_path + '/dataset/curv_32.nc', 'r')
        lat_up, lat_down, lon_left, lon_right = self.lat_up, self.lat_down, self.lon_left, self.lon_right
        lons, lats, z = vgg_nc.variables['lon'][:].data, vgg_nc.variables['lat'][:].data, \
                        vgg_nc.variables['z'][:].data
        lon_step, lat_step = np.mean(lons[1:] - lons[:-1]), np.mean(lats[1:] - lats[:-1])
        rlat_up, rlat_down, rlon_left, rlon_right = np.round((lats[-1] - lat_up) / lat_step), \
                                                    np.round((lats[-1] - lat_down) / lat_step), \
                                                    np.round((lon_left - lons[0]) / lon_step), \
                                                    np.round((lon_right - lons[0]) / lon_step)
        ilat_up, ilat_down, ilon_left, ilon_right = int(rlat_up), int(rlat_down), int(rlon_left), int(rlon_right)
        z = np.flip(z, axis=0)
        return z[ilat_up: ilat_down + 1, ilon_left: ilon_right + 1]

    def vgg_format(self, target_size, order=3):
        """
        fetch vertical gravity gradient data and transformed to the target size with smoothness function of order, default 3
        :param target_size: a tuple (nrow × ncol)
        :param order: an integer default 3
        :return: a matrix
        """
        vgg = self.vgg()
        return transform.resize(vgg, target_size, order)


if __name__ == "__main__":
    kwargs = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160}
    vgg_factor = Vgg(kwargs=kwargs)
    vgg_origin = vgg_factor.vgg()


