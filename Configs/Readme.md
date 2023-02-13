# sensors.json

In dieser Json Datei werden die Sensoren definiert, die im Scheduler verwendet werden.
Die Sensoren werden in einem Array definiert. Jeder Sensor wird durch ein Objekt definiert.
Das Objekt hat folgende Attribute:
    active: true/false
    name: Name des Sensors
    pinID: PinID des Sensors
    class: Name der Klasse, die den Sensor repräsentiert
    intervall: Intervall in Sekunden, in dem der Sensor ausgelesen wird

# pins.json

Diese Datei ist ein Backup der Configuration der Pins und der GPIO Pins. Die Daten werden intern allerdings von der Datenbank bezogen