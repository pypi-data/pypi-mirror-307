import numpy as np
from math import floor
from skimage import transform
from abc import ABCMeta, abstractmethod
import os


file_path = os.path.dirname(__file__)


class ProviderC(metaclass=ABCMeta):
    def __init__(self, kwargs):
        """
        initialize the range of latitude and longitude
        :param kwargs:
            :parameter lat_up in [-89.5, 89.5]
            :parameter lat_down in [-89.5, lat_up]
            :parameter lon_left in [-179.5, 179.5]
            :parameter lon_right in [lon_left, 179.5]
        :return self a factory for providing matrix or rho
        """
        self.lat_up = kwargs.get('lat_up', 30)
        self.lat_down = kwargs.get('lat_down', 20)
        self.lon_left = kwargs.get('lon_left', 150)
        self.lon_right = kwargs.get('lon_right', 160)
        """
        :param kwargs:  a dict contains the coordinates of the research area
            :keys   lat_up      top latitude    -89.5~89.5          default 30
                    lat_down    bottom latitude -89.5~lat_up        default 20
                    lon_left    left longitude  -179.5~lon_right    default 150
                    lon_right   right longitude -179.5~179.5        default 160
                    delta-vgg   the name of vgg data in the fold named gravities    default delta-g-3.dg
        """

    @abstractmethod
    def layer(self, layer_number=0):
        pass
        """
        fetch the grid altitude for the assigned layer_number
        :param layer_number     0~8
            0   The elevation of the upper boundary of the water layer
            1   The elevation of the lower boundary of the water layer 
            2   The elevation of the sub-ice border
            3   The elevation of the lower boundary of the upper sedimentary layer
            4   The elevation of the lower boundary of the middle sedimentary layer
            5   The elevation of the lower boundary of the lower sedimentary layer
            6   The elevation of the lower boundary of the upper crust 
            7   The elevation of the lower boundary of the middle crust
            8   The elevation of the lower crustal boundary
        :return an array of resolution 1° × 1° and size is determined by the initialized coordinates 
        """

    @abstractmethod
    def format_layer(self, target_size, layer_number=0, order=3):
        pass
        """
        fetch the grid altitude for the assigned layer_number, 
        and transform to the target_size by interpolation
        :param  target_size a tuple (m, n)  
                layer_number   0~8     default   0
                order          1~5     default   3  used to control the smoothness for interpolation
        :return an array    m × n
                a formative array
        """

    @abstractmethod
    def rho_mean(self, rho_number=0):
        pass
        """
        fetch the mean density for the assigned rho_number  0~8
        :param  rho_number an integrate range in 0 and 8
            0   the density of water layer
            1   the density of ice layer
            2   the density of the upper sedimentary layer
            3   the density of the middle sedimentary layer
            4   the density of the lower sedimentary layer
            5   the density of the upper crust
            6   the density of the middle crust
            7   the density of the lower crust
            8   the density of the Mantle layer
        :return the mean density value of the c
        """
    @classmethod
    def rho_grid(self, rho_number=0):
        """
        calculate the density matrix for rho_number layer of material
        :param rho_number
        :return density matrix
        """
        pass


class CrustModel(ProviderC):
    def __init__(self, kwargs={}):
        """
        :param kwargs:
            :parameter lat_up in [-89.5, 89.5]
            :parameter lat_down in [-89.5, lat_up]
            :parameter lon_left in [-179.5, 179.5]
            :parameter lon_right in [lon_left, 179.5]
        :return self a factory for providing matrix or rho
        """
        super(CrustModel, self).__init__(kwargs)
        self.rho = np.loadtxt(file_path + '/dataset/crust1.rho').reshape((180, 360, 9))
        self.brs = np.loadtxt(file_path + '/dataset/crust1.bnds').reshape((180, 360, 9))

    def layer(self, layer_number=0):
        lat_up, lat_down, lon_left, lon_right = self.lat_up, self.lat_down, self.lon_left, self.lon_right
        ilat_up, ilat_down, ilon_left, ilon_right = floor(90 - lat_up), floor(90 - lat_down), floor(180 + lon_left), \
                                                    floor(180 + lon_right)
        return self.brs[ilat_up:ilat_down+1, ilon_left:ilon_right+1, layer_number]

    def format_layer(self, target_size, layer_number=0, order=3):
        origin_layer = self.layer(layer_number)
        return transform.resize(origin_layer, target_size, order)

    def rho_mean(self, rho_number=0):
        lat_up, lat_down, lon_left, lon_right = self.lat_up, self.lat_down, self.lon_left, self.lon_right
        ilat_up, ilat_down, ilon_left, ilon_right = floor(90 - lat_up), floor(90 - lat_down), floor(180 + lon_left), \
                                                    floor(180 + lon_right)
        return self.rho[ilat_up:ilat_down + 1, ilon_left:ilon_right + 1, rho_number].mean()

    def rho_grid(self, rho_number=0):
        lat_up, lat_down, lon_left, lon_right = self.lat_up, self.lat_down, self.lon_left, self.lon_right
        ilat_up, ilat_down, ilon_left, ilon_right = floor(90 - lat_up), floor(90 - lat_down), floor(180 + lon_left), \
            floor(180 + lon_right)
        return self.rho[ilat_up:ilat_down + 1, ilon_left:ilon_right + 1, rho_number]


if __name__ == "__main__":
    crust = CrustModel(kwargs = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160})
    moho = crust.format_layer(target_size=(251, 251), layer_number=8)

