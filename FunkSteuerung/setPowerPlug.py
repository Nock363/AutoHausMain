import logging
import time

from rpi_rf import RFDevice

pulseLength = 320
repeats = 5

gpioPin = 3

plugs = []
plugs.append({"Name":"A","OnCode":1361,"OffCode":1364})

rfdevice = RFDevice(gpioPin)
rfdevice.enable_tx()
rfdevice.tx_repeat = repeats



rfdevice.tx_code(plugs[0]["OnCode"], 1, pulseLength, 24)
time.sleep(0.1)
rfdevice.tx_code(plugs[0]["OffCode"], 1, pulseLength, 24)
rfdevice.cleanup()