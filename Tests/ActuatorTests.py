import sys
sys.path.insert(0, '../')
from Actuators.Dummy_Actuator_Thread import Dummy_Actuator_Thread
from Actuators.Plug433MhzPing_Actuator import Plug433MhzPing_Actuator


# actuator = Dummy_Actuator_Thread(name="Dummy",collection="Dummy",config={})
# print("before set")
# actuator.set(True)
# print("after set")


#433Mhz Ping test
pingConfig = {
            "codeOn": 5527299,
            "codeOff": 5527308,
            "pulseLength": 173.2,
            "initialState": False,
            "pingTime":3.0
        }
pingTest = Plug433MhzPing_Actuator(name="Dummy",collection="Dummy",config=pingConfig)
print("Before PingTest")
pingTest.set(True)
# print("After PingTest")
# print("Test mit set False")
pingTest.set(False)