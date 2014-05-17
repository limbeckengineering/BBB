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
import multiprocessing
from BBstepper import Stepper
from Battery import Life
from BBBgps import RoboGPS

OCUdata = { } 
SUBdata = { } 
FLOATdata= { }
run = 1

def Processes(value):
 	       spooler = multiprocessing.Process(name='Spooler', target = spooler_init)
               OCUserver = multiprocessing.Process(name='OCUServer', target = ocuserver, args=(1,1,))
               SUBserver = multiprocessing.Process(name='SUBServer', target = subserver, args=(1,1,))
               sensors = multiprocessing.Process(name='Sensors', target = sensors_init)
               spooler.start()
               OCUserver.start()
               SUBserver.start()
               sensors.start()
	       if (value ==0):
			spooler.terminate()
              	        OCUserver.terminate()
               		SUBserver.terminate()
               		sensors.terminate()
def spooler_init():
	spooler = Stepper()
	spooler.init_pins(config.stepper1)
	spooler.init_pins(config.stepper2)
	print "Spooler Initialized"

def subserver(value, first):
	print "OCUServer Started"
	if (first  == 1):
		subServer = SocketServer.TCPServer((config.HOST, config.SUBPort), SUB_Server)
		first = 0	
	while value:
		subServer.handle_request()

def ocuserver(value, first):
	print "SUBServer Started"
	if (first ==1):
		ocuServer = SocketServer.TCPServer((config.HOST,config.OCUPort), OCU_Server)
		first = 0
	while value:
		ocuServer.handle_request()

def sensors_init():
	battery = Life()
	battery.init()	
	gps = RoboGPS()

class SUB_Server(SocketServer.BaseRequestHandler):
	def handle(self):
		SUBdata = self.request.recv(1024)
		SUBdata = pickle.loads(SUBdata)
		print "Sub_Server"
	
class OCU_Server(SocketServer.BaseRequestHandler):
	def handle(self):
		OCUdata = self.request.recv(1024)
		OCUdata = pickle.loads(OCUdata)
		self.request.sendall(pickle.dumps(SUBdata))
		self.request.sendall(pcikle.dumps(FLOATdata))

class RoboGoby(object):
	def init(self):
		Processes(1)
		sensors_init()		

	def cleanup(self):
		print "Starting Cleanup"
		Processes(0)
		subserver(0,0)
		ocuserver(0,0)
		print "Cleanup Finished"
