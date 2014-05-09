#!/bin/env/python

import smbus
import time
import math
import config
import socket
import thread



def i2c_bus():
  bus = smbus.SMBus(2)
  address1 = 0x2a
  address2 = 0x4b
  return address1, address2
  
class Server()
  
  def init(self, config.OCU):         ##OCU = (ip, port)
    self.s = socket.socket()
    self.s = bind(OCU)
    self.s.listen(1)
    conformation = "1"
    
  def send(self, data):
    self.s.send(data)
    self.s.send(conformation)
    receive = self.conn.recv(1024)
    if (
  
  

class RoboGoby(object):

  def dataInit(self, address1, address2):
    config.arduino1 = address1
    config.arduino2 = address2
    i2c_bus(self)
    
  
	def readSensorData(self):
	  while True:
	  for i in range(0, config.sensor_data_length):
	    config.sensorData += chr(bus.read_byte(config.arduino1)
		time.sleep(.25)
		
	def sendData(self, host):
	  Server.send(config.sensorData)
	

	def spin_counterclockwise(self, pins, rotations, rpm):
		
		
	def cleanup(self, pins):
		GPIO.cleanup()	
