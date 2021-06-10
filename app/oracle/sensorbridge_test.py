#!/home/pi/IoT-Microservice/venv/bin/python3
# CHANGE PYTHON PATH TO MATCH YOUR LOCAL INSTALLATION

import time
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, SensorBridgeShdlcDevice
from crccheck.crc import Crc8Nrsc5

data = bytearray.fromhex("BEEF")
crc = Crc8Nrsc5.calc(data)
print(crc)

def calculateChecksum(data: list):
    assert len(data) == 2
    crc = Crc8Nrsc5.calc(data)
    data.append(crc)
    return data


# Connect to the device with default settings:
#  - baudrate:      460800
#  - slave address: 0
with ShdlcSerialPort(port='/dev/ttyUSB1', baudrate=460800) as port:
    device = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)

    # Print some device information
    print("Version: {}".format(device.get_version()))
    print("Product Name: {}".format(device.get_product_name()))
    print("Serial Number: {}".format(device.get_serial_number()))

    # Enable port 1 with an I2C frequency of 400kHz and a voltage of 5V
    device.set_i2c_frequency(SensorBridgePort.ONE, frequency=400e3)
    device.set_supply_voltage(SensorBridgePort.ONE, voltage=5.0)
    device.switch_supply_on(SensorBridgePort.ONE)

    # Perform synchronous I2C transceive on port 1
    rx_data = device.transceive_i2c(
        SensorBridgePort.ONE, address=0x58, tx_data=[0x20, 0x15],
        rx_length=6, timeout_us=100e3)
    print("Received data: {}".format(rx_data))

    # Perform synchronous I2C transceive on port 1
    rx_data = device.transceive_i2c(
        SensorBridgePort.ONE, address=0x58, tx_data=[0x20, 0x03],
        rx_length=0, timeout_us=100e3)
    print("Received data: {}".format(rx_data))

    for i in range(30):
        time.sleep(1)
        # Perform synchronous I2C transceive on port 1
        rx_data = device.transceive_i2c(
            SensorBridgePort.ONE, address=0x58, tx_data=[0x20, 0x08],
            rx_length=6, timeout_us=100e3)
        print("Received data: {}".format(rx_data))

    # Perform synchronous I2C transceive on port 1
    rx_data = device.transceive_i2c(
        SensorBridgePort.ONE, address=0x58, tx_data=[0x00, 0x06],
        rx_length=0, timeout_us=100e3)
    print("Received data: {}".format(rx_data))

    # Perform asynchronous I2C transceive on port 1
    # handle = device.start_repeated_i2c_transceive(
    #     SensorBridgePort.ONE, interval_us=100e3, address=0x58,
    #     tx_data=[0x20, 0x08], rx_length=6, timeout_us=1000e3, read_delay_us=10e3)
    # time.sleep(1.0)  # let the device perform the repeated transceives
    # buffer = device.read_buffer(handle)
    # device.stop_repeated_i2c_transceive(handle)
    # print("Lost bytes: {}".format(buffer.lost_bytes))
    # print("Remaining bytes: {}".format(buffer.remaining_bytes))
    # print("Buffered values: {}".format(
    #     [value.data for value in buffer.values]))
