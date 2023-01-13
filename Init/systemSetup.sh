
echo "Laden aller Submodule"
git submodule update --init --recursive

echo "System updaten"
sudo apt-get -y update
sudo apt-get -y upgrade

echo "mongoDB installieren"
sh installMongoDb.sh

echo "watchdog einrichten"

# echo "Nur ausführen, wenn VS Code KEINE SSH Verbindung zum Pi hat"
# read -p "Besteht aktuell eine SSH Verbindung von VS Code? (y/n)" yn
#     case $yn in
#         [Nn]* ) echo "Top!"
#         sudo apt-get update
#         sudo apt-get upgrade
# 	;;
#         [Yy]* ) echo "Dann lieber mal schnell ausmachen!";;
#     esac
