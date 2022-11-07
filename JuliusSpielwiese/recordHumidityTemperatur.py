import AHT20
from datetime import datetime


#Inititalisiere AHT20
aht20 = AHT20.AHT20()
dt = datetime.now()

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)




with open("tempLog.csv", "a") as f:
	f.write(str(dt))
	f.write(", ")
	f.write(str(round_num(aht20.get_temperature())))
	f.write("\n")

with open("humidLog.csv", "a")as f:
	f.write(str(dt))
	f.write(", ")
	f.write(str(round_num(aht20.get_humidity())))
	f.write("\n")

with open("tempHudLog.csv", "a") as f:
	f.write(str(dt))
	f.write(", ")
	f.write(str(round_num(aht20.get_temperature())))
	f.write(", ")
	f.write(str(round_num(aht20.get_humidity())))
	f.write("\n")



print("Done")
print(str(dt))
