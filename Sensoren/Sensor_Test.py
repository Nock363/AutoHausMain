from Sensor import Sensor

sensor = Sensor(collection="test",queueDepth = 2)


for i in range(5):
    sensor.addToQueue(i)

sensor.printQueue()