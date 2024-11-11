from multi_interface_inversion import CrustModel, Vgg, Ploter, longrc
from multi_interface_inversion import MultiForward


# example of forward
kwargs = {'lat_up': 30, 'lat_down': 26, 'lon_left': 151, 'lon_right': 155}

crust10 = CrustModel(kwargs)
longrkm, longckm = longrc(lat=28, lon=153, width=4)

parameters = {
    "delta_bnds": {0: crust10.format_layer((241, 241), 5) + 5.8472,
                   1: crust10.format_layer((241, 241), 1) + 5.7634},
    "delta_rhos": {0: 1.2, 1: 0.8},
    "reference_depths": {0: 5.8472, 1: 5.7633},
    "longrkm": longrkm,
    "longckm": longrkm,
}

multi_forward = MultiForward(**parameters)
vgg = multi_forward.forward(t=5)
