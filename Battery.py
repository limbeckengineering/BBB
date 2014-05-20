#!/bin/env/python

import time 
import config
import Adafruit_BBIO.ADC as ADC

shutdown = 1

class Life(object):
  
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


