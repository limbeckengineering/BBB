#!/bin/bash

echo "BB-UART1 > /sys/devices/bone_capemgr.9/slots"
echo "BB-UART4 > /sys/devices/bone_capemgr.9/slots"

gpsd /dev/ttyO4 -F /var/run/gpsd.sock



