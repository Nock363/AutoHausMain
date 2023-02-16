from dataclasses import dataclass
from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler
import Sensoren
import Actuators
import Controllers
import time
import logging
import json
import os
logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('simple_example')
logger.setLevel(logging.WARNING)



@dataclass
class SensorConfig:
    name: str
    sensorClass: type
    sensor: Sensoren.Sensor
    intervall: float

@dataclass
class ActuatorConfig:
    actuatorClass: type
    actuator: Actuators.Actuator

@dataclass
class Logic:
    name : str
    controller : Controllers.BaseBlocks.BaseBlock
    inputs : list[dict]
    outputs : list[dict]
    


class Scheduler():

    __sensoren : list[SensorConfig]
    __actuators : list[ActuatorConfig]
    __mongoHandler : MongoHandler


    def __init__(self):
        #get absolute path to config file from relative path
        self.__sensoren = []
        self.__actuators = []
        print(self.__sensoren)
        self.__mongoHandler = MongoHandler()
        self.__configHandler = ConfigHandler()
        
        #load all sensors into __sensoren
        sensorConfig = self.__configHandler.getSensors()
        for entry in sensorConfig:
            
            objClass = self.importSensor(entry["class"])
            obj = objClass(name=entry["name"],pinID = entry["pinID"])
            conf = SensorConfig(name,objClass,obj,entry["intervall"])
            logger.debug(f"config: {conf}")
            self.__sensoren.append(conf)

        logger.debug(self.__sensoren)

        #load all actuators into __actuators
        actuatorsConfig = self.__configHandler.getActuators()
        for entry in actuatorsConfig:
            
            objClass = self.importActuator(entry["type"])
            obj = objClass(name=entry["name"],collection = entry["collection"],initialState = entry["initialState"],config = entry["config"])
            conf = ActuatorConfig(objClass,obj)
            logger.debug(f"config: {conf}")
            self.__actuators.append(conf)

        logger.debug(self.__actuators)

        #load all logics into __logics
        logicConfig = self.__configHandler.getLogics()
        for entry in logicConfig:
            objClass = self.importController(entry["controller"])
            controller = objClass()
            inputs = []
            for input in entry.inputs:
                

            #logic = Logic(entry["name"])
            

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
    
    def importActuator(self,actuatorName:str):
        moduleString = f"Actuators.{actuatorName}"
        module = __import__(moduleString)
        #logger.debug("module:",module)
        attr = getattr(module,actuatorName)
        #logger.debug("attribute:",attr)
        return getattr(attr,actuatorName)

    def importController(self,controllerName:str):
        moduleString = f"Controllers.{controllerName}"
        module = __import__(moduleString)
        #logger.debug("module:",module)
        attr = getattr(module,controllerName)
        #logger.debug("attribute:",attr)
        return getattr(attr,controllerName)

    def getSensor(self,name):
        for sensor in self.__sensoren:
            if(sensor.name == name):
                return sensor
    
    def getActuator(self,name):
        for actuator in self.__actuators:
            if(actuator.name == name):
                return actuator
    


scheduler = Scheduler()


# while(True):
#     try:
#         scheduler.runAllSensors()
#         time.sleep(10)
#     except Exception as err:
#         logger.error(err)