#enter stepper.'rotation'(pinarray, degrees, rpm)
#1.8 per step

import Adafruit_BBIO.GPIO as GPIO
import time
import math
import config

def step_forward(pins, pin_index):
	GPIO.output(config.stepper1["clk"], GPIO.LOW)
def step_backward(pins, pin_index):
	GPIO.output(config.stepper1["clk"], GPIO.LOW)


class Stepper(object):

	def init_pins(self, pins):
		GPIO.setup(config.stepper1["clk"], GPIO.OUT)
		GPIO.setup(config.stepper1["dir"], GPIO.OUT)
		GPIO.output(config.stepper1["clk"], GPIO.HIGH)
		
	def spin_clockwise(self, pins, rotations, rpm):
		sleep_time=0.3/float(rpm)
		steps_forward = rotations*200
		GPIO.output(config.stepper1["dir"], GPIO.HIGH)	
		for x in range(0, steps_forward):
			step_forward(self,pins)
			time.sleep(sleep_time)
			GPIO.output(config.stepper1["clk"], GPIO.HIGH)
	
	def spin_counterclockwise(self, pins, rotations, rpm):
		sleep_time=.3/float(rpm)
		steps_backward = rotations*200
		GPIO.output(config.stepper1["dir"], GPIO.LOW)
		for x in range(0, steps_backward):
			step_backward(self,pins)
			time.sleep(sleep_time)
			GPIO.output(config.stepper1["clk"], GPIO.HIGH)
		
	def cleanup(self, pins):
		GPIO.cleanup()		

