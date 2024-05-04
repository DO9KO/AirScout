#!/bin/bash

# Aktualisieren der Paketliste
sudo apt update

# Aktualisieren aller installierten Pakete
sudo apt upgrade -y

# Erstellen des Verzeichnisses für Apt-Schlüsselringe
sudo mkdir -p /etc/apt/keyrings/

# Herunterladen des Grafana-Schlüssels und Hinzufügen zu den Apt-Schlüsselringen
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

# Hinzufügen der Grafana-Apt-Quelle zur Datei "grafana.list"
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Aktualisieren der Paketliste nach dem Hinzufügen der Grafana-Apt-Quelle
sudo apt-get update

# Installation von MariaDB Server und Grafana
sudo apt install mariadb-server grafana -y

# MySQL-Sicherheitsinstallation mit automatischen Antworten
echo "sniffer24" | sudo mysql_secure_installation <<EOF

Y
Y
Y
Y
Y
EOF

# Einloggen als Root-Benutzer in MySQL und Erstellen der Datenbank, eines neuen Benutzers und Zuweisen von Berechtigungen
sudo mysql -u root -p"sniffer24" -e "
CREATE DATABASE daten;
CREATE USER 'airscout'@'localhost' IDENTIFIED BY 'sniffer24';
GRANT ALL PRIVILEGES ON daten.* TO 'airscout'@'localhost';
FLUSH PRIVILEGES;
"

# Aktivieren und Starten des Grafana-Servers
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server

