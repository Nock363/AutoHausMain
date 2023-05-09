import sys
sys.path.insert(0, '../')
from Controllers.BaseBlocks import BaseBlock
import logging

class JustRead(BaseBlock):


    def __init__(self,config:dict = {}):
        super().__init__([""])
       


    def run(self,inputData:dict) -> bool:
        super().checkInputData()
        