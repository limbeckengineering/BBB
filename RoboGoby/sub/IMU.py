#!/bin/env/python

import config
import time
import Adafruit_BBIO.UART as UART




def send(YPR):
	


class IMU(object):
        def init(self):
                UART.setup("UART1")
                os.system("echo BB-UART1 > /sys/devices/bone_capemgr.9/slots")

        def read(self):
		ser = serial.Serial(port = "/dev/ttyO1", baudrate=57600)
                ser.close()
                ser.open()
                YPR = ser.readline()
                ser.close()
		send(YPR)
	                
	
		

