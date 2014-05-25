#!/bin/env/python

import Adafruit_BBIO.ADC as ADC
import time
import config


def psi(raw):
	voltage = raw*1.8
	voltage = voltage*(1470/470)
	percent = 100.0 * (voltage/5.15)
	if (percent < 10):
		return "voltage out of scope (too small)"
	if (percent > 90):
		return "voltage out of scope (too large)"
	maxPressure = 150.0
	minPressure = 0.0

	pressure = ((percent-10)*(maxPressure-minPressure))/((90-10)+minPressure)
	return pressure


def convert(pressure):
	depth = ""
	feet = pressure/.43
	feet = feet - 34.42
	meters = feet*.3048
	feet = round(feet, 6)
	meters = round(meters, 5)
	depth += str(feet)
	depth += ","
	depth += str(meters)
	return depth

def start():
	raw = 0
	ADC.setup()
	while True:
		for x in range(0, 20):
			raw+=ADC.read(config.depth_pin)
		raw = raw/20
		pressure = psi(raw)
		print pressure
		value = convert(pressure)
		feet,meters = value.split(",")
		print "Feet: " + feet
		print "Meters: " + meters
		time.sleep(1)			 
