# import sys
# sys.path.insert(0, 'Handler/')
# sys.path.insert(0, 'Sensoren/')
from dataclasses import dataclass
from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Handler.DatabaseHandlers import MongoHandler
import Sensoren
import time
import logging
logging.basicConfig(filename="schedulderLog.log",format=format, level=logging.INFO,datefmt="%H:%M:%S")
logger = logging.getLogger('simple_example')
logger.setLevel(logging.WARNING)
# import sys, inspect
# clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
#logger.debug(clsmembers)

# from DatabaseHandlers import MongoHandler
# from Sensor import Sensor

# logger.debug(Sensoren)

@dataclass
class SensorConfig:
    sensorClass: type
    sensor: Sensoren.Sensor
    intervall: float





class Scheduler():

    __sensoren : list[SensorConfig]
    __mongoHandler : MongoHandler

    def __init__(self):
        self.__sensoren = []
        self.__mongoHandler = MongoHandler()
        sensorsConfig = self.__mongoHandler.getSensors()
        #logger.debug(list(sensorsConfig))
        for entry in sensorsConfig:
            
            logger.debug(f"+++++++++++++{entry}+++++++++++++")
            objClass = self.importSensor(entry["class"])
            obj = objClass(pinID = entry["pinID"])
        
            conf = SensorConfig(objClass,obj,entry["intervall"])
            logger.debug(f"config: {conf}")
            self.__sensoren.append(conf)

        logger.debug(self.__sensoren)
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