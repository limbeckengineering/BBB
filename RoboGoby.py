#!/bin/env/python

import sys
import smbus
import time
import math
import config
import socket
import SocketServer
import data
import pickle
from BBStepper import Stepper


def i2c_bus():
  bus = smbus.SMBus(2)
  address1 = 0x2a
  return address


def spool(depth):
	

  
class Server(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024)
		self.data = pickle.loads(self.data)
		print "Server created"
		goby = RoboGoby()
		goby.send(self.data)

class RoboGoby(object):
	def init(self):
		spooler = Stepper()	
  		spooler.init_pins(config.pins)


	def dataInit(self, address1, address2):
    		config.arduino1 = address1
    		i2c_bus(self)
    
  
	def readSensorData(self):
		print "hello"
	
	def send(self, data):
		HOST, PORT = config.host, config.port
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		run = 1
		test = 5
	
		while run:
			try:
        			sock.connect((HOST, PORT))
        			sock.sendall(pickle.dumps(data))
			except socket.error, msg:
				print ("No Connection. Trying to reach server"),
				for x in range(0, 5):
					print ("."),
					time.sleep(1)
				print "Failed"
				test -= 1	
			finally:
        			sock.close()
				if (test == 0):
					run = 0
	

	def cleanup(self)
		stepper.cleanup(config.pins)
