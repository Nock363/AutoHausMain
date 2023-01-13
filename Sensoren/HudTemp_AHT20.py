import sys

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


from Sensor import Sensor
sys.path.insert(0, '../libs/AHT20')
import AHT20

class HudTempt_AHT20(Sensor):

    def __init__(self):
        super().__init__(collection="HumidityTemp",queueDepth = 10)


    def run(self):