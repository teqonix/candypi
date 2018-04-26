#!/bin/bash

echo "Starting installation of candytracker!"

if [ "$EUID" -ne 0 ] 
	then echo "Please run as root"
	exit
fi 

sudo apt-get install mariadb-server 
sudo mysql < dbsetup.sql > mysqldbinstall.log
pip3 install plotly
pip3 install pymysql
sudo apt-get install python-mysqldb
pip3 install dash==0.21.0  # The core dash backend
pip3 install dash-renderer==0.12.1  # The dash front-end
pip3 install dash-html-components==0.10.0  # HTML components
pip3 install dash-core-components==0.22.1  # Supercharged components
echo "@xset s noblank" >> /etc/xdg/lxsession/LXDE/autostart
echo "@xset s off" >> /etc/xdg/lxsession/LXDE/autostart
echo "@xset -dpms" >> /etc/xdg/lxsession/LXDE/autostart
