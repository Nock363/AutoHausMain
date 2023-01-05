import sys
sys.path.insert(0, '../python_sensor_aht20/')
import AHT20
from datetime import datetime


#Inititalisiere AHT20
aht20 = AHT20.AHT20()

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)

iterations = 100


with open("tempHudLog_stressTest.csv", "a") as f:
	for i in range(0,iterations):
		print(f"iteration {i}")
		dt = datetime.now()
		f.write(str(dt))
		f.write(", ")
		f.write(str(round_num(aht20.get_temperature())))
		f.write(", ")
		f.write(str(round_num(aht20.get_humidity())))
		f.write("\n")



print("Done")
print(str(dt))
