import sys
sys.path.insert(0, '../')
from Controllers.Controller import Controller
import logging

class JustRead(Controller):


    def __init__(self,config:dict = {}):
        super().__init__([""])
       


    def run(self,inputData:dict) -> bool:
        super().checkInputData()
        