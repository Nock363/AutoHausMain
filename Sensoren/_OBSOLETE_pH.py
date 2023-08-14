import sys
import logging
import smbus
import struct
import time
#TODO: Löschen?
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




logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
from Sensoren.Sensor import Sensor


#add code to init and error if not connected



class PH_TDS_arduino(Sensor):

    def __init__(self,name:str,pinID:int):
        super().__init__(name,collection="PH",queueDepth = 10,pinID=pinID)
        #i2c = I2C(self.i2cBus) //hmm
        #self.aht20 = adafruit_ahtx0.AHTx0(i2c)

    def run(self):
        return super().createData({"TDS":format(floats[0]),"PH":.format(floats[1])})
