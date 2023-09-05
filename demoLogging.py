import logging

# Erstelle eine leere Liste, um die Log-Nachrichten zu speichern
log_messages = []

# Erstelle einen benutzerdefinierten Handler, der die Nachrichten in die Liste speichert
class ListHandler(logging.Handler):
    def emit(self, record):
        log_messages.append(self.format(record))

# Konfiguriere den Logger
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG)

# Erstelle einen Handler für die Konsole
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Füge den Konsolen-Handler zum Logger hinzu
logger = logging.getLogger()
logger.addHandler(console_handler)

# Erstelle einen benutzerdefinierten Handler und füge ihn zum Logger hinzu
list_handler = ListHandler()
logger.addHandler(list_handler)

# Beispiel-Log-Nachrichten
logger.debug("Dies ist eine Debug-Nachricht")
logger.info("Dies ist eine Info-Nachricht")
logger.warning("Dies ist eine Warnung")
logger.error("Dies ist eine Fehlermeldung")
logger.critical("Dies ist eine kritische Nachricht")

# Funktion zur Abfrage der letzten N Log-Nachrichten
def getLastLogs(N):
    return log_messages[-N:]

# Abfrage der letzten 100 Log-Nachrichten
last_100_logs = getLastLogs(100)
for log in last_100_logs:
    print(log)
