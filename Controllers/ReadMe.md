# Allgemeine Beschreibung

Controller stellen das eigentliche Herzstück der Steuerung dar. Sie kombinieren variabel viele Inputs zu einem Ausgangssignal, welches an einen folgenden Controller übergeben werden kann oder an variabel viele Aktoren.

Ein Controller sollte aus einem Controller bestehen, der mit passenden Funktionen erweitert wird (Vererbung).
Der Kontroller muss zwangsweise die Funktion 'run(inputData:dict)' besitzen.  Diese Funktion wird aufgerufen, um den controller mit den 'inputData' rechnen zu lassen. Der Rückgabe-Wert besteht aus der Entscheidung des Controllers.


## Controller

Die Datei Controller beschreibt verschiedene Basis-Blöcke, auf deren Basis andere komplexere Controller gebaut werden

### Controller

Der Controller stellt die Grundbasis für einen Controller dar und besitz keine weiteren besonderen Eigenschaften. Im Constructor wird dem Controller eine Liste an Strings übergeben, welches im folgenden als Maske fungiert um zu überprüfen, ob die Eingabedaten(als Dictonary) valide sind.
Er besitzt folgende Funktionene:

    checkInputData(inputData:dict):
    Prüft ob inputData alle Parameter aus der Maske besitzt.

    safeAndReturn(ret):
    Speichert die Variable ret als letzten Wert ab und gibt dann ret zurück.