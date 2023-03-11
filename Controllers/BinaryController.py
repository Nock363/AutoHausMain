import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging

class BinaryController(BaseBlock):

    """
    Der BinaryController gibt als Ausgang True oder False aus.
    Dabei betrachtet  er den Wert 'threshold' und gibt False aus, 
    falls der Wert unter dem Threshold liegt und True fals der Wert
    über den Threshold liegt (invert invertiert die Entscheidung einmal)
    """

    def __init__(self,config:dict = {"threshold":0,"invert":False}):
        super().__init__(["data"])
        self.__threshold = config["threshold"]
        self.__invert = config["invert"]
       


    def run(self,inputData:dict) -> bool:
        super().checkInputData(inputData)
        
        flag = (inputData["data"] > self.__threshold)
        if(self.__invert):
            flag = not flag

        if flag:
            return super().safeAndReturn(True)
        else:
            return super().safeAndReturn(False)