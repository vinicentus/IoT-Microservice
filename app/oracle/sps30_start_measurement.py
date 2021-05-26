#!/home/pi/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
from dbManager import *
from sps30_driver import sps30


device_port = "/dev/ttyUSB0"
startup_time = 30

try:
    # INIT SENSOR CLASS AND ESTABLISHING PORT CONNECTION.
    sensor_sps30 = sps30.Sps30(device_port)

    # TODO: CONFIGURE AUTOMATIC FAN CLEANING INTERVAL
    # sensor_sps30.read_write_auto_cleaning_interval()

    # STARTING UP SPS30 SENSOR. GOING FROM IDLE MODE TO MEASUREMENT MODE
    sensor_sps30.start_measurement(start_up_time=startup_time)

    # CLOSE PORT CONNECTION.
    sensor_sps30.close_port()

except NotImplemented:
    exit()
