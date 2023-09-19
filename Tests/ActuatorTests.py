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
            "codeOn": 1111,
            "codeOff": 1111,
            "pulseLength": 200.0,
            "initialState": False,
            "pingTime":2.0
        }
pingTest = Plug433MhzPing_Actuator(name="Dummy",collection="Dummy",config=pingConfig)
print("Before PingTest")
pingTest.set(True)
print("After PingTest")
print("Test mit set False")
pingTest.set(False)