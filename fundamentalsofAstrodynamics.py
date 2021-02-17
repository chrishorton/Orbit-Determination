#############################################################################
#   
#   
#   
#   
#   
#   
#   
#
#   
#   
#   
#   
#
#   
#   
#   
#############################################################################


import math
import datetime

# conversion factors
earth_radius_km = 6371
earth_radius_miles = 3958.756
deg = math.pi/180.0

# rotation of the earth rate
wE = .00089 # rad/second
omega = [0,0,wE]

# unit direction vectors as basis for topocentric horizon coordinate system
x = [0,0,1]
y = [0,1,0]
z = [1,0,0]

def site(lat, alt, time):
    print("Site")
    position = (0,0)
    velocity = (0,0)
    return position, velocity

def track(range, range_rate, elevation, elevation_rate, azimuth, azimuth_rate):
    print("Tracking...")

    # Here is our position vector, topocentrically. 
    rho_S = -range * math.cos(elevation) * math.cos(azimuth)
    rho_E = range * math.cos(elevation) * math.sin(azimuth)
    rho_Z = range * math.sin(elevation)

    print("rho = " + str(rho_S) + "S +" + str(rho_E) + "E +" + str(rho_Z) + "Z")

    rho_dot_S = - range_rate * math.cos(elevation) * math.cos(azimuth) + range * math.sin(elevation) * elevation_rate * math.cos(azimuth) + range * math.cos(elevation) * math.sin(azimuth) * azimuth_rate
    rho_dot_E = range_rate * math.cos(elevation) * math.sin(azimuth) - range * math.sin(elevation) * elevation_rate * math.sin(azimuth) + range * math.cos(elevation) * math.cos(azimuth) * azimuth_rate
    rho_dot_Z = - range_rate * math.sin(elevation) + range * math.cos(elevation) * elevation_rate
    
    rho = rho_S + rho_E + rho_Z
    rho_dot = rho_dot_S + rho_dot_E + rho_dot_Z

    print("rho_dot = " + str(rho_dot_S) + "S +" + str(rho_dot_E) + "E +" + str(rho_dot_Z) + "Z")
    print("r = " + (str(rho_dot_S) + "S, " + str(rho_dot_E) + "E, " + str(rho_dot_Z) + "Z"))  
    radius = (0,0, 0)
    velocity = (0, 0, 0)

    return radius, velocity

def process_input_data(lat, long, elevation_sea_level, UT, date, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate):
    # TODO much better error handling
    if lat[-1:] == 'n' or lat[-1:] == "N":
        lat = float(lat[:-1])
    elif lat[-1:] == 's' or lat[-1:] == "S":
        lat = -float(lat[:-1])
    else:
        print("There was an error computing site latitude.")

    if long[-1:] == 'e' or long[-1:] == "E":
        long = float(long[:-1])
    elif long[-1:] == 'w' or long[-1:] == "W":
        long = -float(long[:-1])
    else:
        print("There was an error computing site longitude.")

    if elevation_sea_level[-1:] == 'm':
        print("meters")
    elif elevation_sea_level[-1:] == 'f':
        print("feet")
    else:
        print("There was an error computing site elevation.")

    #process date and time, date should be in 09.02.1970 format
    days = compute_days_from_1970(date)

    time = compute_sidereal_time(long, days, UT)

    # need to make sure we have correct canonical units in earths reference frame.
    if rho[-1:].lower() == "k":
        rho = to_canonical_km(float(rho[:-1]), 'earth')
    elif rho[-1:].lower() == "m":
        rho = to_canonical_miles(float(rho[:-1]), 'earth')
    else:
        print("There was an error computing rho (p).")

    vars_to_int = [rho_dot, elevation, elevation_rate, azimuth, azimuth_rate]
    # cast all the rest deg and deg/sec as integers.
    map(float, vars_to_int)

    

    print("Data Entered: " + str((lat, long, elevation_sea_level, UT, date, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, time)))
    return lat, long, elevation_sea_level, UT, date, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, time
        

if __name__ == "__main__":
    print("Welcome to your radar observation home\n \
        You have a single radar observation with Doppler capabilities? Great!\n")
    more_data = True
    while (more_data):
        
        if input("Use test data? y/n") == 'y':
            lat, long, elevation_sea_level, UT, date, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, time = process_input_data("39.007N", "104.883W", "7180f", 2210.575, "02.09.1971", "504.68k", 2.08, 56.2, 2.1, 30.6, 1.1)
            track(rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate)
            break

        print("Please input lat/long followed immediately by N,S,E,W like so 39.007N, 104.883W")
        latitude_site = input("Latitude: ")
        longitude_site = input("Longitude: ")
        print("Please input your site elevation above sea level, followed by the units, m for meters or f for ft like so, 7180f")
        elevation_sea_level = input("Elevation: ")
        print("Please input the Universal Time of the observation in decimal form - 22:10:57.5 = 2210.575 for example")
        UT = input("Universal Time: ")
        print("Please input the date of the observation in full standard day, month, year format, separated by '.' 02.09.1970")
        date = input("Date: ")
        print("Now for the satelite's data...\nPlease input p, followed by units. k for km, m for miles like such 504.68k")
        rho = input("p: ")
        p_dot = input("p_dot: ")
        elevation = input("Elevation in degrees: ")
        elevation_dot = input("Elevation Rate in deg/sec: ")
        azimuth = input("Azimuth in degrees: ")
        azimuth_dot = input("Azimuth Rate in deg/sec: ")
        
        
    
        process_input_data(latitude_site, longitude_site, elevation_sea_level, UT, date, rho, p_dot, elevation, elevation_dot, azimuth, azimuth_dot)
        
        if input("Calculate multiple observations?: y/n: ") == 'n':
            more_data = False