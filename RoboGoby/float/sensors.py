#!/bin/env/python


import time
import os
import config
import serial
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.UART as UART

shutdown = 1

w1 = "/sys/bus/w1/devices/28-00000494acf0/w1_slave"

def readTemp():
        temp = ""
        raw = open(w1, "r").read()
        f = str((float(raw.split("t=")[-1])/1000)*(9.0/5.0) + 32.0)
        c = str(float(raw.split("t=")[-1])/1000)
        temp += f
        temp += ","
        temp += c
        return temp

class Temp:
        def __init__(self):
                os.system("echo BB-W1:00A0 > /sys/devices/bone_capemgr.9/slots")

        def read(self):
                   value = readTemp()
                   fahrenheit,celcius = value.split(",")
                   return fahrenheit +" " + celcius


class Battery_Life:
	def __init__(self):
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




