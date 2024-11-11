from scipy.fftpack import fft2, ifft2
import numpy as np
from abc import ABCMeta, abstractmethod
from math import factorial
from scipy.signal.windows import tukey


class VggToInterface(metaclass=ABCMeta):
    def __init__(self, vgg, coarse_sediment, coarse_thickness, delta_rhos, delta_rho_initial,
                 reference_depths, longrkm, longckm, wh, alpha, age):
        """
        initialize the inputs and parameters
        :param vgg: matric for vertical gravity gradient
        :param coarse_sediment: matrix represents a coarse estimate of the second interface fluctuation
        :param coarse_thickness: matrix represents the thickness between the first and second interface
        :param delta_rhos: a dict with keys:0, 1, 2, …; values: float0, float1, …
                            for the density contrast of the density interfacesz
        :param delta_rho_initial: float the density contrast for the crust upper bound in the senario with one interface
        :param reference_depths: a dict with keys: 0, 1, 2, …; values: float0, float1,…
                                    positive float stands for the reference plane
        :param longrkm: distance from the upper bound latitude to the lower bound latitude
        :param longckm: distance from the left bound longitude to the right bound longitude
        :param target_layer: int stands for the number of the interface of interest
        :param wh: float e.g. 0.1 for cutting off the high order frequency
        :param alpha: int e.g. 8 for the punishment of the high order frequency
        :param age: float range in [0, 1] stands for the smoothness of sediment layer
        :param crust_provider: a Provider object for providing layer information for sdt
        """
        self.vgg = vgg
        self.coarse_sediment = coarse_sediment
        self.coarse_thickness = coarse_thickness
        self.delta_rhos = delta_rhos
        self.delta_rho_initial = delta_rho_initial
        self.reference_depths = reference_depths
        self.longrkm, self.longckm = longrkm, longckm
        self.wh, self.alpha = wh, alpha
        self.age = age

    @abstractmethod
    def downward(self, t):
        """
        calculate the density interface of interest with downward iteration steps
        :param t: iteration for downwards
        :return: matrix for undulation of density interface of interest
        """
        pass

    @classmethod
    def tvkey(cls, matrix, edge=0.02):
        """
        tukey the border values for smoothness with outside values 0
        :param matrix: matrix for tukey
        :param edge: float for definition of border
        :return: tukey matrix
        """
        nrow, ncol = matrix.shape
        tky = np.array([row_tky * col_tky for row_tky in tukey(nrow, edge)
                        for col_tky in tukey(ncol, edge)]).reshape(matrix.shape)
        return tky * matrix


class MultiInverse(VggToInterface):
    def __init__(self, vgg, coarse_sediment, coarse_thickness, delta_rhos, delta_rho_initial,
                 reference_depths, longrkm, longckm, wh, alpha, age):
        super(MultiInverse, self).__init__(vgg, coarse_sediment, coarse_thickness, delta_rhos,
                                           delta_rho_initial, reference_depths, longrkm, longckm,
                                           wh, alpha, age)
        # coarse_sediment, coarse_thickness
        # crust_provider.format_layer(target_size=self.vgg.shape, layer_number=1, order=1)
        # self.coarse_thickness = self.coarse_sediment - crust_provider.format_layer(self.vgg.shape, 5, order=1)
        # initialize frequency and filter
        self.delta_bnds = {0: np.zeros(self.vgg.shape), 1: np.zeros(self.vgg.shape)}
        self.frequency = self.__frequency__()
        self.filter = self.__filter__()

        self.G = 6.67
        # record the residual gravity fft
        self.residual_gravity_fft = 0j

    def __frequency__(self):
        """
        inner function for calculating the frequency
        :return: frequency matrix
        """
        nrow, ncol = self.vgg.shape
        frequency = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                ii = i if i <= nrow / 2 else i - nrow
                jj = j if j <= ncol / 2 else j - ncol
                frequency[i, j] = 2 * np.pi * np.sqrt((ii / self.longrkm) ** 2 +(jj / self.longckm) ** 2)
        return frequency

    def __filter__(self):
        """
        inner function for calculating the filter that lowpass the frequency value
        :return: a filter matrix
        """
        nrow, ncol = self.vgg.shape
        filter = np.ones(self.vgg.shape)
        for i in range(nrow):
            for j in range(ncol):
                if self.frequency[i, j] > self.wh:
                    ratio = self.frequency[i, j] / self.wh
                    filter[i, j] = ratio ** (1 - self.alpha) - (1 - self.alpha) * np.log(ratio) * ratio ** (1 - self.alpha)
        return filter

    def __initialize__interface__(self):
        """
        initialize the target density interface with only the vertical gravity gradient data
        :return: matrix for interface
        """
        qg_target = 2 * np.pi * self.G * self.delta_rho_initial * np.exp(-self.frequency *
                                                                         self.reference_depths.get(0))
        # vgg tukey
        vgg_tukey = self.tvkey(self.vgg)
        # vgg fft
        vgg_fft = fft2(vgg_tukey)
        # initialize the residual gravity fft
        self.residual_gravity_fft = vgg_fft
        # vgg_filter
        vgg_filter = vgg_fft * self.filter
        # interface_fft
        interface_fft = vgg_filter / qg_target
        # set the constant term been zero
        interface_fft[0, 0] = 0 + 0j
        # inverse interface
        interface = ifft2(interface_fft).real - self.reference_depths.get(0)
        # form the sedimentary layer
        sedimentary = Sediment.form_sediment(topography=interface, coarse_sediment=self.coarse_sediment,
                                             coarse_thickness=self.coarse_thickness, age=self.age)
        self.delta_bnds[0] = interface + self.reference_depths.get(0)
        self.delta_bnds[1] = sedimentary + self.reference_depths.get(1)
        return self.delta_bnds[1] - self.reference_depths.get(1)

    def __residual__gravity__(self, t):
        """
        summary the 1 to t-th order of gravity by the non-targeted interfaces
        summary the 2 to t-th order of gravity by the target interface
        :param t: int upper bound for iterations
        :return: residual gravity fft complex matrix
        """
        gravity_fft_keys = {}
        for key, matrix in self.delta_bnds.items():
            # calculate the ratio factor
            gq_key = 2 * np.pi * self.G * self.delta_rhos[key] * np.exp(-self.frequency * self.reference_depths[key])
            # non-target layer
            if key != 0:
                # for order t firstly tukey the interface
                matrix_tukey = self.tvkey(matrix)
                # calculate the fft
                if t == 1:
                    gravity_fft_keys[key] = fft2(matrix_tukey ** t)
                else:
                    gravity_fft_keys[key] = fft2(matrix_tukey ** t) * self.frequency ** (t - 1) / factorial(t)
            # target layer
            else:
                # from order 2 to t
                if t == 1:
                    gravity_fft_keys[key] = 0j
                else:
                    # tukey the interface
                    matrix_tukey = self.tvkey(matrix)
                    # calculate the fft
                    gravity_fft_keys[key] = fft2(matrix_tukey ** t) * self.frequency ** (t - 1) / factorial(t)
            # multiply the ratio factor
            gravity_fft_keys[key] = gravity_fft_keys.get(key) * gq_key
        # calculate the residual gravity
        for key, value in gravity_fft_keys.items():
            self.residual_gravity_fft -= value
        return self.residual_gravity_fft

    def downward(self, t):
        """
        inverse gravity for interface of interest
        :param t:
            :parameter 0: only vgg data are used with no iteration
            :parameter i: the i-th step for downward continuation
        :return: a matrix
        """
        # calculate the initialized interface
        initial_interface = self.__initialize__interface__()
        # if t == 0 means only initial interface is needed
        if t == 0:
            return initial_interface
        # if t >= 1
        qg_target = 2 * np.pi * self.G * self.delta_rhos[0] * np.exp(
                                                            -self.frequency * self.reference_depths[0])
        for it in range(1, t + 1):
            # calculate and update the residual gravity fft
            residual_gravity = self.__residual__gravity__(it)
            # interface fft
            interface_target_fft = residual_gravity / qg_target
            # filter the interface fft
            interface_target_fft_filter = interface_target_fft * self.filter
            # set the constant term zero
            interface_target_fft_filter[0, 0] = 0 + 0j
            # interface
            interface_target = ifft2(interface_target_fft_filter).real - self.reference_depths[0]
            # update the target interface
            self.delta_bnds[0] = interface_target + self.reference_depths[0]
            # calculate the sedimentary layer
            sedimentary_layer = Sediment.form_sediment(topography=interface_target,
                                                       coarse_sediment=self.coarse_sediment,
                                                       coarse_thickness=self.coarse_thickness, age=self.age)
            # update the sedimentary layer
            self.delta_bnds[1] = sedimentary_layer + self.reference_depths[1]
        # return the target interface
        return self.delta_bnds[1] - self.reference_depths[1]


class Sediment:
    @classmethod
    def __old_sediment__(cls, topography, coarse_sediment):
        result_sediment = coarse_sediment.copy()
        result_sediment[topography - coarse_sediment > 0] = topography[topography - coarse_sediment > 0]
        return result_sediment

    @classmethod
    def __young_sediment__(cls, topography, coarse_thickness):
        result_sediment = topography + coarse_thickness
        return result_sediment

    @classmethod
    def form_sediment(cls, topography, coarse_sediment, coarse_thickness, age):
        old_sediment = cls.__old_sediment__(topography, coarse_sediment)
        young_sediment = cls.__young_sediment__(topography, coarse_thickness)
        return age * old_sediment + (1 - age) * young_sediment

