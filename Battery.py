#!/bin/env/python

import time 
import config
import Adafruit_BBIO.ADC as ADC



class Life(object):
  
  def init():
    ADC.setup()
    
  def read_voltage():
    while True:
        value = ADC.read(config.battery_pin)
       voltage = value*1.8
       return voltage
       time.sleep(5)
       
       
      
