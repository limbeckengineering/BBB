#!/bin/env/python

from RoboGoby import RoboGoby
import time
import SocketServer 


goby = RoboGoby()

goby.init()
time.sleep(20)
goby.cleanup()

