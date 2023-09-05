import serial
import time
import random

def main():
    # Öffne eine serielle Verbindung zum Arduino
    ser = serial.Serial('/dev/ttyUSB0', 19200)  # Stelle sicher, dass '/dev/ttyUSB0' korrekt ist
	#ls /dev/tty* zeigt dir auf dem PI alle möglichen USB anschlüsse an. arduino sollte normalerweise /dev/ttyACM0 oder /dev/ttyUSB0 sein.
    while True:
        try:
            # Generiere eine zufällige Blinkzeit zwischen 100 und 500 Millisekunden
            AHT20Value ={"command":"AHT20Value"}

            # Sende die Blinkzeit an den Arduino über die serielle Schnittstelle
            ser.write(str(AHT20Value).encode())

            # Warte auf eine kurze Zeit, bevor du die Antwort des Arduinos liest
            time.sleep(0.1)

            # Lies die Antwort des Arduinos von der seriellen Schnittstelle
            if ser.in_waiting > 0:
                empfangene_daten = ser.readline().decode().strip()
                print(f"Empfangene Daten: {empfangene_daten}")

            # Warte 3 Sekunden, bevor die nächste Blinkzeit gesendet wird
            time.sleep(3)

        except KeyboardInterrupt:
            # Falls du das Skript mit Strg+C beendest
            print("Skript wird beendet.")
            break

    # Schließe die serielle Verbindung zum Arduino
    ser.close()

if __name__ == "__main__":
    main()


