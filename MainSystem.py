from Logics.BaseLogic import BaseLogic
import Sensoren
import Actuators
import Controllers
from Handler.DataHandler import DataHandler
import os
import traceback
from multiprocessing import Queue, Process, Semaphore, Event
import time
import threading
import importlib.util
import sys

import logging
logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('scheduler')
logger.setLevel(logging.DEBUG)

class MainSystem():


    __sensors : list[Sensoren.Sensor]
    __actuators : list[Actuators.Actuator]
    __logics : list[BaseLogic]
    __dataHandler : DataHandler


    #logging from broken objects
    __brokenSensors : list[dict]
    __brokenActuators : list[dict]
    __brokenLogics : list[dict]

    __runRoutine : bool
    __stopFlag : Event
    __process : Process

    __samplingRate = 5 #Abtastrate der Sensoren und der Logik. Logik kann auch seltener laufen aber NICHT schneller als die sampling Rate

    def __init__(self,reqQueue,respQueue, stopEvent = Event()):
        

        #mögliche statusse:
        #boot = system bootet und ist noch nicht bereit
        #ready = system ist initialisiert, aber nicht am laufen
        #running = system ist initialisiert und scheduler läuft
        #broken = system war nicht in der lage korrekt hochzufahren.
        #setup = system intialisiert/startet subsysteme.(Wie boot nur triggerbar durch z.B. starten von neuen Sensoren über die Laufzeit.)

        self.__status = "boot"
        self.__dataHandler = DataHandler()
        self.__sensorClasses = self.__getAvailableClasses("Sensoren",["Sensor.py"])
        self.__actuatorClasses = self.__getAvailableClasses("Actuators",["Actuator.py"])

        

        try:
            self.loadSensors()
            self.loadActuators()
            self.loadLogics()
            self.__printBrokenLogs()
        except Exception as e:
            logger.error(f"Fehler beim laden von Sensoren, Aktoren oder Logik: {e}")
            self.__status = "broken"


        self.__reqQueue = reqQueue
        self.__respQueue = respQueue

        self.__stopFlag = stopEvent
        self.__process = None

        try:
            #start queue worker
            self.__multiProcessInterfaceThread = threading.Thread(target=self.__startQueueWork)
            self.__multiProcessInterfaceThread.start()
        except Exception as e:
            logger.error(f"Fehler beim starten des Queue Workers: {e}")
            self.__status = "broken"

        if(self.__status != "broken"):
            self.__status = "ready"

        logger.debug(f"MainSystem-Initialisierung abgeschlossen. Status: {self.__status}")


    @property
    def status(self):
        return self.__status

    @property
    def sensors(self):
        return self.__sensors

    @property
    def actuators(self):
        return self.__actuators

    @property
    def logics(self):
        return self.__logics


    def __getActuatorClassesAsDict(self):
        acturatorDescriptions = []
        for actuatorClass in self.__actuatorClasses:
            #get name of Class as Clear name
            actuatorName = actuatorClass.__name__
            configDesc = actuatorClass.getConfigDesc()
            actuator = {"name":actuatorName,"configDesc":configDesc,"actuator":actuatorClass}
            acturatorDescriptions.append(actuator)
        return acturatorDescriptions


    def __getAvailableClasses(self,folder_path:str, blacklist:list = []):
        
        classes = []
        for filename in os.listdir(folder_path):
            if not filename.endswith('.py') or filename.startswith('_'):
                continue

            #if filename is in blacklist, skip it
            if filename in blacklist:
                continue

            sensorName = filename[:-3]
            moduleString = f"{folder_path}.{sensorName}"
            try:
                module = __import__(moduleString)
                attr = getattr(module,sensorName)
                classes.append(getattr(attr,sensorName))
            except Exception as e:
                logger.error(f"Error while loading module {moduleString}: {e}")
        return classes



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
        sensorConfig = self.__dataHandler.getSensors(onlyActive=False)
        #clear broken sensors
        self.__brokenSensors = []
        for entry in sensorConfig:
            try:
                sensorClass = self.__importSensor(entry["class"])
                sensor = sensorClass(
                    name=entry["name"],
                    collection = entry["collection"],
                    config = entry["config"],
                    description = entry["description"],
                    active=entry["active"]
                )
                self.__sensors.append(sensor)
            except Exception as e:
                full_traceback = traceback.format_exc()
                short_traceback = traceback.extract_tb(sys.exc_info()[2])
                brokenSensor = {
                    "sensor": entry,
                    "error": str(e),
                    "full_traceback": full_traceback,
                    "short_traceback": short_traceback
                }
                self.__brokenSensors.append(brokenSensor)

        #if broken sensors are found, print them
        # print("Broken Sensors:")
        # for sensor in self.__brokenSensors:
        #     logging.debug(sensor)
        logger.debug(self.__sensors)

    def loadActuators(self):
        self.__actuators = []
        actuatorsConfig = self.__dataHandler.getActuators(onlyActive=False)
        self.__brokenActuators = []
        for entry in actuatorsConfig:
            try:    
                actuatorClass = self.__importActuator(entry["type"])
                actuator = actuatorClass(
                    name=entry["name"],
                    collection = entry["collection"],
                    config = entry["config"],
                    active = entry["active"]
                )
                self.__actuators.append(actuator)
            except Exception as e:
                brokenActuator = {"actuator":entry,"error":e}
                self.__brokenActuators.append(brokenActuator)

        logger.debug(self.__actuators)

        # print("Broken Actuators:")
        # for actuator in self.__brokenActuators:
        #     logging.debug(sensor)

    def loadLogics(self):
        self.__logics = []
        logicConfig = self.__dataHandler.getLogics(onlyActive=False)
        self.__brokenLogics = []
        for entry in logicConfig:

            try:
                runnable = True #Gibt an ob die Logik ausgeführt werden kann. falls inputs oder outputs deaktiviert sind kann die Logik nicht ausgeführt werden.
                controllerConfig = entry["controller"]
                controllerClass = self.__importController(controllerConfig["controller"])
                controller = controllerClass(controllerConfig["config"])
                inputs = entry["inputs"]
                for input in inputs:
                    input["object"] = self.getSensor(input["sensor"])
                    if(input["object"] == None):
                        raise Exception(f"Sensor {input['sensor']} not found")
                    if(not input["object"].active):
                        runnable = False
                        logger.debug(f"Sensor {input['sensor']} ist nicht aktiviert. Logik {entry['name']} wird deswegen deaktiviert.")

                outputs = entry["outputs"]
                for output in outputs:
                    output["object"] = self.getActuator(output["actuator"])
                    if(output["object"] == None):
                        raise Exception(f"Actuator {output['actuator']} not found")
                    if(not output["object"].active):
                        runnable = False
                        logger.debug(f"Aktor {output['sensor']} ist nicht aktiviert. Logik {entry['name']} wird deswegen deaktiviert.")        

                if(not runnable):
                    active = False
                else:
                    active = entry["active"]

                logic = BaseLogic(#TODO: beschreibung integrieren.
                    name= entry["name"],
                    controller= controller,
                    inputs= inputs,
                    outputs= outputs,
                    active= active
                )
                self.__logics.append(logic)
                
            except Exception as e:
                brokenLogic = {"logic":entry,"error":e}
                self.__brokenLogics.append(brokenLogic)

        logging.debug(self.__logics)

        # print("Broken Sensors:")
        # for logic in self.__brokenLogics:
        #     logging.debug(logic)

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

    def __printBrokenLogs(self):
        logger.info("______Broken Sensors______")
        for sensor in self.__brokenSensors:
            infoString = f"Sensor: {sensor['sensor']['name']} Error: {sensor['error']}\n"
            for t in sensor["short_traceback"]:
                infoString = infoString + f"\t {t.filename} ({t.lineno})\n"


            
            logger.info(infoString)
            
            
        logger.info("______Broken Actuators______")
        for actuator in self.__brokenActuators:
            logger.info(f"Actuator: {actuator['actuator']['name']} Error: {actuator['error']}")

        logger.info("______Broken Logics______")
        for logic in self.__brokenLogics:
            logger.info(f"Logic: {logic['logic']['name']} Error: {logic['error']}")

    def __getSensorsWithData(self,length):
        sensorsWithData = []
        for sensor in self.__sensors:
            sensorConfig = sensor.getInfos()
            sensorConfig["data"] = sensor.getHistory(length)
            sensorsWithData.append(sensorConfig)
        return sensorsWithData

    def __getActuatorsWithData(self,length):
        actuatorsWithData = []
        for actuator in self.__actuators:
            actuatorConfig = actuator.getInfos()
            actuatorConfig["data"] = [] #TODO liefern von historischen Daten für Aktoren implementieren
            actuatorsWithData.append(actuatorConfig)
        return actuatorsWithData

    def __startQueueWork(self):
        counter = 1
        while True:
            request = self.__reqQueue.get()
            if request["command"] == "sensorHistory":
                sensor = request["sensor"]
                length = request["length"]
                sensor_obj = self.getSensor(sensor)
                self.__respQueue.put(sensor_obj.getHistory(length))
            elif request["command"] == "sensorsWithData":
                length = request["length"]
                #create list of sensors with data
                self.__respQueue.put(self.____getSensorsWithData(length))
            elif request["command"] == "systemInfo":
                sensors = self.__getSensorsWithData(1)
                actuators = self.__getActuatorsWithData(0)
                logics = []
                for logic in self.__logics:
                    logics.append(logic.getInfos())
                systemInfo = {
                    "status": self.__status,
                    "sensors": sensors,
                    "actuators": actuators,
                    "logics": logics
                }
                self.__respQueue.put(systemInfo)

    def run(self):
        #Diese Funktion ruft alle Logics auf, triggert die Sensoren und aktiviert darauf die Aktoren, welche in der Logik vermerkt sind
        #Ein Report wird erstellt und zurückgegeben, darüber welcher Sensor erfolgreich lief und welcher nicht
        dataHandler = self.__dataHandler
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
            time.sleep(self.__samplingRate)

    def runNtimes(self, N = 1000):
        for i in range(0,N):
            self.run()
            time.sleep(self.__samplingRate)

    def startProcess(self):
        self.__stopFlag = threading.Event()
        self.__thread = threading.Thread(target=self.runForever, args=(self.__stopFlag,))
        self.__thread.start()
        logger.info("Scheduler Thread gestartet")

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