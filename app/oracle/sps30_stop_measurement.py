#!/home/pi/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
from sps30_driver import sps30


device_port = "/dev/ttyUSB0"

try:
    # INIT SENSOR CLASS AND ESTABLISHING PORT CONNECTION.
    sensor_sps30 = sps30.Sps30(device_port)

    # TURNING OFF MEASUREMENT MODE. RETURNING TO IDLE MODE.
    sensor_sps30.stop_measurement()

    # CLOSE PORT CONNECTION.
    sensor_sps30.close_port()

except NotImplemented:
    exit()
