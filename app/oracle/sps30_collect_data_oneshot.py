#!/home/pi/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
import time
import numpy as np
from dbManager import *
from sps30_driver import sps30


device_port = "/dev/ttyUSB0"

try:
    # INIT SENSOR CLASS AND ESTABLISHING PORT CONNECTION.
    sensor_sps30 = sps30.Sps30(device_port)

    # TODO: Check that it is running in measurement mode

    # PERFORMING MEASUREMENTS
    date = time.strftime('%Y-%m-%d')
    timestamp = time.strftime('%H:%M:%S')
    result = sensor_sps30.read_measured_values()
    time.sleep(1)

    # CLOSE PORT CONNECTION.
    sensor_sps30.close_port()

    # ERROR HANDLING
    if (result.length != 12):
        # Print the error message
        print(result[0])
        # TODO: log errors to separate table in database?
        exit()

    # ADD DATA SAVING
    add_entry(date, timestamp, result[0], result[1], result[2], result[3], result[4],
              result[5], result[6], result[7], result[8], result[9])
except NotImplemented:
    exit()
