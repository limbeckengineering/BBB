#!/bin/env/python

#enter stepper.'rotation'(pinarray, degrees, rpm)
#1.8 per step

import Adafruit_BBIO.GPIO as GPIO
import time
import math
import config
import multiprocessing

def step_forward(pins, rotations, rpm):
		from BBstepper import Stepper
		stepper = Stepper()
		sleep_time=0.3/float(rpm)
		steps_forward = rotations*200
		GPIO.output(pins["dir"], GPIO.HIGH)	
		for x in range(0, steps_forward):
			GPIO.output(pins["clk"], GPIO.LOW)
			time.sleep(sleep_time)
			GPIO.output(pins["clk"], GPIO.HIGH)
		stepper.spin_clockwise(pins, rotations, rpm, 0)

def step_backward(pins, rotations, rpm):
		from BBstepper import Stepper
		stepper = Stepper()
		sleep_time=.3/float(rpm)
		steps_backward = rotations*200
		GPIO.output(pins["dir"], GPIO.LOW)
		for x in range(0, steps_backward):
			GPIO.output(pins["clk"], GPIO.LOW)
			time.sleep(sleep_time)
			GPIO.output(pins["clk"], GPIO.HIGH)
		stepper.spin_counterclockwise(pins, rotations,rpm,0)		



class Stepper(object):

	def init_pins(self, pinarray):
		GPIO.setup(pinarray["clk"], GPIO.OUT)
		GPIO.setup(pinarray["dir"], GPIO.OUT)
		GPIO.output(pinarray["clk"], GPIO.HIGH)
		
	def spin_clockwise(self, pinarray, rotations, rpm, signal):
		clockwise = multiprocessing.Process(name='Clockwise', target=step_forward, args=(pins, rotations, rpm,))
		clockwise.start()
		if signal == 0:
			clockwise.terminate()
		
	
	def spin_counterclockwise(self, pinarray, rotations, rpm, signal):
		counterclock = multiprocessing.Process(name='CounterClock', target = step_backward, args=(pins, rotations,rpm,))
		counterclock.start()
		if signal == 0:
			counterclock.terminate()
		
	def cleanup(self, pinarray):
		GPIO.cleanup()		

