import math
import datetime
import csv
from Astro.calculations import *
from Astro.preprocessor import *

# conversion factors
earth_radius_km = 6371
earth_radius_miles = 3958.756
deg = math.pi/180.0

# rotation of the earth rate
wE = .00089 # rad/second
omega = [0,0,wE]

def site(lat, alt, time):
    print("Site")
    position = (0,0)
    velocity = (0,0)
    return position, velocity

def track(rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, days, lst_time, elevation_sea_level):
    
    r_SEZ, v_SEZ = compute_position_and_velocity_vectors_topocentric(rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate)

    r_IJK, v_IJK = compute_r_v_geocentric(r_SEZ, v_SEZ, latitude, lst_time, elevation_sea_level)
    
    print(r_IJK, v_IJK)
    return r_IJK, v_IJK


if __name__ == '__main__':
    # data fields
    with open('Astro/data.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        total = 0
        for row in reader:
            if total == 0:
                total += 1
            else: 
                latitude, longitude, elevation_sea_level, UT, date, p, p_dot, el, el_dot, az, az_dot = row
                latitude, longitude, elevation_sea_level_canonical, days, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, lst_time = process_input_data(latitude, longitude, elevation_sea_level, UT, date, p, p_dot, el, el_dot, az, az_dot)
                r, v = track(rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, days, lst_time, elevation_sea_level_canonical)
                total += 1


# if __name__ == "__main__":
#     print("Welcome to your radar observation home\n \
#         You have a single radar observation with Doppler capabilities? Great!\n")
#     more_data = True
#     while (more_data):
        
#         if input("Use test data? y/n") == 'y':
#             lat, long, elevation_sea_level, UT, date, rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate, time = process_input_data("39.007N", "104.883W", "7180f", 2210.575, "02.09.1971", "504.68k", 2.08, 56.2, 2.1, 30.6, 1.1)
#             track(rho, rho_dot, elevation, elevation_rate, azimuth, azimuth_rate)
#             break

#         print("Please input lat/long followed immediately by N,S,E,W like so 39.007N, 104.883W")
#         latitude_site = input("Latitude: ")
#         longitude_site = input("Longitude: ")
#         print("Please input your site elevation above sea level, followed by the units, m for meters or f for ft like so, 7180f")
#         elevation_sea_level = input("Elevation: ")
#         print("Please input the Universal Time of the observation in decimal form - 22:10:57.5 = 2210.575 for example")
#         UT = input("Universal Time: ")
#         print("Please input the date of the observation in full standard day, month, year format, separated by '.' 02.09.1970")
#         date = input("Date: ")
#         print("Now for the satelite's data...\nPlease input p, followed by units. k for km, m for miles like such 504.68k")
#         rho = input("p: ")
#         p_dot = input("p_dot: ")
#         elevation = input("Elevation in degrees: ")
#         elevation_dot = input("Elevation Rate in deg/sec: ")
#         azimuth = input("Azimuth in degrees: ")
#         azimuth_dot = input("Azimuth Rate in deg/sec: ")
        
        
    
#         process_input_data(latitude_site, longitude_site, elevation_sea_level, UT, date, rho, p_dot, elevation, elevation_dot, azimuth, azimuth_dot)
        
#         if input("Calculate multiple observations?: y/n: ") == 'n':
#             more_data = False