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
from datetime import datetime, timedelta
from Utils import tools
import json
import copy
import logging

class MainSystem():

    __sensors : list[Sensoren.Sensor]
    __actuators : list[Actuators.Actuator]
    __logics : list[BaseLogic]
    __dataHandler : DataHandler
    

    #logging from broken objects
    __brokenSensors : list[dict]
    __brokenActuators : list[dict]
    __brokenLogics : list[dict]

    __lonelySensors : list[Sensoren.Sensor]

    __stopFlag : Event

    __defaultSamplingRate = 10 #Abtastrate der Sensoren und der Logik. Logik kann auch seltener laufen aber NICHT schneller als die sampling Rate
    __samplingResolution = 1 #Minimale Auflösung. Alle samßpling rates müssen teilbar sein durch die sampling resolution
    __dynamicSchedule = [] #Liste mit dynamisch erzeugten Intervallen. Diese werden in der run funktion berücksichtigt und überschreiben die fixe sampling rate, falls erwünscht


    def __init__(self,reqChannel,respChannel, stopEvent = Event()):
        
        # Konfiguriere den Logger
        # logging.basicConfig(filename="MainSystemLog.log", format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG)
        # Holen Sie sich den Logger
        self.logger = logging.getLogger()

        #mögliche statusse:
        #boot = system bootet und ist noch nicht bereit
        #ready = system ist initialisiert, aber nicht am laufen
        #running = system ist initialisiert und scheduler läuft
        #broken = system war nicht in der lage korrekt hochzufahren.
        #setup = system intialisiert/startet subsysteme.(Wie boot nur triggerbar durch z.B. starten von neuen Sensoren über die Laufzeit.)

        self.__status = "boot"
        self.__info = "System bootet!"
        self.__dataHandler = DataHandler()

        
        try:
            config = self.__dataHandler.getMainConfig()
            self.__defaultSamplingRate = config["sampleRate"]
            self.__samplingResolution = config["samplingResolution"]            


        except Exception as e:
            self.logger.error(f"Fehler beim laden der MainConfig(nutze nun default): {e}")
            self.__status = "broken"
        self.logger.info(f"Setze Sampling rate auf: {self.__defaultSamplingRate}")
        # self.__sensorClasses = self.__getAvailableClasses("Sensoren",["Sensor.py"])
        # self.__actuatorClasses = self.__getAvailableClasses("Actuators",["Actuator.py"])

        self.__reqChannel = reqChannel
        self.__respChannel = respChannel

        self.__stopFlag = stopEvent

        try:
            #start queue worker
            self.__multiProcessInterfaceThread = threading.Thread(target=self.__startQueueWork)
            self.__multiProcessInterfaceThread.start()
        except Exception as e:
            self.logger.error(f"Fehler beim starten des Queue Workers: {e}")
            self.__status = "broken"
            self.__info = f"System ist defekt, ba der Queue Worker einen Fehler hat: {e}"

        if(self.__status != "broken"):
            self.__status = "ready"
            self.__info = "System ist einsatzbereit!"

        self.logger.info(f"MainSystem-Initialisierung abgeschlossen. Status: {self.__status}")


    def setup(self):
        self.logger.info("Starte setup Prozess für MainSystem")
        self.__status = "setup"
        self.__info = "System befindet sich im Setup!"
        self.__lonelySensors = []

        try:
            self.__loadAllSensors()
            self.__loadActuators()
            self.__loadLogics()
            self.__printBrokenLogs()
            self.__status = "ready"
            self.__info = "System ist einsatzbereit!"
        except Exception as e:
            self.logger.error(f"Fehler beim laden von Sensoren, Aktoren oder Logik: {e}")
            self.__status = "broken"
            self.__info = f"System ist defekt, da beim laden von Sensoren, Aktoren oder Logik ein Fehler aufgetreten ist: {e}"

        self.logger.info("Starte setup Prozess für MainSystem abgeschlossen")
        



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
                self.logger.error(f"Error while loading module {moduleString}: {e}")
        return classes

    def systemInfo(self):

        if(self.__status == "broken"):
            return {"status":"broken","info":self.__info}

        if(self.__status != "setup"):
            sensors = self.__getSensorsWithData(1)
            actuators = self.__getActuatorsWithData(0)

            #remove tracebacks from broken sensors without modifiging the original list
            brokenSensors = []
            for sensor in self.__brokenSensors:
                brokenSensors.append(sensor.copy())
            for sensor in brokenSensors:
                sensor.pop("full_traceback")
                sensor.pop("short_traceback")

            brokenActuators = []
            for actuator in self.__brokenActuators:
                brokenActuators.append(actuator.copy())
            for actuator in brokenActuators:
                actuator.pop("full_traceback")
                actuator.pop("short_traceback")

            brokenLogics = []
            for logic in self.__brokenLogics:
                brokenLogics.append(logic.copy())
            for logic in brokenLogics:
                logic.pop("full_traceback")
                logic.pop("short_traceback")


            logics = []
            for logic in self.__logics:
                logics.append(logic.getInfos())
            systemInfo = {
                "status": self.__status,
                "sensors": sensors,
                "actuators": actuators,
                "logics": logics,
                "brokenSensors": brokenSensors,
                "brokenActuators": brokenActuators,
                "brokenLogics": brokenLogics,
                "info": self.__info,
            }
            # tools.checkDictForJsonSerialization(systemInfo)
            return systemInfo
        else:
            return {"status":"setup","info":self.__info}

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


    def __loadSensor(self, config:dict):

        #search for sensor in self.__sensors
        for sensor in self.__sensors:
            if sensor.name == config["name"]:
                self.logger.error(f"Sensor {config['name']} bereits geladen")
                return

        oldInfo  = self.__info
        success = False

        try:
                self.__info = f"Konfiguriere Sensor {config['name']}"
                sensorClass = self.__importSensor(config["class"])
                sensor = sensorClass(
                    name=config["name"],
                    collection = config["collection"],
                    config = config["config"],
                    description = config["description"],
                    active=config["active"]
                )
                self.__sensors.append(sensor)
                success = True
        except Exception as e:
            full_traceback = traceback.format_exc()
            short_traceback = traceback.extract_tb(sys.exc_info()[2])
            brokenSensor = {
                "sensor": config,
                "error": str(e),
                "full_traceback": full_traceback,
                "short_traceback": short_traceback
            }
            self.__brokenSensors.append(brokenSensor)

        self.__info = oldInfo
        return 
        

    def __loadAllSensors(self):
        self.__sensors = []
        sensorConfig = self.__dataHandler.getSensors(onlyActive=False)
        #clear broken sensors
        self.__brokenSensors = []
        for entry in sensorConfig:
            self.__loadSensor(entry)

        self.logger.debug(self.__sensors)
        self.__info = "Konfiguration der Sensoren abgeschlossen"

    def __loadActuators(self):

        self.__info = "Konfiguriere Aktoren"
        self.__actuators = []
        actuatorsConfig = self.__dataHandler.getActuators(onlyActive=False)
        self.__brokenActuators = []
        for entry in actuatorsConfig:
            try:    
                self.__info = f"Konfiguriere Aktor {entry['name']}"
                actuatorClass = self.__importActuator(entry["type"])
                actuator = actuatorClass(
                    name=entry["name"],
                    collection = entry["collection"],
                    config = entry["config"],
                    active = entry["active"]
                )
                self.__actuators.append(actuator)
            except Exception as e:
                full_traceback = traceback.format_exc()
                short_traceback = traceback.extract_tb(sys.exc_info()[2])
                brokenActuator = {
                    "actuator":entry,
                    "error":str(e),
                    "full_traceback": full_traceback,
                    "short_traceback": short_traceback
                }
                self.__brokenActuators.append(brokenActuator)

        self.logger.debug(self.__actuators)
        self.__info = "Konfiguration der Aktoren abgeschlossen"

        # print("Broken Actuators:")
        # for actuator in self.__brokenActuators:
        #     logging.debug(sensor)

    def __loadLogics(self):

        self.__info = "Konfiguriere Logik"
        self.__logics = []
        logicConfig = self.__dataHandler.getLogics(onlyActive=False)
        self.__brokenLogics = []
        self.__lonelySensors = []
        #fill them with all sensors
        usedSensors = []

        for entry in logicConfig:

            oldEntry = copy.deepcopy(entry)
            try:

                self.__info = f"Konfiguriere Logik {entry['name']}"
                runnable = True #Gibt an ob die Logik ausgeführt werden kann. falls inputs oder outputs deaktiviert sind kann die Logik nicht ausgeführt werden.
                controllerConfig = entry["controller"]
                controllerClass = self.__importController(controllerConfig["controller"])
                controller = controllerClass(controllerConfig["config"])
                inputs = entry["inputs"]
                for input in inputs:
                    input["object"] = self.getSensor(input["sensor"])
                    #remove sensor from lonely sensors
                    if(input["object"] == None):
                        raise Exception(f"Sensor {input['sensor']} not found")
                    if(not input["object"].active):
                        runnable = False
                        self.logger.debug(f"Sensor {input['sensor']} ist nicht aktiviert. Logik {entry['name']} wird deswegen deaktiviert.")
                    else:
                        usedSensors.append(input["object"])


                outputs = entry["outputs"]
                for output in outputs:
                    output["object"] = self.getActuator(output["actuator"])
                    if(output["object"] == None):
                        raise Exception(f"Actuator {output['actuator']} not found")
                    if(not output["object"].active):
                        runnable = False
                        self.logger.debug(f"Aktor {output['actuator']} ist nicht aktiviert. Logik {entry['name']} wird deswegen deaktiviert.")        

                if(not runnable):
                    active = False
                else:
                    active = entry["active"]

                logic = BaseLogic(#TODO: beschreibung integrieren.
                    name= entry["name"],
                    controller= controller,
                    inputs= inputs,
                    outputs= outputs,
                    active= active,
                    intervall=entry["intervall"]
                )
                self.__logics.append(logic)
                
            except Exception as e:
                full_traceback = traceback.format_exc()
                short_traceback = traceback.extract_tb(sys.exc_info()[2])
                brokenLogic = {
                    "logic":oldEntry,
                    "error":str(e),
                    "full_traceback": full_traceback,
                    "short_traceback": short_traceback
                }
                self.__brokenLogics.append(brokenLogic)

        #add every sensor that is not in usedSensors to lonelySensors
        for sensor in self.__sensors:
            if sensor not in usedSensors:
                self.__lonelySensors.append(sensor)

        self.__info = "Konfiguration der Logik abgeschlossen"
        self.logger.debug(self.__logics)

        # print("Broken Sensors:")
        # for logic in self.__brokenLogics:
        #     self.logger.debug(logic)

    def __importSensor(self,sensorName:str):
        #moduleString = "Sensoren.HudTemp_AHT20"
        moduleString = f"Sensoren.{sensorName}"
        module = __import__(moduleString)
        #self.logger.debug("module:",module)
        attr = getattr(module,sensorName)
        #self.logger.debug("attribute:",attr)
        return getattr(attr,sensorName)
    
    def __importActuator(self,actuatorName:str):
        moduleString = f"Actuators.{actuatorName}"
        module = __import__(moduleString)
        #self.logger.debug("module:",module)
        attr = getattr(module,actuatorName)
        #self.logger.debug("attribute:",attr)
        return getattr(attr,actuatorName)

    def __importController(self,controllerName:str):
        moduleString = f"Controllers.{controllerName}"
        module = __import__(moduleString)
        #self.logger.debug("module:",module)
        attr = getattr(module,controllerName)
        #self.logger.debug("attribute:",attr)
        return getattr(attr,controllerName)

    def __printBrokenLogs(self):
        
        logStringSensors = "BROKEN SENSORS\n"
        
        for sensor in self.__brokenSensors:
            infoString = f"Sensor: {sensor['sensor']['name']} Error: {sensor['error']}\n"
            
            if(self.logger.level == logging.DEBUG):
                for t in sensor["short_traceback"]:
                    infoString = infoString + f"\t {t.filename} ({t.lineno})\n"

            logStringSensors = logStringSensors + infoString
            
        self.logger.info(logStringSensors)

        logStringActuators = "BROKEN ACTUATORS\n"

        for actuator in self.__brokenActuators:
            infoString = f"Actuator: {actuator['actuator']['name']} Error: {actuator['error']}\n"

            if(self.logger.level == logging.DEBUG):
                for t in actuator["short_traceback"]:
                    infoString = infoString + f"\t {t.filename} ({t.lineno})\n"

            logStringActuators = logStringActuators + infoString

        self.logger.info(logStringActuators)
        
        
        logStringLogics = "BROKEN LOGICS\n"

        for logic in self.__brokenLogics:
            infoString = f"Logic: {logic['logic']['name']} Error: {logic['error']}"

            if(self.logger.level == logging.DEBUG):
                for t in logic["short_traceback"]:
                    infoString = infoString + f"\t {t.filename} ({t.lineno})\n"
            
            logStringLogics = logStringLogics + infoString

        self.logger.info(logStringLogics)

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
        while True:
            if len(self.__reqChannel) > 0:
                try:
                    requestPackage = self.__reqChannel.pop()
                    request = requestPackage["request"]
                    id = requestPackage["id"]
                    response = None

                    if request["command"] == "sensorHistory":
                        if(self.__status == "setup"):
                            response = {"errror":"System in Setup"}
                        else:
                            sensor = request["sensor"]
                            length = request["length"]
                            sensor_obj = self.getSensor(sensor)
                            response = sensor_obj.getHistory(length)

                    elif request["command"] == "actuatorHistory":
                        if(self.__status == "setup"):
                            response = {"errror":"System in Setup"}
                        else:
                            actuator = request["actuator"]
                            length = request["length"]
                            actuator_obj = self.getActuator(actuator)
                            response = actuator_obj.getHistory(length)

                    elif request["command"] == "sensorsWithData":
                        if(self.__status == "setup"):
                            response = {"errror":"System in Setup"}
                        else:
                            length = request["length"]
                            #create list of sensors with data
                            response = self.____getSensorsWithData(length)
                    elif request["command"] == "sensorHistoryByTimespan":
                        if(self.__status == "setup"):
                            response = {"errror":"System in Setup"}
                        else:
                            startTime = datetime.strptime(request["startTime"],"%Y-%m-%dT%H:%M")
                            endTime = datetime.strptime(request["endTime"],"%Y-%m-%dT%H:%M")
                            sensor = request["sensor"]
                            sensor_obj = self.getSensor(sensor)
                            response = sensor_obj.getHistoryByTimespan(startTime,endTime)
                    elif request["command"] == "systemInfo":
                        systemInfo = self.systemInfo()
                        response = systemInfo
                    elif request["command"] == "startBrokenSensor":
                        #get sensor name
                        sensorName = request["sensor"]
                        #start sensor
                        success = self.loadBrokenSensor(sensorName)
                        if(success):
                            response = {"success": True}
                        else:
                            #add error to response
                            response = {"success": False, "error": "Sensor not found"}
                            for sensor in self.__brokenSensors:
                                if sensor["sensor"]["name"] == sensorName:
                                    response = {"success": False, "error": sensor["error"]}
                                    break
                    elif request["command"] == "startScheduler":
                        success = self.startScheduler()
                        response = {"success": success}
                    elif request["command"] == "stopScheduler":
                        success = self.stopScheduler()
                        response = {"success": success}
                    elif request["command"] == "schedulerInfo":
                        response = {"status":self.__status}
                    if(response == None):
                        self.logger.error(f"Request {request} gesendet über den multiprocessing-kanal konnte nicht bearbeitet werden.")
                        continue
                except Exception as e:
                    self.logger.error(f"Fehler beim bearbeiten des Requests {request}: {e}")
                    response = {"error":"der Queue Worker konnte den Request nicht bearbeiten."}

                self.__respChannel.append({"id":id,"response":response})

    def loadBrokenSensor(self,sensorName,overwriteActive = True):
        
        if(self.__status == "running"):
            self.stopScheduler()
            schedulerWasRunning = True

        #when system not ready return false and log error
        if(self.__status != "ready"):
            self.logger.error(f"System ist nicht bereit. Status: {self.__status}")
            return False

        entry = None
        
        schedulerWasRunning = False
        for s in self.__brokenSensors:
            if s["sensor"]["name"] == sensorName:
                entry = s["sensor"]
                self.__brokenSensors.remove(s)
                break
        
        if(entry != None):
           success = self.__loadSensor(entry)
        else:
            success = False
            self.logger.error(f"Sensor {sensorName} ist nicht als defekter Sensor gelistet.")
            
        self.startScheduler()
        return success


        if(sensor == None):
            self.logger.error(f"Sensor {sensorName} ist nicht als defekter Sensor gelistet.")
            return False
        
        stopScheduler()
        self.status = "setup"


        return True

    def runClassic(self):
        #Diese Funktion ruft alle Logics auf, triggert die Sensoren und aktiviert darauf die Aktoren, welche in der Logik vermerkt sind
        #Ein Report wird erstellt und zurückgegeben, darüber welcher Sensor erfolgreich lief und welcher nicht

        #ignoreDynamicIntervalls = True -> Ignoriere dynamisch erzeugte Intervalle und führe alles nach der fixxen Samplingrate aus.

        #if system is not running, return false
        if(self.__status != "running"):
            self.logger.info(f"System ist nicht am laufen. Status: {self.__status}")
            return False


        self.logger.info("starte Scheduler-Run")

        #Alle Sensoren laufen aus lonelySensors laufen lassen
        self.runAllSensors(self.__lonelySensors)
 
        #run all logics
        timeNow = time.time()
        logicReport =  []
        for logic in self.__logics:
            if(logic.active):
                try:
                    logic.run()
                    logicReport.append({"name": logic.name, "success": True})
                    if(not ignoreDynamicIntervalls):
                        self.addToDynamicSchedule(schedulerTime=logic.getNextScheduleTime(timeNow),scheduleType=logic.name)

                except Exception as e:
                    self.logger.error(f"Logic {logic.name} failed: {str(e)}")
                    logicReport.append({"name": logic.name, "success": False, "error": str(e)})

        logicReportStr = ""
        #add logic reports to log like : [ERROR] or [OK] followed by logic name an error message if there is one
        for report in logicReport:
            if(report["success"]):
                logicReportStr = logicReportStr + f"OK: {report['name']}\n"
            else:
                logicReportStr = logicReportStr + f"BROKEN: {report['name']} - {report['error']}\n"
        
        self.logger.info(f"Logik-Report:\n{logicReportStr}")
        
        return logicReport
               
    def runAllSensors(self,sensors:list[Sensoren.Sensor]):
        
        failedSensors = []
        for sensor in sensors:
            if(sensor.active):
                try:
                    sensor.run()
                except Exception as e:
                    
                    full_traceback = traceback.format_exc()
                    short_traceback = traceback.extract_tb(sys.exc_info()[2])
                
                    self.logger.error(f"Fehler beim ausführen des Sensors {sensor.name}: {e}")
                    self.logger.debug(full_traceback)
                    failedSensors.append({
                        "sensor":sensor.getConfig(),
                        "error":str(e),
                        "full_traceback":full_traceback,
                        "short_traceback":short_traceback
                    })

        #remove all failed sensors from self.__sensors and add them to self.__brokenSensors
        for failedSensor in failedSensors:
            for sensor in sensors:
                if sensor.name == failedSensor["sensor"]["name"]:
                    sensors.remove(sensor)
                    break
            self.__brokenSensors.append(failedSensor)

    def runLogic(self,logic):
        try:
            logic.run()
        except Exception as e:
            self.logger.error(f"Logic {logic.name} failed: {str(e)}")
            
        return logic.getNextScheduleTime()


    def runForever(self, stopFlag,ignoreDynamicIntervalls = False):
        
        #init dynamic schedule with default and every logic with nextSamplingRate==datetime.now()
        now = datetime.now()

        # self.addToDynamicSchedule(now,"default")

        avgWaitTime={}

        for logic in self.__logics:
            self.addToDynamicSchedule(now,logic.name)

        nextSchedule = self.__dynamicSchedule.pop(0)

        while True:
            
            if(nextSchedule["time"] <= datetime.now()):
                print(f"run Schedule: {nextSchedule['type']}")
                if(nextSchedule["type"] == "default"):
                    self.runAllSensors(self.__sensors)
                    nextSampleTime = datetime.now() + timedelta(seconds=self.__defaultSamplingRate)
                    self.addToDynamicSchedule(nextSampleTime,"default")
                else:
                    #search for logic with name == nextSchedule
                    for logic in self.__logics:
                        if(logic.name == nextSchedule["type"]):
                            nextSampleTime = self.runLogic(logic)
                            self.addToDynamicSchedule(nextSampleTime,logic.name)

                            break

            self.printDynamicSchedule()
            sleepTime = self.getTimeUntilNextSchedule()
            if(sleepTime == None):
                sleepTime = 0
            else:
                nextSchedule = self.__dynamicSchedule.pop(0)
                if(sleepTime < 0):
                    print(f"sleepTime: {sleepTime} < 0!")
                    sleepTime = 0
                    

            

            print("runForever.sleepTime: ",sleepTime)

            

            if stopFlag.wait(sleepTime):
                print("stopFlag triggerd")
                break

        self.__status = "ready"

    def runNtimes(self, N = 1000):
        for i in range(0,N):
            self.runClassic()
            time.sleep(self.__defaultSamplingRate)

    def startScheduler(self):
        try:
            if(self.__status != "ready"):
                self.logger.error(f"System ist nicht bereit. Status: {self.__status}")
                return False
            self.__status = "running"
            self.__stopFlag = threading.Event()
            self.__thread = threading.Thread(target=self.runForever, args=(self.__stopFlag,))
            self.__thread.start()
            self.logger.info("Scheduler Thread gestartet")
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim starten des Scheduler Threads: {e}")
            return False

    def stopScheduler(self):
        #stop scheduler and return True when success. also log to terminal
        if(self.__stopFlag.is_set()):
            self.logger.info("Scheduler Thread ist bereits gestoppt")
            return False
        else:
            self.__stopFlag.set()
            self.__thread.join(10)
            self.logger.info("Scheduler Thread gestoppt")
            return True

    def statusScheduler(self):
        return self.__status

    def schedulerIsRunning(self):
        if(self.__stopFlag.is_set()):
            return False
        else:
            return True
        
    def addToDynamicSchedule(self,scheduleTime:datetime,scheduleType:str):
        #append to schedule so that it keeps an ascending order
        schedule = {"type":scheduleType,"time":scheduleTime}
        if(len(self.__dynamicSchedule) == 0):
            self.__dynamicSchedule.append(schedule)
            return

        for (i,s) in enumerate(self.__dynamicSchedule):
            if(scheduleTime <= s["time"]):
                self.__dynamicSchedule.insert(i,schedule)
                return
        #Kein schedule punkt größer als die neue Zeit.
        self.__dynamicSchedule.append(schedule)


    def getTimeUntilNextSchedule(self):
        if(len(self.__dynamicSchedule) == 0):
            return None
        else:
            return (self.__dynamicSchedule[0]["time"] - datetime.now()).total_seconds()

    def printDynamicSchedule(self):
        print("dynamicSchedule:")
        #print the dynamic schedule plus the time left to the schedule
        for s in self.__dynamicSchedule:
            print(f"{s['type']}: {s['time']} ({(s['time'] - datetime.now()).total_seconds()} seconds)")