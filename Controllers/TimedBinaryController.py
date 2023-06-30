import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging

class TimedBinaryController(BaseBlock):

    """
    Der BinaryController gibt als Ausgang True oder False aus.
    Dabei betrachtet  er den Wert 'threshold' und gibt False aus, 
    falls der Wert unter dem Threshold liegt und True fals der Wert
    über den Threshold liegt (invert invertiert die Entscheidung einmal)
    """

    def getConfigDescription(self):
        desc: {
            "minValue":{"type":float,"desc":"input niedriger => trigger"},
            "minReaction":{"type":bool,"desc":"Was soll getriggert werden, wenn minValue unterschritten?"},
            "maxValue":{"type":float,"desc":"input höher => trigger"},
            "maxReaction":{"type":bool,"desc":"Was soll getriggert werden, wenn maxValue überschritten?"},
            "waitAfterCorrection":{"type":float,"desc":"Zeit die gewartet wird, nachdem Korrektur vorgenommen wurde"},
            "waitWhenCorrect":{"type":float,"desc":"Zeit die gewartet wird, Falls keine Korrektur nötig"},
        }
        return desc

    def __init__(self,config:dict = {"minValue":5.0,"minReaction":False,"maxValue":6.0,"maxReaction":True,"waitAfterCorrection":60.0,"waitWhenCorrect":3600.0}):
        super().__init__(["data"])
        self.__minValue = config["minValue"]
        self.__minReaction = config["minReaction"]
        self.__maxValue = config["maxValue"]
        self.__maxReaction = config["maxReaction"]
        self.__waitAfterCorrection = config["waitAfterCorrection"]
        self.__waitWhenCorrect = config["waitWhenCorrect"]
        self.__nextCall = 0

    def run(self,inputData:dict) -> bool:
        
        #prüfe pf input data mit der maske übereinstimmt
        super().checkInputData(inputData)
        input = inputData["data"]

        #prüfe ob controller wieder call-bar ist. (warte zeit zuende)
        time = time.time()
        if(self.__nextCall <= time):
            #prüfe ob reagiert werdem muss
            if(input > self.__maxValue):
                self.__nextCall = time + self.__waitAfterCorrection
                return super().safeAndReturn(self.__maxReaction)
            elif(input < self.__minValue):
                self.__nextCall = time + self.__waitAfterCorrection
                return super().safeAndReturn(self.__minReaction)
            
            else:
                #keine Korrektur nötig, 
                self.__nextCall = time + self.__waitWhenCorrect

        return super().safeAndReturn(False)    
