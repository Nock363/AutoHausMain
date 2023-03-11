# Allgemeine Beschreibung des Systems

Das System besteht im Fundament aus einem Scheduler. Dieser ließt alle konfigurierten Sensoren aus, ruft du Controller auf und triggert passend die Outputs. Der Scheduler wird im script main.py als Process gestartet. Parallel wird die RestAPI Gestartet, welches es dem Nutzer erlaubt, das System zu steuern über eine Rest-Schnittstelle.
#Konfiguration
Alle Konfigurationen werden im Ordner /Configs als JSON Dateien abgelegt.

# Allgemeine Conventionen

## XXX_Test

diese Skripte beschreiben Tests für das Skript XXX und können im allgemeinen ignoriert werden.


# Scheduler

Der Scheduler regelt die finale ausführung der Sensoren, Logik und Aktoren. In der Aktuellen Ausführung werden dabei lediglich die Logiken betrachtet, und die dabei angegebenen Sensoren getriggert.
Die daraus resultierende Daten werden direkt and den jeweiligen Controller übergeben und daraus ein Ausgangs-Signal erzäugt.

# RestAPI

Die RestAPI stellt eine Schnittstelle da, um mit dem System über das lokale Netzwerk interagieren zu können. Die vorhandenen Funktionen sind folgende:

## /pins
Auflistung aller Pins des System, mit allen relevanten Informationen

## /sensors
Auflistung aller Sensoren

## /actuators
Auflistung aller Aktoren


## /logics
Auflistung aller Logiken(Kombination aus Sensoren, Controller und Aktoren


## /data/collection/length
Wiedergabe der length Letzten Werte von collection

## /collections
Auflistung aller verfügbaren Collections

## /stopScheduler
Stoppt den Scheduler

## /startScheduler
Startet den Scheduler       

