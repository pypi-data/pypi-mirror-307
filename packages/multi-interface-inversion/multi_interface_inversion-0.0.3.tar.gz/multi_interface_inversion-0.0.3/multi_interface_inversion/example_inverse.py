from multi_interface_inversion import CrustModel, Vgg, longrc
from multi_interface_inversion import MultiInverse
from multi_interface_inversion import Ploter as Plr


# example of inverse
kwargs = {'lat_up': 30, 'lat_down': 26, 'lon_left': 151, 'lon_right': 155}

# vgg, coarse_sediment, coarse_thickness, delta_rhos, delta_rho_initial,
#                  reference_depths, longrkm, longckm, wh, alpha, age
crust10 = CrustModel(kwargs)
vgg2023 = Vgg(kwargs).vgg()
parameters = {
    'vgg': vgg2023,
    'coarse_sediment': crust10.format_layer(target_size=vgg2023.shape, layer_number=1, order=3),
    'coarse_thickness': crust10.format_layer(target_size=vgg2023.shape,
                                             layer_number=1, order=3) - crust10.format_layer(
                                                target_size=vgg2023.shape, layer_number=5, order=3),
    'delta_rhos': {0: 0.7, 1: 0.8},
    'delta_rho_initial': 2.05,
    'reference_depths': {0: 5.7628, 1: 5.8460},
    'longrkm': longrc(lat=28, lon=153, width=4)[0],
    'longckm': longrc(lat=28, lon=153, width=4)[1],
    'wh': 0.18,
    'alpha': 8,
    'age': 0.5,
}

mii = MultiInverse(**parameters)
result = mii.downward(t=8)
Plr.plt_3d(result)
