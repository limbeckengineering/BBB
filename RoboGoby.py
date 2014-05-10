#!/bin/env/python

import smbus
import time
import math
import config
import socket
import thread
import SocketServer



def i2c_bus():
  bus = smbus.SMBus(2)
  address1 = 0x2a
  return address
  
class Server(SocketServer.BaseRequestHandler):
  
  def handle(self):
  	self.data = self.request.recv(1024)
  	config.data += self.data
  	
  	self.request.sendall("data recieved")
    
  def start(self)
  	HOST, PORT = "10.0.1.202", 1234
  	server = SocketServer.TCPServer((HOST, PORT), Server)
  	server.serve_forever()
  
 

class RoboGoby(object):

  def dataInit(self, address1, address2):
    config.arduino1 = address1
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
