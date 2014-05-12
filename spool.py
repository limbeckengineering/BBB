#!/bin/env/python

import sys
import time
import config
from BBStepper import Stepper


def spool(depth1, depth2):
  rotations = depth/1.2
  rpm = (depth2-depth1)/1
  
def unspool(depth):
    rotations = depth/1.2
    rpm = (depth2 - depth1)/1
    

class Spool(object):
    def init(self):
        stepper1 = Stepper.init(config.stepper1)
        stepper2 = Stepper.init(config.stepper2)
        stepper1.init()
        stepper2.init()
    
    def read
