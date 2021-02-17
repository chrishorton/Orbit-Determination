# from Fundamentals_of_Astro.Astro.fundamental_helpers import *
import math
import datetime
from numpy import array, dot, reshape, cross
from math import pi


# conversion factors
earth_radius_km = 6378.145 # DU
earth_radius_miles = 3963.195563
TU = 806.8118744 # seconds

DU_TU = 7.90536828

deg = pi/180.0

equatorial_radius = 6378.145 # km (earth)
polar_radius = 6356.785 # km (earth)
eccentricity = 0.08182 # (earth)
gst_0 = 1.74933340

wE = .0588336565 # rad/hour

degree_sec_to_rad_TU = 14.08152366
km_sec_to_du_tu = 0.12649632054



# rotation of the earth rate

def normalize_site_elevation(elevation_sea_level):
    """Calculates the site elevation from the center of the earth.
        Args:
            elevation_sea_level: elevation of the observation site, followed by unit indicator, f or m
        Returns:
            true_elevation_miles: miles from the center of the earth
            true_elevation_km: km from the center of the earth
    """
        
    elevation_units = elevation_sea_level[-1:].lower()
    elevation_sea_level = float(elevation_sea_level[:-1])

    if elevation_units == 'm':
        normalized_elevation_km = elevation_sea_level/1000.0 # km above sea level
        normalized_elevation_km /= earth_radius_km
        # true_elevation_km = normalized_elevation_km + earth_radius_km # km from geocenter
        return normalized_elevation_km
    elif elevation_units == 'f':
        normalized_elevation_miles = elevation_sea_level/5280.0
        normalized_elevation_miles /= earth_radius_miles
        # true_elevation_miles = normalized_elevation_miles + earth_radius_miles
        return normalized_elevation_miles
    else:
        print("There was an error computing site elevation.")
        return 0

def to_canonical_km(km, reference_orbit):
    # DU (distance unit) is radius of the reference orbit. The reference orbit will be a minimum altitude circular orbit just grazing the surface of the planet
    # Define our TU (time unit) such that the speed of a satelite in the reference orbit is 1 DU/TU then gravitational parameter mu = 1 DU^3/TU^3
    if reference_orbit == "earth":
        return km / earth_radius_km

def to_canonical_miles(miles, reference_orbit):
    if reference_orbit == "earth":
        return miles / earth_radius_miles

def compute_days_from_1970(date):
    day, month, year = map(int, date.split('.'))
    assert year >= 1970, "Observation year must be after 1970"
    days = (datetime.datetime(year,month,day) - datetime.datetime(1970,1,1)).days
    return days
 
def compute_lst(longitude, day, universal_time):
    d = day + (universal_time / 100.0) / 24 + (math.floor(universal_time) % 100) / 1440 + (universal_time - math.floor(universal_time)) / 864
    lst = longitude + gst_0 + 1.0027379093 * 2 * pi * d
    lst %= 2 * pi
    return lst


def process_input_data(latitude, longitude, elevation_sea_level, UT, date, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate):

    rho_dot = float(rho_dot)
    azimuth = float(azimuth)
    azimuth_rate = float(azimuth_rate)
    elevation = float(elevation)
    elevation_rate = float(elevation_rate)
    UT = float(UT)

    # TODO much better error handling
    if latitude[-1:] == 'n' or latitude[-1:] == "N":
        latitude = float(latitude[:-1])
    elif latitude[-1:] == 's' or latitude[-1:] == "S":
        latitude = -1 * float(latitude[:-1])
    else:
        latitude = 0
        print("There was an error computing site latitude.")

    if longitude[-1:] == 'e' or longitude[-1:] == "E":
        longitude = float(longitude[:-1])
    elif longitude[-1:] == 'w' or longitude[-1:] == "W":
        longitude = -1 * float(longitude[:-1])
    else:
        longitude = 0
        print("There was an error computing site longitude.")

    # need to make sure we have correct canonical earth units.
    if rho[-1:].lower() == "k":
        rho = to_canonical_km(float(rho[:-1]), 'earth')
        # rho_dot = to_canonical_km(rho_dot, 'earth')
    elif rho[-1:].lower() == "m":
        rho = to_canonical_miles(float(rho[:-1]), 'earth')
        # rho_dot = to_canonical_miles(rho_dot, 'earth')
    else:
        print("There was an error computing rho and rho_dot.")

    # convert from degrees to radians and to canonical units
    
    elevation *= deg
    azimuth *= deg
    latitude *= deg
    longitude *= deg

    # convert to radians per TU
    elevation_rate *= degree_sec_to_rad_TU
    azimuth_rate *= degree_sec_to_rad_TU
    rho_dot *= km_sec_to_du_tu # change from km/ sec to DU/TU canonical units

    elevation_sea_level_canonical = normalize_site_elevation(elevation_sea_level)

    #process date and time, date should be in dd/mm/yyyy format
    days = compute_days_from_1970(date)
    lst_time = compute_lst(longitude, days, UT)

    return latitude, longitude, elevation_sea_level_canonical, days, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, lst_time



# I don't know what this exactly does
# def compute_gst(ut, longitude):
#     lst = gst * omega_radians + longitude
#     print("Local sidereal time: " + str(lst))
#     return lst