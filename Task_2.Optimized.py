
"""
'''
Created on Tue Nov  6 14:33:47 2018
@author: Bhuiyan_Rony

Features:
    1. Distance
    2. Total Steps
    3. Total Jumps
    
Github link: https://github.com/BalayetRony/task-2 
'''
"""
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.signal import find_peaks
#from scipy import integrate
#from mpl_toolkits import mplot3d


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    A = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    C = 2 * asin(sqrt(A))
    R = 6371000 # Radius of earth in meters. Use 3956 for miles
    return C * R



DATA_SENSOR = pd.read_csv('Sensor_record_20181112_174950_AndroSensor.csv')

ACC_X = DATA_SENSOR['ACCELEROMETER X (m/s²)']
ACC_Y = DATA_SENSOR['ACCELEROMETER Y (m/s²)']
ACC_Z = DATA_SENSOR['ACCELEROMETER Z (m/s²)']
LATITUDE = DATA_SENSOR['LOCATION Latitude : ']
LONGITUDE = DATA_SENSOR['LOCATION Longitude : ']
#TIME = DATA_SENSOR['Time since start in ms ']


DATA_SENSOR['ACC_RMS'] = np.sqrt(ACC_X **2 + ACC_Y ** 2 + ACC_Z **2)
plt.figure(figsize=(10, 10))
plt.grid()
plt.plot(DATA_SENSOR.index, DATA_SENSOR['ACC_RMS'])
plt.title('ACC_RMS')
plt.show()


DISTANCES = []
COUNT = 0
while True:
    if COUNT < len(LATITUDE)-1:
        DISTANCES.append(haversine(LONGITUDE[COUNT], LATITUDE[COUNT], \
                                   LONGITUDE[COUNT+1], LATITUDE[COUNT+1]))
        COUNT = COUNT + 1
    else:
        break

print("The actual distance is: ", sum(DISTANCES), "m")

ACC_RMS = DATA_SENSOR['ACC_RMS']
FILTERED_DATA = (ACC_RMS- ACC_RMS.mean())
POS = FILTERED_DATA[FILTERED_DATA > 13]
print("Number of Jumps: ", len(POS))

POS = FILTERED_DATA[FILTERED_DATA > 2.8]
NEG = FILTERED_DATA[FILTERED_DATA < -2.8]
print("Number of Steps: ", len(POS) + len(NEG))
