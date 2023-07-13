import serial
import time

# Configure the serial port
port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Function to send data to Arduino
def send_data(data):
    data_str = ','.join(str(val) for val in data)  # Convert data to comma-separated string
    port.write(data_str.encode())  # Send the data over serial

# Example usage
data_array = [0, 0]
time.sleep(1)

send_data(data_array)

# Close the serial port
port.close()
