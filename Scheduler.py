from dataclasses import dataclass
from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler
import Sensoren
import Controller
import time
import logging
import json
import os
logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('simple_example')
logger.setLevel(logging.WARNING)



@dataclass
class SensorConfig:
    sensorClass: type
    sensor: Sensoren.Sensor
    intervall: float

class Logik:
    inputs : list[dict]
    outputs : list[dict]
    controller : Controller.BaseBlocks.BaseBlock



class Scheduler():

    __sensoren : list[SensorConfig]
    __mongoHandler : MongoHandler

    def __init__(self):
        #get absolute path to config file from relative path
        self.__sensoren = []
        print(self.__sensoren)
        self.__mongoHandler = MongoHandler()
        self.__configHandler = ConfigHandler()
        
        sensorConfig = self.__configHandler.getSensors()
        # sensorsConfig = json.load(open(os.path.join(os.path.dirname(__file__),"Configs/sensors.json")))
        # sensorsConfig = self.__mongoHandler.getSensors()
        #logger.debug(list(sensorsConfig))
        for entry in sensorsConfig:
            
            logger.debug(f"+++++++++++++{entry}+++++++++++++")
            objClass = self.importSensor(entry["class"])
            obj = objClass(name=entry["name"],pinID = entry["pinID"])
        
            conf = SensorConfig(objClass,obj,entry["intervall"])
            logger.debug(f"config: {conf}")
            self.__sensoren.append(conf)

        logger.debug(self.__sensoren)

        logicConfig = self.__mongoHandler.getAllLogics()

        for entry in logicConfig:

            for inputData in entry["inputs"]:
                sensorName = inputData["sensor"]

    def searchForSensorByName(self,name:str) -> Sensoren.Sensor:
        for conf in self.__sensoren:
            if(conf.sensor.name == name):
                return conf.sensor
            
        raise Exception("Sensor nicht in Liste!")

        # aht20 = self.importSensor("HudTemp_AHT20")
        # logger.debug(type(aht20))
        # test = aht20(pinID = 7)

    def runAllSensors(self):
        logger.debug("run all Sensors:")
        
        for sensor in self.__sensoren:
            logger.debug(sensor)
            sensor.sensor.run()

    def importSensor(self,sensorName:str):
        #moduleString = "Sensoren.HudTemp_AHT20"
        moduleString = f"Sensoren.{sensorName}"
        module = __import__(moduleString)
        #logger.debug("module:",module)
        attr = getattr(module,sensorName)
        #logger.debug("attribute:",attr)
        return getattr(attr,sensorName)


scheduler = Scheduler()


while(True):
    try:
        scheduler.runAllSensors()
        time.sleep(10)
    except Exception as err:
        logger.error(err)