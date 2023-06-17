from dataclasses import dataclass
from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Handler.DataHandler import DataHandler
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
from Utils.Container import MainContainer

class Scheduler():

    __sensoren : list[Sensoren.Sensor]
    __actuators : list[Actuators.Actuator]
    __dataHandler : DataHandler

    __runRoutine : bool
    __intervall = 1
    __environName = "RUN_SCHEDULER"

    __stopFlag : Event
    __process : Process

    __mainContainer : MainContainer

    def __init__(self,runRoutine = False, stopEvent = Event(),mainContainer : MainContainer = None):
        #get absolute path to config file from relative path
        self.__sensoren = mainContainer.sensors
        self.__actuators = mainContainer.actuators
        self.__logics = mainContainer.logics
        self.__runRoutine = runRoutine
        print(self.__sensoren)
        self.__dataHandler = DataHandler()
        self.__stopFlag = stopEvent
        self.__mainContainer = MainContainer


    def setMainContainer(self,mainContainer:MainContainer):
        self.__mainContainer = mainContainer

    def run(self):
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
            sensor.run()

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

    #This function runs the function run() as a coroutine in a loop
    async def routine(self):
        while(self.__runRoutine):
            try:
                self.run()
                await asyncio.sleep(10)
            except Exception as err:
                logger.error(err)

    def runRoutine(self):
        asyncio.run(self.routine())

    def runForever(self,stopFlag):
        while not stopFlag.is_set():
            self.run()
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
    # scheduler.run()
    