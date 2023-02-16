from BaseBlocks import PowerPlugBlock
from Sensoren.Sensor import Sensor
from Sensoren.Dummy_Sensor import Dummy_Sensor

sensors = []
sensors.append(Dummy_Sensor(3))

powerPlugBlock = PowerPlugBlock(sensors,"plugA")