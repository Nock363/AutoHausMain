import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging
from datetime import datetime

class TimerController(BaseBlock):

    """
    """

    def __init__(self,config:dict = {"from":"8:00:00","to":"22:00:00"}):
        super().__init__([])
        self.__from = datetime.strptime(config["from"],"%H:%M:%S").time()
        self.__to = datetime.strptime(config["to"],"%H:%M:%S").time()


    def run(self) -> bool:
        
        timeNow = datetime.now().time()

        print(self.__from)
        print(self.__to)
        print(timeNow)


        if self.__from <= timeNow <= self.__to:
            return super().safeAndReturn(True)
        else:
            return super().safeAndReturn(False)