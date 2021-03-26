import time
import numpy as np
from app.dbManager import *
from .sps30_driver import sps30


device_port = "/dev/ttyUSB0"
startup_time = 8
samples_per_measurement = 30
results = []
dates = []
timestamps = []


try:
    # INIT SENSOR CLASS AND ESTABLISHING PORT CONNECTION.
    sensor_sps30 = sps30.Sps30(device_port)

    # STARTING UP SPS30 SENSOR. GOING FROM IDLE MODE TO MEASUREMENT MODE
    sensor_sps30.start_measurement(start_up_time=startup_time)

    # PERFORMING MEASUREMENTS
    for i in range(samples_per_measurement):
        dates.append(time.strftime('%Y-%m-%d'))
        timestamps.append(time.strftime('%H:%M:%S'))
        results.append(sensor_sps30.read_measured_values())
        time.sleep(1)

    # TURNING OFF MEASUREMENT MODE. RETURNING TO IDLE MODE.
    sensor_sps30.stop_measurement()

    # CLOSE PORT CONNECTION.
    sensor_sps30.close_port()

    # DATA AGGREGATION
    np_data = np.array(results)
    aggr_data = np_data.mean(axis=0)

    # ADD DATA SAVING
    add_entry(dates[-1], timestamps[-1], aggr_data[0], aggr_data[1], aggr_data[2], aggr_data[3], aggr_data[4],
              aggr_data[5], aggr_data[6], aggr_data[7], aggr_data[8], aggr_data[9])
except NotImplemented:
    exit()



