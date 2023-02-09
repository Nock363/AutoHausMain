import BaseBlock


class FanController(BaseBlock):

    def __init__(self,inputs:dict):
        super().__init__(inputs,["Humidity","Temperature"])

       

    def run(inputData:dict) -> bool:
        super().checkInputData(inputData)
         if inputData["Humidity"] > 55:
            return super().safeAndReturn(True)
         else:
            return super().safeAndReturn(False)