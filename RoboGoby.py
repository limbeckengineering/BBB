#!/bin/env/python

import sys
import smbus
import time
import math
import config
import socket
import SocketServer
import pickle
import threading
from threading
from BBStepper import Stepper
from Battery import Life


OCUdata = { } 
SUBdata = { } 

def spooler_init():
	spooler = Stepper()
	spooler.init_pins(config.stepper1)
	spooler.init_pins(config.stepper2)
	
def servers_init():
	
	
def sensors_init():
	

	
  
class SUB_Server(SocketServer.BaseRequestHandler):
	def handle(self):
		self.SUBdata = self.request.recv(1024)
		self.SUBdata = pickle.loads(SUBself.data)
		self.request.sendall("N/A")

class OCU_Server(SocketServer.BaseRequestHandler):
	def handle(self):
		self.OCUdata = self.request.recv(1024)
		self.OCUdata = pickle.loads(self.OCUdata)
		self.request.sendall(SUBdata)
			

class RoboGoby(object):
	def init(self):
		spooler = threading.Thread(name='Spooler', target = spooler_init)
		servers = threading.Thread(name='Servers', target = servers_init)
		sensors = threading.Thread(name='Sensors', target = sensors_init)
		spooler.start()
		servers.start()
		sensors.start()

	def dataInit(self, address1, address2):
    		config.arduino1 = address1
    		i2c_bus(self)
    
  
	def readSensorData(self):
		print "hello"
		
	def start_server(self):
		HOST, IP = "10.0.1.119", 3456
		server = SocketServer((HOST,IP), Server)
		server.server_forever()
	
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
		stepper.cleanup(config.stepper1)
		stepper.cleanup(config.stepper2)
