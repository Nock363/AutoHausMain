import sys
sys.path.insert(0, 'Handler/')
from DatabaseHandlers import MongoHandler

import re

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class SoftwareI2CSetup():

    configFile = []
    softwareI2C_Start = -1
    softwareI2C_End = -1

    startTag = "#SOFTWARE_I2C_START"
    endTag = "#SOFTWARE_I2C_END"


    def __init__(self):
        self.mongoHandler = MongoHandler()


    def setup(self):
        pinText = self.createPinText()
        newConfig = ""
        with open("/home/user/AutoHausMain/config_backup_test.txt","r") as file:
            data = file.read()
            regex = re.compile("#SOFTWARE_I2C_START.*#SOFTWARE_I2C_END",re.DOTALL)
            replacement = f"#SOFTWARE_I2C_START\n{pinText}#SOFTWARE_I2C_END"
            newConfig = re.sub(regex,replacement,data)
            file.close

        if(newConfig != ""):
            with open("/home/user/AutoHausMain/config_backup_test.txt","w") as file:
                file.write(newConfig)
                file.close()

    def readAndClear(self):
        with open("/home/user/AutoHausMain/config_backup_test.txt") as file:
            configFile = file.readlines()
            for i, line in enumerate(configFile):
                
                if self.startTag in line:
                    self.softwareI2C_Start = i
                if self.endTag in line:
                    self.softwareI2C_End = i

            print(f"start: {self.softwareI2C_Start}, end: {self.softwareI2C_End}")

            #configFile.pop(0:2)

            # print("_______________")
            # for n in range(self.softwareI2C_Start+1,self.softwareI2C_End):
            #     print(configFile.pop(n))
            # print("_______________")

            for i, line in enumerate(configFile):
                print(f"{i}|{line}")

    def createPinText(self):
        pins = self.mongoHandler.getAllPins(mode="I2C")
        pins = list(pins)
        
        substring = ""

        busNumber = len(pins)+2
        for p in pins:
            
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