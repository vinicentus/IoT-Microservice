#!/usr/local/bin/python3.8
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
import time
from sps30_driver import sps30

device_port = "/dev/ttyUSB0"
startup_time = 8


try:
    sensor_sps30 = sps30.Sps30(device_port)
    sensor_sps30.start_measurement(start_up_time=startup_time)
    # EXECUTES FAN CLEANING COMMAND
    sfc = sensor_sps30.start_fan_cleaning()
    time.sleep(11)
    sensor_sps30.stop_measurement()
    sensor_sps30.close_port()

except TypeError as e:
    print(e)
    exit()
