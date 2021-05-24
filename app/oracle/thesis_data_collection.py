#!/home/pi/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
import time
import numpy as np
import pandas as pd
from sps30_driver import sps30


device_port = "/dev/ttyUSB0"
startup_time = 8
samples = 900
results = []



try:
    # INIT SENSOR CLASS AND ESTABLISHING PORT CONNECTION.
    sensor_sps30 = sps30.Sps30(device_port)

    # STARTING UP SPS30 SENSOR. GOING FROM IDLE MODE TO MEASUREMENT MODE
    sensor_sps30.start_measurement(start_up_time=startup_time)

    # PERFORMING MEASUREMENTS
    for i in range(samples):
        results.append([time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), sensor_sps30.read_measured_values()])
        time.sleep(1)

    # TURNING OFF MEASUREMENT MODE. RETURNING TO IDLE MODE.
    sensor_sps30.stop_measurement()

    # CLOSE PORT CONNECTION.
    sensor_sps30.close_port()

    # SAVE DATA TO CSV
    pd.DataFrame(results).to_csv('measurement_samples.csv', index=False)

except RuntimeError:
    exit()
