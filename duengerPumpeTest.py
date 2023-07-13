import sys
import logging
import smbus
import struct
import time

if len(sys.argv) != 3:
    print("Please provide two integer numbers as start parameters.")
    print("The First 1-3 refers to the Pump Number, the second is the Time in  milli seconds")
    print("for example: python3 i2cArduino_Test.py 2 4")
    sys.exit(1)


try:
    pump = int(sys.argv[1])
    duration = int(sys.argv[2]*1000)
except ValueError:
    print("Invalid start parameters. Please provide two integer numbers.")
    sys.exit(1)

# Define I2C bus number and Arduino slave address
bus = smbus.SMBus(7)
address = 0x8
DATA_FORMAT = 'ii'  # Format string for a float and an integer

data1 = struct.pack(DATA_FORMAT, pump, duration)
#data2 = struct.pack(DATA_FORMAT, 2, duration)
#data3 = struct.pack(DATA_FORMAT, 3, duration)
#bus.write_i2c_block_data(address, 0, list(data1))
#time.sleep(1)
bus.write_i2c_block_data(address, 0, list(data1))

#time.sleep(1.3)
#bus.write_i2c_block_data(address, 0, list(data2))
#time.sleep(1.3)
#bus.write_i2c_block_data(address, 0, list(data3))

#get_data()


    