# import sys
# sys.path.insert(0, 'Handler/')
# sys.path.insert(0, 'Sensoren/')
from dataclasses import dataclass
from Handler.DatabaseHandlers import MongoHandler
#from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
import Sensoren

# import sys, inspect
# clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
#print(clsmembers)

# from DatabaseHandlers import MongoHandler
# from Sensor import Sensor

# print(Sensoren)

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
        #print(list(sensorsConfig))
        for entry in sensorsConfig:
            
            objClass = self.importSensor(entry["class"])
            obj = objClass(pinID = entry["pinID"])
        
            conf = SensorConfig(objClass,obj,entry["intervall"])
            print(f"config: {conf}")
            self.__sensoren.append(conf)

        print(self.__sensoren)
        # aht20 = self.importSensor("HudTemp_AHT20")
        # print(type(aht20))
        # test = aht20(pinID = 7)

    def runAllSensors(self):
        for sensor in self.__sensoren:
            print(sensor.sensor.run())

    def importSensor(self,sensorName:str):
        #moduleString = "Sensoren.HudTemp_AHT20"
        moduleString = f"Sensoren.{sensorName}"
        module = __import__(moduleString)
        # print("module:",module)
        return getattr(module,"HudTemp_AHT20")


scheduler = Scheduler()
scheduler.runAllSensors()