import sys
import logging
import smbus
import struct
import time
sys.path.insert(0, '../')
from Sensoren.Sensor import Sensor


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)




class Arduino(Sensor):

    def __init__(self,name:str,pinID,collection:str,*args, **kwargs):
        dataStructure={"Ph":float,"Ec":float}
        super().__init__(
            name=name,
            collection=collection,
            pinID = pinID,
            dataStructure=dataStructure,
            range=(0,15),               #TODO: Range nur für PH angewendet und nicht für ec
            *args,
            **kwargs)
        # Define I2C bus number and Arduino slave address
        self.bus = smbus.SMBus(pinID+2)
        self.address = 0x8

    def run(self):
              
        # Define number of floats to receive
        floats_received = 2

        # Read floats sent by Arduino over I2C
        data = self.bus.read_i2c_block_data(self.address, 0, floats_received * 4)
        floats = struct.unpack('f' * floats_received, bytearray(data))
 
        # Print received data
        print("TDS value: {} ppm".format(floats[0]))
        print("pH value: {}".format(floats[1]))
        
        #format macht aus float strings.... oh ne. ok danke =/
        #klassicher fall von wald vor lauter bäumen nicht xD
        #passiert den besten
        #me happy woooh
        phValue = float(floats[1])
        ecValue = float(floats[0])
        return super().createData({"Ph":phValue,"Ec":ecValue})


# # Send Data
# def send_data():
#     bus.write_byte(address, 1)
#     time.sleep(1)
#     bus.write_byte(address, 0)

# while True:
#     bus.write_byte(address, 1)
#     time.sleep(0.3)
#     bus.write_byte(address, 0)
#     time.sleep(0.3)

#     get_data()''
