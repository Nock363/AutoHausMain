# actuators.json

In dieser Datei werden alle Aktoren des Systems beschrieben. Mit Aktoren sind Elemente gemeint, die geschaltet werde, um die Umgebung zu manipulieren. Das Objekt hat folgende Attribute:

    active: true/false
    name: Name des Aktors
    type: Type des Aktors(Klasse aus /Actuators)
    collection: Collection in die die entscheidungen dess Aktors gespeichert werden.
    initialState: Initial Wert des Aktors. Wert der zu Anfang angenommen wird.
    config: variable Parameter, die je nach Aktor variieren. Z.B. bei Funksteckdosen codeOn/codeOff

# sensors.json

In dieser Json Datei werden die Sensoren definiert, die im Scheduler verwendet werden.
Die Sensoren werden in einem Array definiert. Jeder Sensor wird durch ein Objekt definiert.
Das Objekt hat folgende Attribute:

    active: true/false
    name: Name des Sensors
    pinID: PinID des Sensors
    class: Name der Klasse, die den Sensor repräsentiert
    intervall: Intervall in Sekunden, in dem der Sensor ausgelesen wird


# logics.json

In den Logics werden Sensoren und Aktoren mit einem Controller combiniert, welcher entscheidet, wann der die Aktoren geschaltet werden. Die Logik bildet damit also einen (offenen) Regelkreis, bei dem die Sensoren den Eingabewert Liefern und der Controller diese interpretiert. Der Input einer Logik kann aus mehren Sensoren bestehen. Eine Logik besteht aus folgenden Einträgen

    active: true/false
    name: Name der Logik
    controller: Beschreibung des controllers
        controller: Name der Controller-Klasse
        config: Individuelle Konfigurationsparameter des Controllers
        {"controller":XXX,"config":XXX}

    inputs: Alle Inputs mit den jeweiligen Parametern.
        parameter: Name des Controller-Inputs der belegt werden soll.
        input: Name des Parameters des Sensors, der mit dem Parameter verbunden werden soll.
        {"parameter":XXX,"input":YYY,"sensor:ZZZ}
        
    outputs: Liste an Aktuatoren, an die das Ausgangssignal des Controllers übergebeben werden soll.
        actuator:Name des Actuators
        {"actuator":KKK}


# pins.json

Diese Datei ist ein Backup der Configuration der Pins und der GPIO Pins. Die Daten werden intern allerdings von der Datenbank bezogen. 
**Diese Daten sollten nicht vom Nutzer manipuliert werden**
