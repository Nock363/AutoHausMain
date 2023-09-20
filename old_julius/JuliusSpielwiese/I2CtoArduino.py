import smbus
import struct
import time

# Define I2C bus number and Arduino slave address
bus = smbus.SMBus(1)
address = 0x8

def get_data():
    # Define number of floats to receive
    floats_received = 2

    # Read floats sent by Arduino over I2C
    data = bus.read_i2c_block_data(address, 0, floats_received * 4)
    floats = struct.unpack('f' * floats_received, bytearray(data))
 
    # Print received data
    print("TDS value: {} ppm".format(floats[0]))
    print("pH value: {}".format(floats[1]))


# Send Data
def send_data():
    bus.write_byte(address, 1)
    time.sleep(1)
    bus.write_byte(address, 0)

while True:
    bus.write_byte(address, 1)
    time.sleep(0.3)
    bus.write_byte(address, 0)
    time.sleep(0.3)

    get_data()

