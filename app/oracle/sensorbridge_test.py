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
    return crc


def compareChecksum(data: list, checksum: int):
    if (calculateChecksum(data) != checksum):
        return -1
    return 0


def separatePackets(data: list):
    # 16bit data packets with 8bit checksum
    rawDataPackets = []
    tempdata = bytearray()
    for i in range(len(data)):
        tempdata.append(data[i])
        if ((i + 1) % 3 == 0):
            rawDataPackets.append(bytes(tempdata))
            tempdata = bytearray()
    return rawDataPackets


def sendCommand(address: int, command: list, expectedReturnbytes: int,  device: SensorBridgeShdlcDevice, data: list = []):
    txData = command + data

    rx_data = device.transceive_i2c(
        SensorBridgePort.ONE, address=address, tx_data=txData,
        rx_length=expectedReturnbytes, timeout_us=100e3)

    rawDataPackets = separatePackets(rx_data)

    for packet in rawDataPackets:
        dataOnly = bytes(packet)[:2]
        checkSum = bytes(packet)[2:]
        if (compareChecksum(bytearray(dataOnly), int.from_bytes(checkSum, byteorder="big")) != 0):
            print("checksum error")

    print("Received data '{}' of length '{}'".format(
        bytes(rx_data).hex(), len(rx_data)))

    return rawDataPackets


# Connect to the device with default settings:
#  - baudrate:      460800
#  - slave address: 0
with ShdlcSerialPort(port='/dev/ttyUSB1', baudrate=460800) as port:
    device = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)

    # Print some device information
    # This is information about the sensor bridge!
    print("Version: {}".format(device.get_version()))
    print("Product Name: {}".format(device.get_product_name()))
    print("Serial Number: {}".format(device.get_serial_number()))

    # Enable port 1 with an I2C frequency of 400kHz and a voltage of 5V
    device.set_i2c_frequency(SensorBridgePort.ONE, frequency=400e3)
    device.set_supply_voltage(SensorBridgePort.ONE, voltage=5.0)
    device.switch_supply_on(SensorBridgePort.ONE)

    # Prepare the sensor to start reading data with a "sgp30_iaq_init" command
    rx_data = device.transceive_i2c(
        SensorBridgePort.ONE, address=0x58, tx_data=[0x20, 0x03],
        rx_length=0, timeout_us=100e3)

    # for i in range(30):
    #     time.sleep(1)
    #     # Read the data using "sgp30_measure_iaq" command
    #     # Note that the first 15 measurements do not contain any valid data
    #     # TODO: fitler out the first 15 measurements
    #     rx_data = device.transceive_i2c(
    #         SensorBridgePort.ONE, address=0x58, tx_data=[0x20, 0x08],
    #         rx_length=6, timeout_us=100e3)
    #     print("Received data '{}' of length '{}'".format(
    #         bytes(rx_data).hex(), len(rx_data)))

    for i in range(30):
        time.sleep(1)
        sendCommand(address=0x58, command=[0x20, 0x08],
                    expectedReturnbytes=6, device=device)

    # Perform a soft reset of all sensirion devices on the bus
    rx_data = device.transceive_i2c(
        SensorBridgePort.ONE, address=0x58, tx_data=[0x00, 0x06],
        rx_length=0, timeout_us=100e3)
