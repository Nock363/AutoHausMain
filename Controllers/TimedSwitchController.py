import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging
from datetime import datetime, timedelta
import time

class TimedSwitchController(BaseBlock):

    def getConfigDescription(self):
        desc = {
            "onTime": {"type": str, "desc": "Zeit, wie lange der Controller True zurück geben soll. Format: 'HH:MM:SS'"},
            "offTime": {"type": str, "desc": "Zeit, wie lange der Controller False zurück geben soll. Format: 'HH:MM:SS'"}
        }
        return desc

    def __init__(self, config: dict = {"onTime": "00:01:00", "offTime": "00:01:30"}):
        super().__init__([])
        try:
            self.onTimespanStr = config["onTime"]
            self.offTimespanStr = config["offTime"]
            self.onTime = datetime.now()
            self.offTime = self.onTime + timedelta(
                seconds=int(self.onTimespanStr[-2:]), minutes=int(self.onTimespanStr[-5:-3]), hours=int(self.onTimespanStr[:-6]))
            self.isOne = True
        except Exception as e:
            logging.error("TimerController: Fehler beim parsen der Zeitangabe")
            logging.error(e)
            raise ValueError("TimerController: Fehler beim parsen der Zeitangabe")

    def run(self, inputData: dict) -> bool:
        try:
            if self.isOne:
                if datetime.now() < self.offTime:
                    return super().safeAndReturn(True)
                else:
                    self.isOne = False
                    self.onTime = self.offTime + timedelta(
                        seconds=int(self.offTimespanStr[-2:]), minutes=int(self.offTimespanStr[-5:-3]), hours=int(self.offTimespanStr[:-6]))
                    return super().safeAndReturn(False)
            else:
                if datetime.now() < self.onTime:
                    return super().safeAndReturn(False)
                else:
                    self.isOne = True
                    self.offTime = self.onTime + timedelta(
                        seconds=int(self.onTimespanStr[-2:]), minutes=int(self.onTimespanStr[-5:-3]), hours=int(self.onTimespanStr[:-6]))
                    return super().safeAndReturn(True)
        except Exception as e:
            logging.error("TimerController: Fehler beim Ausführen des Controllers")
            logging.error(e)
            return super().safeAndReturn(False)

# Beispiel für die Verwendung des TimerControllers
if __name__ == "__main__":
    timer_controller = TimerController({"onTime": "00:00:02", "offTime": "00:00:10"})
    while True:
        result = timer_controller.run({})
        print(result)
        time.sleep(1)
