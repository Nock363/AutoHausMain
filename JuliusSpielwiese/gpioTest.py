# Bibliotheken laden
from gpiozero import LED
from time import sleep

# Initialisierung von GPIO17 als LED (Ausgang)
led = LED(37)

# LED einschalten
led.on()

# 5 Sekunden warten
sleep(5)

# LED ausschalten
led.off()