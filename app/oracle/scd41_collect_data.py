#!/home/pi/IoT_Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
from datetime import datetime
from dbManager import add_entry_scd41, convertTimeStampToUTCString
from raspberry_pi_i2c_scd4x_python.i2c_class import I2C
from raspberry_pi_i2c_scd4x_python.sensor_class import SCD4x

i2c = I2C()
scd41 = SCD4x()

i2c.sensirion_i2c_hal_init()

scd41.scd4x_measure_single_shot()

if scd41.scd4x_get_data_ready_status():
    timestamp = convertTimeStampToUTCString(datetime.utcnow())
    m = scd41.scd4x_read_measurement()

    if m is not None:
        print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}°C, rh: {m[2]:.2f}%")
        add_entry_scd41(timestamp, m[0], m[1], m[2])

i2c.sensirion_i2c_hal_free()
