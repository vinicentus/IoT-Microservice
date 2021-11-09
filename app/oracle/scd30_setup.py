#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
import time
from scd30_i2c import SCD30


scd30 = SCD30()

scd30.set_measurement_interval(60)
scd30.start_periodic_measurement()

time.sleep(1)
