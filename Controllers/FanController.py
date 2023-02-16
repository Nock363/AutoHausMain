from Controllers.BaseBlocks import BaseBlock


class FanController(BaseBlock):

    def __init__(self):
        super().__init__(mask=["Humidity","Temperature"])

       

    def run(inputData:dict) -> bool:
        super().checkInputData(inputData)
        if inputData["Humidity"] > 55:
            return super().safeAndReturn(True)
        else:
            return super().safeAndReturn(False)