import serial
import time

def send_serial_command(port, baudrate, command):
    try:
        # Öffnen der seriellen Verbindung
        ser = serial.Serial(port, baudrate, timeout=1)
        
        # Warten, um sicherzustellen, dass die Verbindung hergestellt ist
        time.sleep(2)

        # Senden des Befehls als Bytes
        ser.write(command.encode())

        # Schließen der seriellen Verbindung
        ser.close()
        print("Befehl erfolgreich gesendet.")
    except Exception as e:
        print(f"Fehler beim Senden des Befehls: {e}")

if __name__ == "__main__":
    port = "/dev/ttyUSB0"  # Der Port des Arduinos
    baudrate = 19200
    command = '{"command":"setPump","runtime":1000}'

    send_serial_command(port, baudrate, command)
