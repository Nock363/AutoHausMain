import sys
import logging
import smbus
import struct
import time

# Define I2C bus number and Arduino slave address
bus = smbus.SMBus(3)
address = 0x8
DATA_FORMAT = 'ii'  # Format string for a float and an integer

# def get_data():
#     # Define number of floats to receive
#     floats_received = 2

#     # Read floats sent by Arduino over I2C
#     data = bus.read_i2c_block_data(address, 0, floats_received * 4)
#     floats = struct.unpack('f' * floats_received, bytearray(data))
 
#     # Print received data
#     print("TDS value: {} ppm".format(floats[0]))
#     print("pH value: {}".format(floats[1]))


# Send Data
# def send_data():
#     bus.write_byte(address, 1)
#     time.sleep(1)
#     bus.write_byte(address, 0)

# while True:
#dataA is defined as hex value

duration = 1

data1 = struct.pack(DATA_FORMAT, 1, duration)
data2 = struct.pack(DATA_FORMAT, 2, duration)
data3 = struct.pack(DATA_FORMAT, 3, duration)
bus.write_i2c_block_data(address, 0, list(data1))
time.sleep(1.3)
bus.write_i2c_block_data(address, 0, list(data2))
time.sleep(1.3)
bus.write_i2c_block_data(address, 0, list(data3))

#get_data()


    