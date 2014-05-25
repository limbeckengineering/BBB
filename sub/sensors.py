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

class Temperature(object):
        def init(self):
                os.system("echo BB-W1:00A0 > /sys/devices/bone_capemgr.9/slots")

        def read(self):
                   value = readTemp()
                   fahrenheit,celcius = value.split(",")
                   return fahrenheit +" " + celcius


class Battery_Life(object):

  def init(self):
    ADC.setup()
    time.sleep(1)

  def read_voltage(self):
       value = 0
       for x in range (0, 20):
                value += ADC.read(config.battery_pin)
       value = value/20
       value = round(value, 4)
       voltage = value * 1.8
       voltage = voltage * (1047/47)
       percentage = voltage/25.6
       percentage = .2 - (1-percentage)
       percentage = .2/percentage
       if (percentage < .8):
            return shutdown
       else:
            return percentage


class IMU(object):
	def init(self):
		UART.setup("UART1")
		os.system("sudo echo BB-UART1 > /sys/devices/bone_capemgr.9/slots")
		ser = serial.Serial(port = "/dev/ttyO1", baudrate = 57600, timeout = .5)
		ser.close()
	
	def read(self):
		ser.open()
		YPR = ser.readline()
		return YPR
		ser.close()
		

