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

def psi(raw):
	voltage = raw*1.8
	voltage = voltage*(1470/470)
	percent = 100.0*(voltage/5.15)
	if (percent < 10):
		return "voltage out of scope (too small)"
	if (percent > 90):
		return "voltage out of scope(too large)"
	maxPressure = 150.0
	minPressure = 0.0

	pressure = ((percent-10)*(maxPressure-minPressure))/((90-10)+minPressure)
	return pressure

def convert(pressure):
	depth = ""
	feet = pressure/.435
	feet = feet - 33.79
	meters = feet*.3048
	feet = round(feet,6)
	meters = round(meters, 5)
	depth += str(feet)
	depth += ","
	depth += str(meters)
	return depth

class Temp():
        def __init__(self):
                #os.system("echo BB-W1:00A0 > /sys/devices/bone_capemgr.9/slots")

        def read(self):
                   value = readTemp()
                   values  = value.split(",")
                   temps = "f:" + values[0] + ";c:" + values[1]
		   return temps

class IMU():
	def __init__(self):
		#os.system("sudo echo BB-UART1 > /sys/devices/bone_capemgr.9/slots")
		ser = serial.Serial(port = "/dev/ttyO1", baudrate = 57600, timeout = .5)
		ser.close()	
		ser.open()
		YPR = ser.readline()
		return YPR
		ser.close()
		

class Depth():
	def __init__(self):
		raw = 0
		ADC.setup()
		while True:
			for x in range(0, 20):
				raw += ADC.read(configSub.depth_pin)
			raw = raw/20
			pressure = psi(raw)
			value = convert(pressure)
			depth = value.split(",")
			depth = "f:" + depth[0] + ";m:"+ depth[1]
			return depth
