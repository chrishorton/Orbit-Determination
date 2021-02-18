import math
import datetime
from numpy import array, dot, reshape, cross
from math import pi as pi

# conversion factors
earth_radius_km = 6371
earth_radius_miles = 3958.756
equatorial_radius = 6378.145 # km
polar_radius = 6356.785 # km
eccentricity = 0.08182
L = 0
H = 6.378 / 6371.0

omega = 15 #degrees/hour
wE = .0588336565 # rad/hour
omega_wE = array([0,0,wE])

round_off_factor = 5


# rotation of the earth rate

def compute_station_coords_ellipsoid(lst_time, lat, elevation_sea_level):
    x = abs(1 / ( math.sqrt(1 - math.pow(eccentricity,2) * math.sin(lat))) + elevation_sea_level) * math.cos(lat)
    z = abs(1 / ( math.sqrt(1 - math.pow(eccentricity,2) * math.sin(lat))) + elevation_sea_level) * math.sin(lat)
    R = array([ x * math.cos(lst_time), x * math.sin(lst_time), z])
    return R

def calculate_position_and_velocity_vectors_topocentric(range, range_rate, elevation, elevation_rate, azimuth, azimuth_rate):

    rho_S = -1 * range * math.cos(elevation) * math.cos(azimuth)
    rho_E = range * math.cos(elevation) * math.sin(azimuth)
    rho_Z = range * math.sin(elevation)

    rho = array([rho_S, rho_E, rho_Z])
    # print (round(rho_S, round_off_factor), round(rho_E, round_off_factor), round(rho_Z, round_off_factor))

    rho_dot_S = -1 * range_rate * math.cos(elevation) * math.cos(azimuth) + range * math.sin(elevation) * elevation_rate * math.cos(azimuth) + range * math.cos(elevation) * math.sin(azimuth) * azimuth_rate
    rho_dot_E = range_rate * math.cos(elevation) * math.sin(azimuth) - range * math.sin(elevation) * elevation_rate * math.sin(azimuth) + range * math.cos(elevation) * math.cos(azimuth) * azimuth_rate
    rho_dot_Z = range_rate * math.sin(elevation) + range * math.cos(elevation) * elevation_rate
    
    rho_dot = array([rho_dot_S, rho_dot_E, rho_dot_Z])
    # print (round(rho_dot_S, round_off_factor), round(rho_dot_E, round_off_factor), round(rho_dot_Z, round_off_factor))

    return rho, rho_dot

# TODO: note - would it just be easier to bring these 2 functions together?
# and definitely make it into OOP and some class variables/methods

def compute_r_v_geocentric(r_topo, v_topo, lat, lst_time, elevation_sea_level):

    # account for eccentricity of the earth, more accurate
    R = compute_station_coords_ellipsoid(lst_time, lat, elevation_sea_level) 
    r_topo += R

    # for some reason the book doesn't account for eccentricity, so assuming that the earths radius is 1 DU all the way around, simply add 1 to the Z distance vector
    # r_topo += [0,0,1]
    
    rotation_matrix = array([
        [math.sin(lat) * math.cos(lst_time), -1 * math.sin(lst_time), math.cos(lat) * math.cos(lst_time)],
        [math.sin(lat) * math.sin(lst_time), math.cos(lst_time), math.cos(lat) * math.sin(lst_time)],
        [-1 * math.cos(lat), 0, math.sin(lat)]
    ])

    rho_3_vector = array(r_topo)
    rho_dot_3_vector = array(v_topo)

    r = dot(rotation_matrix, rho_3_vector)
    rho_dot = dot(rotation_matrix, rho_dot_3_vector)

    v = rho_dot + cross(omega_wE, r)
    return r, v


class Math(object):
    """
    docstring
    """
    def __init__(self):
        pass

    def get_magnitude(self, vector):
        sum = 0
        for i in vector:
            sum += i ** 2
        return math.sqrt(sum)