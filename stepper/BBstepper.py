#enter stepper.'rotation'(pinarray, degrees, rpm)
#1.8 per step

import Adafruit_BBIO.GPIO as GPIO
import time
import math
import config

def step_forward(pins, pin_index):
	l=config.l
	m=config.m
	n=config.n
	o=config.o

	GPIO.output(config.pins[l], GPIO.HIGH)
	GPIO.output(config.pins[m], GPIO.LOW)
	GPIO.output(config.pins[n], GPIO.LOW)
	GPIO.output(config.pins[o], GPIO.LOW)

	config.l=l+1
	config.m=m+1
	config.n=n+1
	config.o=o+1
	if (config.o==3):
		config.o=0
	if (config.n==3):
		config.n=0
	if (config.m==3):
		config.m=0
	if (config.l==3):
		config.l=0

def step_backward(pins, pin_index):
	GPIO.output(config.pins[l2], GPIO.HIGH)
	GPIO.output(config.pins[m2], GPIO.LOW)
	GPIO.output(config.pins[n2], GPIO.LOW)
	GPIO.output(config.pins[o2], GPIO.LOW)
	l2=l2+1
	m2=m2+1
	n2=n2+1
	o2=o2+1
	if (o2==3):
		o2=0
	if (n2==3):
		n2=0
	if (m2==3):
		m2=0
	if (l2==3):
		l2=0

class Stepper(object):

	def init_pins(self, pins):
		for pin in pins:
			GPIO.setup(pin, GPIO.OUT)
		for pin in pins:
			GPIO.output(pin, GPIO.LOW)

	def spin_clockwise(self, pins, rotations, rpm):
		sleep_time=0.1/float(rpm)
		steps_forward = rotations*200	
		for x in range(0, steps_forward):
			step_forward(self,pins)
			time.sleep(sleep_time)
		
	def spin_counterclockwise(self, pins, rotations, rpm):
		sleep_time=.1/float(rpm)
		steps_backward = rotations*200
		for x in range(0, steps_backward):
			step_backward(self,pins)
			time.sleep(sleep_time)


