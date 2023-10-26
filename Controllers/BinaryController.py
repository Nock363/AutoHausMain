import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging

class BinaryController(Controller):

    """
    Der BinaryController gibt als Ausgang True oder False aus.
    Dabei betrachtet  er den Wert 'threshold' und gibt False aus, 
    falls der Wert unter dem Threshold liegt und True fals der Wert
    über den Threshold liegt (invert invertiert die Entscheidung einmal)
    """

    def getConfigDescription(self) -> dict:
        return {
            "threshold": {
                "type": float,
                "description": "Threshold, ab dem True ausgegeben wird"
            },
            "invert": {
                "type": bool,
                "description": "invertiert die Entscheidung"
            }
        }

    def __init__(self,config:dict = {"threshold":0,"invert":False}):
        super().__init__(mask=["data"],config=config)
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