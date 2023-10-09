import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging

class ProportionalController(Controller):

    """
    """

    def getConfigDescription(self):
        desc: {
            "minValue":{"type":float,"desc":"Faktor um den der eingabe Wert multipliziert werden soll."}
        }
        return desc

    def __init__(self,config:dict = {"factor":1}):
        super().__init__(["data"])
        self.__factor = config["factor"]
       

    def run(self,inputData:dict) -> int:
        super().checkInputData(inputData)
        inputValue = inputData["data"]
        return super().safeAndReturn(inputValue*self.__factor)


    