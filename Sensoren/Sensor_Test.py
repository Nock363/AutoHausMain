from Sensor import Sensor

sensor = Sensor(queueDepth = 2)

for i in range(5):
    sensor.addToQueue(i)

sensor.printQueue()