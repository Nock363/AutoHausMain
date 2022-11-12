import os


os.system('sudo raspi-config nonint do_i2c 0')		//aktiviert i2c

with open(/boot/config.txt, "a") as f:
	f.write(str(dtoverlay=i2c-gpio,bus=4,i2c_gpio_sda=17,i2c_gpio_scl=27))
	

os.system('sudo reboot')	