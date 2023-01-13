# Installations Routinen 
In diesem Ordner befinden sich alle nötigen Skripte und Routinen um das System auf dem Pi zu installieren.

## Installations Schritte
1. System updaten
```
sudo apt-get -y update
sudo apt-get -y upgrade
```

2. System neustarten

3. Mongo DB installieren
```
source installMongoDb.sh
```

4. In /etc/mongod.conf bindIP ändern (Damit die DB im Netzwerk sichtbar ist)
```
port: 27017
bindIp: 0.0.0.0
```

5. watchdog aufsetzen - Part 1
```
source setupWatchdog1.sh
```

6. System neustarten

7. watchdog aufsetzen - Part 2
```
source setupWatchdog2.sh
```