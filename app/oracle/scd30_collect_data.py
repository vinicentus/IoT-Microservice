#!/home/pi/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
import datetime
from scd30_i2c import SCD30
from dbManager import *
from sps30_driver import sps30


scd30 = SCD30()

if scd30.get_data_ready():
    timestamp = datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    m = scd30.read_measurement()

    if m is not None:
        print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
        add_entry_scd30(timestamp, m[0], m[1], m[2])
