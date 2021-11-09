#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
import time
from sps30_driver import sps30

device_port = "/dev/ttyUSB0"


try:
    sensor_sps30 = sps30.Sps30(device_port)
    # EXECUTES FAN CLEANING COMMAND
    sfc = sensor_sps30.start_fan_cleaning()
    time.sleep(1)
    sensor_sps30.close_port()

except TypeError as e:
    print(e)
    exit()
