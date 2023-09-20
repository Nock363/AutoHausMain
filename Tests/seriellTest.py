import serial
import time
import random

def main():
    # Öffne eine serielle Verbindung zum Arduino
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Stelle sicher, dass '/dev/ttyACM0' korrekt ist

    while True:
        try:
            # Generiere eine zufällige Blinkzeit zwischen 100 und 500 Millisekunden
            blink_zeit = random.randint(100, 500)

            # Sende die Blinkzeit an den Arduino über die serielle Schnittstelle
            ser.write(str(blink_zeit).encode())

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
