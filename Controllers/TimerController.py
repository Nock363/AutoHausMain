import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging
from datetime import datetime

class TimerController(BaseBlock):


    def getConfigDescription(self):
        desc: {
            "startTime":{"type":str,"desc":"Uhrzeit wann getriggert werden soll. Format: 'HH:MM:SS'"},
            "runTime":{"type":str,"desc":"Wie lange soll der Timer laufen. Format: 'HH:MM:SS'"}
        }
        return desc


    def __init__(self,config:dict = {"startTime":"12:00:00","runTime":"00:01:00"}):
        super().__init__([])
        try:
            self.__startTime = datetime.strptime(config["startTime"],"%H:%M:%S")
            self.__runtime = datetime.strptime(config["runTime"],"%H:%M:%S")
            
            #konvertiere startTime zu einem timestamp
            self.__startTimeStamp = self.__startTime.timestamp()
            self.__endTimeStamp = self.__startTimeStamp + self.__runtime.timestamp()

        except Exception as e:
            logging.error("TimerController: Fehler beim parsen der Zeitangabe")
            logging.error(e)
            raise ValueError("TimerController: Fehler beim parsen der Zeitangabe")



    def run(self,inputData:dict) -> bool:
        
        time = datetime.now().timestamp()

        if(time >= self.__startTimeStamp and time <= self.__endTimeStamp):
            return super().safeAndReturn(True)

        return super().safeAndReturn(False)    
