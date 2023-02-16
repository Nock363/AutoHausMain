from Controllers.BaseBlocks import BaseBlock


class BinaryController(BaseBlock):

    def __init__(self,inputs:dict):
        super().__init__(inputs,["data"])

    def run(inputData:dict) -> bool:
        super().checkInputData(inputData)
        if inputData["data"] > 0:
            return super().safeAndReturn(True)
        else:
            return super().safeAndReturn(False)