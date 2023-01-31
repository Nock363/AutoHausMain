import sys
sys.path.insert(0, '../')

from Sensoren.HudTemp_AHT20 import HudTemp_AHT20
from Sensoren.Pres_BMP280 import Pres_BMP280
from Sensoren.Co2H2Eth_SPG30 import Co2H2Eth_SPG30

# print("HudTemp_AHT20:")
# hudTemp_AHT20 = HudTemp_AHT20(pinID = 5)
# hudTemp_AHT20.run()

# print("Pres_BMP280:")
# pres_BMP280 = Pres_BMP280(pinID = 1)
# print(pres_BMP280.run())

print("Co2H2Eth_SPG30:")
co2H2Eth_SPG30 = Co2H2Eth_SPG30(pinID = 1)
print(co2H2Eth_SPG30.run())