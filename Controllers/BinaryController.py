import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock


class BinaryController(BaseBlock):

    def __init__(self):
        super().__init__(["data"])

    def run(self,inputData:dict) -> bool:
        super().checkInputData(inputData)
        if inputData["data"] > 0:
            return super().safeAndReturn(True)
        else:
            return super().safeAndReturn(False)