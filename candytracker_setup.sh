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
echo "@xset s noblank" >> /etc/xdg/lxsession/LXDE/autostart
echo "@xset s off" >> /etc/xdg/lxsession/LXDE/autostart
echo "@xset -dpms" >> /etc/xdg/lxsession/LXDE/autostart
