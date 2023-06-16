from Logics.BaseLogic import BaseLogic
import Sensoren
import Actuators
import Controllers
from Handler.DataHandler import DataHandler
import os
import logging


logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('simple_example')
logger.setLevel(logging.INFO)


class MainContainer():

    __sensors : list[Sensoren.Sensor]
    __actuators : list[Actuators.Actuator]
    __logics : list[BaseLogic]
    __dataHandler : DataHandler

    def __init__(self):
        self.__dataHandler = DataHandler()
        self.loadSensors()
        self.loadActuators()
        self.loadLogics()

    def getActuator(self, name : str) -> Actuators.Actuator:
        #search for actuator with actuator.name == name
        for actuator in self.__actuators:
            if actuator.name == name:
                return actuator
        return None

    def getSensor(self, name : str) -> Sensoren.Sensor:
        #search for sensor with sensor.name == name
        for sensor in self.__sensors:
            if sensor.name == name:
                return sensor
        return None

    def getLogic(self, name : str) -> BaseLogic:
        #search for logic with logic.name == name
        for logic in self.__logics:
            if logic.name == name:
                return logic
        return None

    def loadSensors(self):
        self.__sensors = []
        sensorConfig = self.__dataHandler.getSensors()
        for entry in sensorConfig:
            sensorClass = self.__importSensor(entry["class"])
            sensor = sensorClass(name=entry["name"],pinID = entry["pinID"],collection = entry["collection"])
            self.__sensors.append(sensor)

        logger.debug(self.__sensors)

    def loadActuators(self):
        self.__actuators = []
        actuatorsConfig = self.__dataHandler.getActuators()
        for entry in actuatorsConfig:
            
            actuatorClass = self.__importActuator(entry["type"])
            actuator = actuatorClass(name=entry["name"],collection = entry["collection"],initialState = entry["initialState"],config = entry["config"])
            self.__actuators.append(actuator)

        logger.debug(self.__actuators)

    def loadLogics(self):
        self.__logics = []
        logicConfig = self.__dataHandler.getLogics()
        for entry in logicConfig:
            controllerConfig = entry["controller"]
            controllerClass = self.__importController(controllerConfig["controller"])
            controller = controllerClass(controllerConfig["config"])
            inputs = entry["inputs"]
            for input in inputs:
                input["object"] = self.getSensor(input["sensor"])
                if(input["object"] == None):
                    raise Exception(f"Sensor {input['sensor']} not found") 

            outputs = entry["outputs"]
            for output in outputs:
                output["object"] = self.getActuator(output["actuator"])
                if(output["object"] == None):
                    raise Exception(f"Actuator {output['actuator']} not found")
                
            self.__logics.append(BaseLogic(entry["name"],controller,inputs,outputs))

        logging.debug(self.__logics)

    def __importSensor(self,sensorName:str):
        #moduleString = "Sensoren.HudTemp_AHT20"
        moduleString = f"Sensoren.{sensorName}"
        module = __import__(moduleString)
        #logger.debug("module:",module)
        attr = getattr(module,sensorName)
        #logger.debug("attribute:",attr)
        return getattr(attr,sensorName)
    
    def __importActuator(self,actuatorName:str):
        moduleString = f"Actuators.{actuatorName}"
        module = __import__(moduleString)
        #logger.debug("module:",module)
        attr = getattr(module,actuatorName)
        #logger.debug("attribute:",attr)
        return getattr(attr,actuatorName)

    def __importController(self,controllerName:str):
        moduleString = f"Controllers.{controllerName}"
        module = __import__(moduleString)
        #logger.debug("module:",module)
        attr = getattr(module,controllerName)
        #logger.debug("attribute:",attr)
        return getattr(attr,controllerName)


# class ServiceContainer():
#     __restApi : RestAPI
    

#     def __init__(self):
#         self.__scheduler = Scheduler()
#         self.__scheduler.setServiceContainer(self)
#         self.__restApi = RestAPI(scheduler = self.__scheduler)

    
#     @property
#     def restAPI(self):
#         return self.__restApi
