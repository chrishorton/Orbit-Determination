from numpy import radians
from scipy.constants import kilo
import matplotlib.pyplot as plt

from orbital import earth, KeplerianElements, Maneuver, plot, plot3d, elements_from_state_vector

km_radius = 6371

def plot_with_elements(a, e, i, raan, arg_pe):
    a *= km_radius
    a += km_radius
    e = 1 - e
    
    orbit = KeplerianElements(a=a, e=e, i=i, raan=raan, arg_pe=arg_pe, body=earth)
    plot_ = plot3d(orbit, animate=False)
    plt.show()

# i = 0.790488069356154
# raan = 2.841424499708282
# arg_pe = 0.9925161413607387
# nu = 3.0898420708516094

# orbit_ = KeplerianElements.with_elements(a, e, i, raan, arg_pe, body=earth)
# plot_ = plot(orbit_)
# plt.show()