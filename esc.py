#!/usr/bin/python

import Adafruit_BBIO.PWM as PWM
import time 
#import config

f = open('speed.txt', 'r')
pwm = f.readline(3)
print pwm
 
PWM.start("P8_19", 6.5, 60)

while (pwm != 100):
	var = raw_input("Enter PWM%: ")
	float(var)	
	PWM.set_duty_cycle("P8_19", float(var))
	pwm = f.readline(3)

time.sleep(2)

PWM.stop("P8_19")
PWM.cleanup()



