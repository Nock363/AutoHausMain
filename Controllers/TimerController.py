import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging
from datetime import datetime, timedelta

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
            startTime = datetime.strptime(config["startTime"], '%H:%M:%S')
            now = datetime.now()
            today = datetime.today()


            self.__startTime = datetime.combine(today, startTime.time())
            if self.__startTime < now:
                self.__startTime += timedelta(days=1)

            
            self.__runTime = timedelta(seconds=int(config["runTime"][-2:]), minutes=int(config["runTime"][-5:-3]), hours=int(config["runTime"][:-6]))
            self.__endTime = self.__startTime + self.__runTime

        except Exception as e:
            logging.error("TimerController: Fehler beim parsen der Zeitangabe")
            logging.error(e)
            raise ValueError("TimerController: Fehler beim parsen der Zeitangabe")



    def run(self,inputData:dict) -> bool:
        
        now = datetime.now()
        if self.__startTime <= now <= self.__endTime:
            return super().safeAndReturn(True)
        elif now > self.__endTime:
            self.__startTime += timedelta(days=1)
            self.__endTime += timedelta(days=1)
            return super().safeAndReturn(False)
        else:
            return super().safeAndReturn(False)

        
        
            return super().safeAndReturn(True)

        return super().safeAndReturn(False)    
