import sys
sys.path.insert(0, '../')

from Actuators.Dummy_Actuator import Dummy_Actuator
from Actuators.Plug433Mhz_Actuator import Plug433Mhz_Actuator
import time

# dummyActuator = Dummy_Actuator("dummy","Dummy_Actuator",False,{})
# dummyActuator.set(True)
# time.sleep(1)
# dummyActuator.set(False)


plugAConfig = {"codeOn":1361,"codeOff":1364,"pulseLength":320}
plug433MhzActuator = Plug433Mhz_Actuator("plugA","Plugs433Mhz",False,plugAConfig)
print("Debug1")
time.sleep(1)
plug433MhzActuator.set(True)
print("Debug2")
time.sleep(5)
plug433MhzActuator.set(False)
print("Debug3")
#time.sleep(2)
# plug433MhzActuator.set(False)
# print("Debug4")