#!/bin/env/python

import sys
import smbus
import time
import math
import config
import socket
import SocketServer
import threading
import multiprocessing
from BBstepper import Stepper
from Battery import Life
from BBBgps import RoboGPS
import select

OCUdata = { } 
subDATA = {"hello Josef Biberstein...I am watching you" } 
floatDATA= { }
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

def ocu_send_message(sock, message):
	for socket in CONNECTION_LIST1:
		if socket != server and socket == sock:
			try:
		 	    message = message.encode(encoding='UTF-8')
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST1.remove(socket)

def sub_send_data(sock, message):
	for socket in CONNECTION_LIST2:
		if socket != server and socket == sock:
			try:
			    message = message.encode(encoding='UTF-8')
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST2.remove(socket)

def ocuserver():
	CONNECTION_LIST1 = []
	OCUserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	OCUserver.bind((config.HOST, config.OCUPort))
	Print "Starting OCUServer..."
	server.listen(10)
	
	CONNECTION_LIST1.append(server)

	while 1:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST1, [], [])
		
		for sock in read_sockets:
			if sock == OCUserver:
				sock, addr = OCUserver.accept()
				CONNECTION_LIST1.append(sock)
				send_data(sock, "Welcome to RoboGoby's OCU Server")
			else:
				try:
					data = sock.recv(config.RECV_BUFFER)
					if data:
						data = data.decode(encoding='UTF-8')
						floatDATA += data
						ocu_send_data(sock, floatDATA)
					else:
						ocu_send_data(sock, floatDATA)
				except:
					sock.close()
					CONNECTION_LIST1.remove(sock)
					continue

def subserver():
    	CONNECTION_LIST2 = []
        SUBserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SUBserver.bind((config.HOST, config.SUBPort))
        Print "Starting SUBServer..."
        server.listen(10)

        CONNECTION_LIST2.append(server)

        while 1:
                read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST2, [], [])

                for sock in read_sockets:
                        if sock == SUBserver:
                                sock, addr = OCUserver.accept()
                                CONNECTION_LIST2.append(sock)
                                send_data(sock, "Welcome to RoboGoby's SUB Server")
                        else:
                                try:
                                        data2 = sock.recv(config.RECV_BUFFER)
                                        if data2:
                                                data2 = data2.decode(encoding='UTF-8')
                                                subDATA += data2
                                                sub_send_data(sock, subDATA)
                                        else:
                                                sub_send_data(sock, subDATA)
                                except:
                                        sock.close()
                                        CONNECTION_LIST2.remove(sock)
                                        continue

def sensors_init():
	battery = Life()
	gps = RoboGPS()
	battery.init()
	gps.init()
	
class RoboGoby(object):
	def init(self):
		Processes(1)
		sensors_init()		

	def cleanup(self):
		print "Starting Cleanup"
		Processes(0)
		print "Cleanup Finished"
