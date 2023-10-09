import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging
from datetime import datetime, timedelta
import time
from Utils import tools

class TimedSwitchController(Controller):

    def getConfigDescription(self):
        desc = {
            "onTime": {"type": str, "desc": "Zeit, wie lange der Controller True zurück geben soll. Format: 'HH:MM:SS'"},
            "offTime": {"type": str, "desc": "Zeit, wie lange der Controller False zurück geben soll. Format: 'HH:MM:SS'"}
        }
        return desc

    def __init__(self, config: dict = {"onTime": "00:01:00", "offTime": "00:01:30"}):
        super().__init__(mask=[],config=config)
        try:
            self.onTimespanStr = config["onTime"]
            self.offTimespanStr = config["offTime"]
            
            self.onTimeDelta = tools.castDeltatimeFromString(self.onTimespanStr)
            self.offTimeDelta = tools.castDeltatimeFromString(self.offTimespanStr)

            self.onTime = datetime.now()
            self.offTime = self.onTime + self.onTimeDelta
            self.isOn = True
        except Exception as e:
            logging.error("TimerController: Fehler beim parsen der Zeitangabe")
            logging.error(e)
            raise ValueError("TimerController: Fehler beim parsen der Zeitangabe")

    def run(self, inputData: dict) -> bool:
        try:
            if self.isOn:
                if datetime.now() < self.offTime:
                    return super().safeAndReturn(True)
                else:
                    self.isOn = False
                    self.onTime = self.offTime + self.offTimeDelta
                    return super().safeAndReturn(False)
            else:
                if datetime.now() < self.onTime:
                    return super().safeAndReturn(False)
                else:
                    self.isOn = True
                    self.offTime = self.onTime + self.onTimeDelta
                    return super().safeAndReturn(True)
        except Exception as e:
            logging.error("TimerController: Fehler beim Ausführen des Controllers")
            logging.error(e)
            return super().safeAndReturn(False)

    def getNextScheduleTime(self):
        if(self.isOn):
            return self.offTime
        else:
            return self.onTime

# Beispiel für die Verwendung des TimerControllers
if __name__ == "__main__":
    timer_controller = TimerController({"onTime": "00:00:02", "offTime": "00:00:10"})
    while True:
        result = timer_controller.run({})
        print(result)
        time.sleep(1)
