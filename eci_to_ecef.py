# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
# This script converts Earth-Centered Inertial (ECI) coordinates to Earth-Centered Earth-Fixed (ECEF) coordinates.
#
# Parameters:
# year: Year of the date (integer)
# month: Month of the date (integer, 1 to 12)
# day: Day of the month (integer)
# hour: Hour of the day (integer, 0 to 23)
# minute: Minute of the hour (integer, 0 to 59)
# second: Seconds of the minute (float, can have a decimal portion)
# eci_x_km: X-coordinate of the ECI position in kilometers (float)
# eci_y_km: Y-coordinate of the ECI position in kilometers (float)
# eci_z_km: Z-coordinate of the ECI position in kilometers (float)
#
# Output:
# Prints the corresponding ECEF coordinates in kilometers.
#
# Written by: Jeren Browder
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

import sys  # for argument parsing
import math  # for trigonometric functions
from datetime import datetime, timedelta

# Helper function: Calculate Julian date from date and time
def ymdhms_to_julian_date(year, month, day, hour, minute, second):
    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + A // 4

    jd_int = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    frac_day = (hour + minute / 60.0 + second / 3600.0) / 24.0

    return jd_int + frac_day

# Helper function: Calculate the Greenwich Sidereal Time (GST) in radians
def gst_from_julian_date(julian_date):
    JD2000 = 2451545.0  # Julian date for January 1, 2000, 12:00 UT
    T = (julian_date - JD2000) / 36525.0  # Julian centuries since J2000.0

    # Calculate Greenwich Sidereal Time at 0h UT (in seconds)
    GST_sec = (280.46061837 + 360.98564736629 * (julian_date - JD2000) + \
               T * T * (0.000387933 - T / 38710000)) * 3600

    # Convert GST to hours, then to radians
    GST_hours = (GST_sec / 3600) % 24
    GST_rad = math.radians(GST_hours * 15) - 1.02581572

    return GST_rad
    
# Helper function: Convert ECI to ECEF
def eci_to_ecef(eci_x_km, eci_y_km, eci_z_km, gst_rad):
    """
    Convert ECI coordinates to ECEF using the Greenwich Sidereal Time (GST).
    
    Args:
        eci_x_km (float): X-coordinate in the ECI frame (kilometers).
        eci_y_km (float): Y-coordinate in the ECI frame (kilometers).
        eci_z_km (float): Z-coordinate in the ECI frame (kilometers).
        gst_rad (float): Greenwich Sidereal Time in radians.
        
    Returns:
        tuple: ECEF coordinates (x, y, z) in kilometers.
    """
    # Apply rotation matrix for ECI to ECEF
 
    ecef_x_km = ((math.cos(gst_rad)) * eci_x_km) + ((math.sin(gst_rad)) * eci_y_km)
    ecef_y_km = ((-math.sin(gst_rad)) * eci_x_km) + ((math.cos(gst_rad)) * eci_y_km)
    ecef_z_km = eci_z_km

    return ecef_x_km, ecef_y_km, ecef_z_km

# Main function
def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 10:
        print("Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km")
        sys.exit(1)

    # Parse the input arguments
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])

    # Convert the given date and time to Julian Date
    jd = ymdhms_to_julian_date(year, month, day, hour, minute, second)

    # Calculate the Greenwich Sidereal Time (GST) in radians
    gst_rad = gst_from_julian_date(jd)

    # Convert ECI coordinates to ECEF
    ecef_x_km, ecef_y_km, ecef_z_km = eci_to_ecef(eci_x_km, eci_y_km, eci_z_km, gst_rad)

    # Print the resulting ECEF coordinates
    print(ecef_x_km)
    print(ecef_y_km)
    print(ecef_z_km)
    
if __name__ == "__main__":
    main()