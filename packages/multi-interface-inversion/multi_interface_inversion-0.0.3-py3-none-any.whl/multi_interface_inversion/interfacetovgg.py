from abc import ABCMeta, abstractmethod
from scipy.fftpack import fft2, ifft2
import numpy as np
from math import factorial


class InterfaceToVggC(metaclass=ABCMeta):
    def __init__(self, delta_bnds, delta_rhos, reference_depths, longrkm, longckm):
        """
        initialize the inputs
        :param delta_bnds: a dict with keys: 0,1,2,…; values: matrix0, matrix1, …
                            for the undulation of the density interfaces
        :param delta_rhos: a dict with keys:0, 1, 2, …; values: float0, float1, …
                            for the density contrast of the density interfaces
        :param reference_depths: a dict with keys: 0, 1, 2, …; values: float0, float1,…
                                    positive float stands for the reference plane
        :param longrkm: distance from the upper bound latitude to the lower bound latitude
        :param longckm: distance from the left bound longitude to the right bound longitude
        """
        self.delta_bnds = delta_bnds
        self.delta_rhos = delta_rhos
        self.reference_depths = reference_depths
        self.longrkm, self.longckm = longrkm, longckm

    @abstractmethod
    def forward(self, t):
        """
        calculate the vgg from the inputs with iteration t
        :param t: iteration stands for the order of parker's formula
        :return: vgg matrix
        """
        pass


class MultiForward(InterfaceToVggC):
    def __init__(self, delta_bnds, delta_rhos, reference_depths, longrkm, longckm):
        super(MultiForward, self).__init__(delta_bnds, delta_rhos, reference_depths, longrkm, longckm)
        self.frequency = self.__frequency__()
        self.G = 6.67

    def __frequency__(self):
        """
        inner function for calculating the frequency
        :return: frequency matrix
        """
        nrow, ncol = self.delta_bnds.get(0).shape
        frequency = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                ii = i if i <= nrow / 2 else i - nrow
                jj = j if j <= ncol / 2 else j - ncol
                frequency[i, j] = 2 * np.pi * np.sqrt((ii / self.longrkm) ** 2 +(jj / self.longckm) ** 2)
        return frequency

    def forward(self, t):
        gravity_fft = None
        for key, matrix in self.delta_bnds.items():
            # gravity factor
            qg_key = -2 * np.pi * self.G * self.delta_rhos.get(key) * np.exp(-self.frequency * self.reference_depths.get(key))
            gravity_fft_k = None
            for it in range(1, t + 1):
                if gravity_fft_k is None:
                    gravity_fft_k = self.frequency ** (it - 1) * fft2(matrix ** it) / factorial(it)
                else:
                    gravity_fft_k += self.frequency ** (it - 1) * fft2(matrix ** it) / factorial(it)
            # summary all gravity caused by all matrix
            if gravity_fft is None:
                gravity_fft = gravity_fft_k * qg_key
            else:
                gravity_fft += gravity_fft_k * qg_key
        # inverse iff
        vgg = ifft2(gravity_fft).real
        return vgg


if __name__ == "__main__":
    x, y = np.linspace(0, 4 * np.pi, 20), np.linspace(0, 3 * np.pi, 30)
    xx, yy = np.meshgrid(x, y)
    zz = np.sin(xx + yy)
    parameters = {
        "delta_bnds": {0: zz},
        "delta_rhos": {0: 1.82},
        "reference_depths": {0: 5},
        "longrkm": 500,
        "longckm": 600,
    }
    cho = MultiForward(**parameters)
    vgg = cho.forward(t=3)

