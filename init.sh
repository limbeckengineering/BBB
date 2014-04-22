#!/bin/bash

if (( $EUID != 0 )); then 
   echo "$(tput setaf 1)This must be run as root. Try 'sudo bash $0'.$(tput sgr0)" 
   exit 1 
fi

read -p "$(tput bold ; tput setaf 1)Press [Enter] to begin, [Ctrl-C] to abort...$(tput sgr0)"

echo "Installing necessary dependencies and libraries..."

sleep 2

ntpdate pool.ntp.org

apt-get update && apt-get upgrade -y

apt-get install python3-serial -y

apt-get install openjdk-7-jre -y

apt-get install build-essential python-dev python-smbus -y
git clone git://github.com/adafruit/adafruit-beaglebone-io-python.git
cd adafruit-beaglebone-io-python
python setup.py install
cd ..
rm -rf adafruit-beaglebone-io-python

apt-get install gpsd gpsd-clients python-gps
