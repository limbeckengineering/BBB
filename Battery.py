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

class Life(object):
  
  def init(self):
    ADC.setup()
    ratioConstant = maxRatio - minRatio
    
  def read_voltage(self, run):
    while run:
       value = ADC.read_raw(config.battery_pin)
       ratio = value/maxValue
       difference = maxRatio - ratio
       percentage = difference/ratioConstant
       if (ratio < .8):
            return shutdown
       else:
            return percentage
       time.sleep(5)
