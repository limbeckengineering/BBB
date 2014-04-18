#!/usr/bin/python

import Adafruit_BBIO.PWM as PWM
import time 
import config

PWM.start("P8_19", 10)
PWM.set_duty_cycle("P8_19", 6.5)
PWM.set_frequency("P8_19", 50)

while (pwm != 100):
	pwm = f.read()
	PWM.set_duty_cycle("P8_19",6.5)
	pwm = f.read()

time.sleep(2)

PWM.stop("P8_19")
PWM.cleanup()



