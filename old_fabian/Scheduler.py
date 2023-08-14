#from dataclasses import dataclass
#from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Handler.DataHandler import DataHandler
#from Logics.BaseLogic import BaseLogic
import Sensoren
import Actuators
import Controllers
import time
import logging
import json
import os
logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('scheduler')
logger.setLevel(logging.DEBUG)
import asyncio
from multiprocessing import Process, Semaphore, Event
from Utils.Container import MainContainer

class Scheduler():

    __sensors : list[Sensoren.Sensor]
    __actuators : list[Actuators.Actuator]
    __dataHandler : DataHandler

    __runRoutine : bool
    __intervall = 1
    __stopFlag : Event
    __process : Process

    __samplingRate = 1.0 #Abtastrate der Sensoren und der Logik. Logik kann auch seltener laufen aber NICHT schneller als die sampling Rate

    __mainContainer : MainContainer

    def __init__(self,runRoutine = False, stopEvent = Event(),mainContainer : MainContainer = None):
        #get absolute path to config file from relative path
        self.__sensors = mainContainer.sensors
        self.__actuators = mainContainer.actuators
        self.__logics = mainContainer.logics
        self.__runRoutine = runRoutine
        print(self.__sensors)
        self.__dataHandler = DataHandler()
        self.__stopFlag = stopEvent
        self.__mainContainer = mainContainer
        self.__process = None

    def test(self):
        return True

    def setMainContainer(self,mainContainer:MainContainer):
        self.__mainContainer = mainContainer

    def run(self):
        #Diese Funktion ruft alle Logics auf, triggert die Sensoren und aktiviert darauf die Aktoren, welche in der Logik vermerkt sind
        #Ein Report wird erstellt und zurückgegeben, darüber welcher Sensor erfolgreich lief und welcher nicht

        #Alle Sensoren laufen lassen
        self.runAllSensors()

        #run all logics
        timeNow = time.time()
        logicReport =  []
        for logic in self.__logics:
            try:
                logic.run()
                logicReport.append({"name": logic.name, "success": True})
            except Exception as e:
                logicReport.append({"name": logic.name, "success": False, "error": e})

                    
        #if logger is set to info, the report will be printed without the error
        #if logger is set to debug, the report will be printed with the error
        if logger.level == logging.INFO:
            logger.info(f"#############Logic run finished [{time.time()}]########")
            for entry in logicReport:
                logger.info(f"Logic: {entry['name']}, Success: {entry['success']}")

        if logger.level == logging.DEBUG:
            logger.debug(f"#############Logic run finished [{time.time()}]########")
            for entry in logicReport:
                if "error" in entry:
                    logger.debug(f"Logic: {entry['name']}, Success: {entry['success']}, Error: {entry['error']}")
                else:
                    logger.debug(f"Logic: {entry['name']}, Success: {entry['success']}")

        # logger.debug("Logic run finished:", report)
        return logicReport
               
    def runAllSensors(self):
        logger.debug("run all Sensors:")
        
        for sensor in self.__sensors:
            #logger.debug(sensor)
            if(sensor.active):
                sensor.run()

    def runForever(self,stopFlag):
        while not stopFlag.is_set():
            self.run()
            time.sleep(self.__intervall)

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
        if(self.__process is None):
            return False
        return self.__process.is_alive()

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.runForever()
    # scheduler.run()
    
