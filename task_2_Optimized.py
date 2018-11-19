# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:35:28 2018
@author: mdb99
Features:
    1. Distance
    2. Total Steps
    3. Total Jumps
"""

from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


def peak_counter(lower_bound, upper_bound, column, threshold):
    ''' Calculate peak points within given range and threshold.
        Works as sliding window function to select the range.
        In:
            lower_bound: integer lower limit in range
            upper_bound: integer upper bound in limit
            column: string value for column
            threshold: integer value to eliminate lower values
        Return:
            Number of peaks in given range
    '''
    filtered_data = DATA_FIELD[column].iloc[lower_bound:upper_bound]
    peak, _ = find_peaks(filtered_data, height=threshold)
    num_peak = len(peak)
    return num_peak


DATA_FIELD = pd.read_csv('Sensor_record_20181112_174950_AndroSensor.csv')

ACC_X = DATA_FIELD['ACCELEROMETER X (m/s²)']
ACC_Y = DATA_FIELD['ACCELEROMETER Y (m/s²)']
ACC_Z = DATA_FIELD['ACCELEROMETER Z (m/s²)']
#LATITUDE = data_field1['LOCATION Latitude : ']
#LONGITUDE = data_field1['LOCATION Longitude : ']
TIME = DATA_FIELD['Time since start in ms ']


DATA_FIELD['ACC_RMS'] = np.sqrt(ACC_X **2 + ACC_Y ** 2 + ACC_Z **2)
plt.figure(figsize=(10, 10))
plt.grid()
plt.plot(DATA_FIELD.index, DATA_FIELD['ACC_RMS'])
plt.title('ACC_RMS')
plt.show()

STEP1 = peak_counter(0, 70, 'ACC_RMS', 0)
STEP2 = peak_counter(75, 200, 'ACC_RMS', 0)
STEP3 = peak_counter(220, 275, 'ACC_RMS', 0)

TOTAL_STEPS = STEP1+STEP2+STEP3
print("Number of total STEPSs taken :::", TOTAL_STEPS)

JUMP1 = peak_counter(60, 80, 'ACC_RMS', 10)
JUMP2 = peak_counter(200, 230, 'ACC_RMS', 10)

TOTAL_JUMPS = JUMP1+JUMP2
print("Number of total JUMPs taken :::", TOTAL_JUMPS)


R = 6373000.0

LAT1 = radians(48.1635)
LON1 = radians(11.558943)
LAT2 = radians(48.16329)
LON2 = radians(11.557148)

DLON = LON2 - LON1
DLAT = LAT2 - LAT1

A = sin(DLAT / 2)**2 + cos(LAT1) * cos(LAT2) * sin(DLON / 2)**2
C = 2 * atan2(sqrt(A), sqrt(1 - A))

DISTANCE = R * C

print("Distance Covered::", DISTANCE, 'm')
