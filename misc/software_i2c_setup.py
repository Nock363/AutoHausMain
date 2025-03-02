import sys
sys.path.insert(0, '../')
from Handler.DataHandler import DataHandler

import re

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class SoftwareI2CSetup():

    configFile = []
    softwareI2C_Start = -1
    softwareI2C_End = -1

    startTag = "#SOFTWARE_I2C_START"
    endTag = "#SOFTWARE_I2C_END"

    path = "/boot/config.txt"
    #path= "/home/user/AutoHausMain/config_backup_test.txt"

    def __init__(self):
        self.dataHandler = DataHandler()

    def setup(self):
        pinText = self.createPinText()
        newConfig = ""
        with open(self.path,"r") as file:
            data = file.readData()
            regex = re.compile("#SOFTWARE_I2C_START.*#SOFTWARE_I2C_END",re.DOTALL)
            # if(re.search(regex,data) is None):
            #     print("No Tags found")
            
            print(f"regex:{regex}")
            replacement = f"#SOFTWARE_I2C_START\n{pinText}#SOFTWARE_I2C_END"
            newConfig = re.sub(regex,replacement,data)
            file.close()

        if(newConfig != ""):
            with open(self.path,"w") as file:
                file.write(newConfig)
                file.close()

   
    def createPinText(self):
        pins = self.dataHandler.getAllPins(mode="I2C")
        pins = list(pins)
        print(f"pins: {pins}")
        substring = ""

        
        for p in pins:
            
                busNumber = p["pinID"] + 2

                sda=p["dataPin2"]
                scl=p["dataPin1"]
                #print(f"pin {p['pinID']}: sda={sda} scl={scl}")
                command = f"dtoverlay=i2c-gpio,bus={busNumber},i2c_gpio_delay_us=1,i2c_gpio_sda={sda},i2c_gpio_scl={scl}\n"
                substring = substring + command
                busNumber = busNumber - 1 
                
        return substring


    # def clearI2CPart(self):







setup = SoftwareI2CSetup()
setup.setup()