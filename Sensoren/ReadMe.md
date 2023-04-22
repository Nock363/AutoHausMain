# Sensoren
Die Sensoren basieren alle auf der Basis Klasse Sensor.py. Als Beispiele können unteranderem HudTemp_AHT20.py betrachtet werden. 

## Integrieren von neuen Sensoren. 
Beim hinzufügen ist es wichtig, den Sensor auch unter "\_\_init\_\_.py" hinzuzufügen. Damit dieser Sensor auch in anderen Skripten erkannt.

# Namenskonvention für Sensoren

## Messwert:
- Hud = Humidity
- Temp = Temperature
- Pres = Pressure(Luftdruck)
- Co2 = CO2
- H2 = H2
- Ph = PH
- Ec = Ec
- Eth = Ethanol

## Name
> [Messwerte]_[Sensorname]

beispiel:
> HudTemp_AHT20

# Test der Sensorklassen

Im Skript Test.py werden verschiedene Sensoren getestet. Allgemein sollten die Senosren ersteinmal getestet werden, bevor man sie im Scheduler verwendet.