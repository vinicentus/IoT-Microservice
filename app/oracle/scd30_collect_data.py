#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
from datetime import datetime
from scd30_i2c import SCD30
from dbManager import add_entry_scd30, convertTimeStampToUTCString


scd30 = SCD30()

if scd30.get_data_ready():
    timestamp = convertTimeStampToUTCString(datetime.now())
    m = scd30.read_measurement()

    if m is not None:
        print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
        add_entry_scd30(timestamp, m[0], m[1], m[2])
