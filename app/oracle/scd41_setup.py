#!/home/pi/IoT_Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION
from raspberry_pi_i2c_scd4x_python.i2c_class import I2C
from raspberry_pi_i2c_scd4x_python.sensor_class import SCD4x

i2c = I2C()
sensor = SCD4x()

i2c.sensirion_i2c_hal_init()

# Clean up potential SCD40 states
sensor.scd4x_wake_up()
sensor.scd4x_stop_periodic_measurement()
sensor.scd4x_reinit()

serial = sensor.scd4x_get_serial_number()
print(f"Serial number: {hex(serial)}")

i2c.sensirion_i2c_hal_free()
