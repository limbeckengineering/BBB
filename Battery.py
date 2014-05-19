#!/bin/env/python

import time 
import config
import Adafruit_BBIO.ADC as ADC

maxValue = 1150
minValue = 900
#maxValue/maxValue
maxRatio = 1.00
#minValue/maxValue
minRatio = .78

shutdown = 1
ratioConstant = maxRatio - minRatio

class Life(object):
  
  def init(self):
    ADC.setup()
    
  def read_voltage(self):
       value = 0
       for x in range (0, 20):
		value += ADC.read_raw(config.battery_pin)
       value = value/20
       print value
       ratio = value/maxValue
       difference = maxRatio - ratio
       percentage = difference/ratioConstant
       print percentage
       if (ratio < .8):
            return shutdown
       else:
            return percentage
