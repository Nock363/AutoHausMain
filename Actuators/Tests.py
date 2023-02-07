import sys
sys.path.insert(0, '../')

from Actuators.Dummy_Actuator import Dummy_Actuator
import time

actuator = Dummy_Actuator("dummy","Dummy_Actuator",False,{})

actuator.set(True)
time.sleep(1)
actuator.set(False)
