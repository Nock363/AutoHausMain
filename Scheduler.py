from dataclasses import dataclass
from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Handler.DatabaseHandlers import MongoHandler
from Handler.JsonHandlers import ConfigHandler
from Logics.BaseLogic import BaseLogic
import Sensoren
import Actuators
import Controllers
import time
import logging
import json
import os
logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('simple_example')
logger.setLevel(logging.INFO)
import asyncio
from multiprocessing import Process, Semaphore, Event


@dataclass
class SensorConfig:
    name: str
    sensorClass: type
    sensor: Sensoren.Sensor
    intervall: float

@dataclass
class ActuatorConfig:
    name: str
    actuatorClass: type
    actuator: Actuators.Actuator


    


class Scheduler():

    __sensoren : list[SensorConfig]
    __actuators : list[ActuatorConfig]
    __mongoHandler : MongoHandler

    __runRoutine : bool
    __intervall = 1
    __environName = "RUN_SCHEDULER"

    __stopFlag : Event
    __process : Process


    def __init__(self,runRoutine = False, stopEvent = Event()):
        #get absolute path to config file from relative path
        self.__sensoren = []
        self.__actuators = []
        self.__logics = []
        self.__runRoutine = runRoutine
        print(self.__sensoren)
        self.__mongoHandler = MongoHandler()
        self.__configHandler = ConfigHandler()
        self.__stopFlag = stopEvent
        

        #load all sensors into __sensoren
        sensorConfig = self.__configHandler.getSensors()
        for entry in sensorConfig:
            
            objClass = self.importSensor(entry["class"])
            obj = objClass(name=entry["name"],pinID = entry["pinID"],collection = entry["collection"])
            conf = SensorConfig(entry["name"],objClass,obj,entry["intervall"])
            logger.debug(f"config: {conf}")
            self.__sensoren.append(conf)

        logger.debug(self.__sensoren)

        #load all actuators into __actuators
        actuatorsConfig = self.__configHandler.getActuators()
        for entry in actuatorsConfig:
            
            objClass = self.importActuator(entry["type"])
            obj = objClass(name=entry["name"],collection = entry["collection"],initialState = entry["initialState"],config = entry["config"])
            conf = ActuatorConfig(entry["name"],objClass,obj)
            logger.debug(f"config: {conf}")
            self.__actuators.append(conf)

        logger.debug(self.__actuators)

        #load all logics into __logics
        logicConfig = self.__configHandler.getLogics()
        for entry in logicConfig:
            controllerConfig = entry["controller"]
            objClass = self.importController(controllerConfig["controller"])
            controller = objClass(controllerConfig["config"])
            inputs = entry["inputs"]
            for input in inputs:
                input["object"] = self.searchForSensorByName(input["sensor"])
                
            outputs = entry["outputs"]
            for output in outputs:
                output["object"] = self.searchForActuatorByName(output["actuator"])
                
            self.__logics.append(BaseLogic(entry["name"],controller,inputs,outputs))

        logging.debug(self.__logics)
            #logic = Logic(entry["name"])
            

    def searchForSensorByName(self,name:str) -> Sensoren.Sensor:
        for conf in self.__sensoren:
            if(conf.name == name):
                return conf.sensor
            
        raise Exception(f"Sensor {name} nicht in Liste!")


    def searchForActuatorByName(self,name:str) -> Sensoren.Sensor:
        for conf in self.__actuators:
            if(conf.name == name):
                return conf.actuator
            
        raise Exception("Sensor nicht in Liste!")

    def fullRun(self):
        #Diese Funktion ruft alle Logics auf, triggert die Sensoren und aktiviert darauf die Aktoren, welche in der Logik vermerkt sind
        #Ein Report wird erstellt und zurückgegeben, darüber welcher Sensor erfolgreich lief und welcher nicht

        report = []
        for logic in self.__logics:

            startTime = time.time()
            try:
                logic.run()
                report.append({"name": logic.name, "success": True, "time": time.time() - startTime})    
            except Exception as e:
                report.append({"name": logic.name, "success": False, "time": time.time() - startTime, "error": e})
        
        #if logger is set to info, the report will be printed without the error
        #if logger is set to debug, the report will be printed with the error
        if logger.level == logging.INFO:
            logger.info(f"#############Logic run finished [{time.time()}]########")
            for entry in report:
                logger.info(f"Logic: {entry['name']}, Success: {entry['success']}, Time: {entry['time']}")

        if logger.level == logging.DEBUG:
            logger.debug(f"#############Logic run finished [{time.time()}]########")
            for entry in report:
                logger.debug(f"Logic: {entry['name']}, Success: {entry['success']}, Time: {entry['time']}, Error: {entry['error']}")
        
        # logger.debug("Logic run finished:", report)
        return report
    
    
    
               
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
    
    def setActuator(self,name,state: bool):

        for actuator in self.__actuators:
            if(actuator.name == name):
                actuator.actuator.set(state)
                return True

        #if no actuator with this name was found, throw error in German
        return f"Es gibt keinen Aktuator mit dem Namen {name}"

    #This function runs the function fullRun() as a coroutine in a loop
    async def routine(self):
        while(self.__runRoutine):
            try:
                self.fullRun()
                await asyncio.sleep(10)
            except Exception as err:
                logger.error(err)

    def runRoutine(self):
        asyncio.run(self.routine())

    def runForever(self,stopFlag):
        while not stopFlag.is_set():
            self.fullRun()
            time.sleep(1)

    def startProcess(self):
        self.__stopFlag = Event()
        self.__process = Process(target=self.runForever,args=(self.__stopFlag,))
        self.__process.start()
        logger.info("Scheduler Process gestartert")

    def stopProcess(self):
        if(self.__process.is_alive()):
            self.__stopFlag.set()
            self.__process.join()
            logger.info("Scheduler Process beendet")    
        else:
            logger.error("Scheduler Process läuft aktuell nicht. Nutze startProcess um den Prozess zu starten.")

    def statusProcess(self):
        return self.__process.is_alive()

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.runForever()
    # scheduler.fullRun()
    