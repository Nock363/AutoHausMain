import sys

from Sensor import Sensor


class HumidityTempt_AHT20(Sensor):

    def __init__(self):
        super().__init__(collection="HumidityTemp",queueDepth = 10)
