# Allgemeine Beschreibung des Systems

Das System besteht im Fundament aus einem Scheduler. Dieser ließt alle konfigurierten Sensoren aus, ruft du Controller auf und triggert passend die Outputs. Der Scheduler wird im script main.py als Process gestartet. Parallel wird die RestAPI Gestartet, welches es dem Nutzer erlaubt, das System zu steuern über eine Rest-Schnittstelle.
#Konfiguration
Alle Konfigurationen werden im Ordner /Configs als JSON Dateien abgelegt.

