#!/usr/bin/python


import time
import RoboGoby
import smbus

bus = smbus.SMBus(1)
address = 0x2a

while True:
    enviData = ""
    for i in range(0, 20):
      RoboGoby.data += chr(bus.read_byte(address))
    time.sleep(.5)
    

