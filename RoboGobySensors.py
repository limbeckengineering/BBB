#!/bin/env/python


import time
import os
import config
import serial
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.UART as UART
import math
shutdown = 1

w1 = "/sys/bus/w1/devices/28-0000049561b8/w1_slave"

def readTemp():
	raw = open(w1, "r")
        lines = raw.readlines()
	raw.close()
	return lines

def tranTemp():
        temp = ""
	lines = readTemp()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = readTemp()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string =lines[1][equals_pos+2:]
		c = float(temp_string)/1000.0
		f = c*(9.0/5.0) + 32.0
	temp += str(f)
        temp += ","
        temp += str(c)
        return temp

class Temp(object):
        def init(self):
                os.system("echo BB-W1:00A0 > /sys/devices/bone_capemgr.9/slots")

        def read(self):
		value = tranTemp()
                fahrenheit,celcius = value.split(",")
                return fahrenheit +" " + celcius


class Battery_Life(object):
	def init(self):
		ADC.setup()


	def read(self):
       		value = 0
       		for x in range (0, 20):
                	value += ADC.read(config.battery_pin)
       		value = value/20
       		value = round(value, 4)
       		voltage = value * 1.8
       		voltage = voltage * (1047/47)
       		rawpercentage = voltage/25.6
       		percentage = 1 - rawpercentage
		percentage = percentage*5
		percentage = 1-percentage
       		percentage = round(percentage, 4)
		if (rawpercentage < .8):
            		shutdown = 0
			return shutdown
       		else:
            		return percentage




