import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

def get_available_wlans():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
        wlans = result.stdout.split('\n')
        wlans = [ssid for ssid in wlans if ssid]
        return wlans
    except Exception as e:
        print(f"Error scanning for WLANs: {e}")
        return []

def connect_to_wlan(ssid, password):
    try:
        # Disconnect any existing connections
        subprocess.run(['sudo', 'nmcli', 'connection', 'down', 'id', ssid], capture_output=True, text=True)
        # Delete the connection if it exists
        subprocess.run(['sudo', 'nmcli', 'connection', 'delete', 'id', ssid], capture_output=True, text=True)
        # Add a new connection
        result = subprocess.run(['sudo', 'nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], capture_output=True, text=True)
        print("result: ", result)
        return result.returncode == 0, result.stdout
    except Exception as e:
        print(f"Error connecting to WLAN: {e}")
        return False, str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    available_wlans = get_available_wlans()
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        success, message = connect_to_wlan(ssid, password)
        if success:
            return f'Successfully connected to {ssid}.'
        else:
            return f'Failed to connect to {ssid}: {message}'

    return render_template('index.html', wlans=available_wlans)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
