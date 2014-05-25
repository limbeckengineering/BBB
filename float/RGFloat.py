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
from BBBgps import RoboGPS
import select
from Sensors import Temperature, Battery_Life


ocuDATA = { } 
subDATA = {"hello Josef Biberstein...I am watching you" } 
floatDATA= ""
run = 1

def Processes(value):
 	       spooler = multiprocessing.Process(name='Spooler', target = spooler_init)
               OCUserver = multiprocessing.Process(name='OCUServer', target = ocuserver)
               SUBserver = multiprocessing.Process(name='SUBServer', target = subserver)
               s = multiprocessing.Process(name='Sensors', target = sensors)
	       spooler.start()
	       OCUserver.start()
	       SUBserver.start()
	       s.start()
	       if (value == 0):
			spooler.terminate()
			OCUserver.terminate()
			SUBserver.terminate()
			s.terminate()

def spooler_init():
	spooler = Stepper()
	spooler.init_pins(config.stepper1)
	spooler.init_pins(config.stepper2)
	print "Spooler Initialized"


def ocu_stream(sock):
	for socket in CONNECTION_LIST1:
		if socket != server:
			while True:
				try:
				     global floatDATA
				     message1 = floatDATA.encode(encoding='UTF-8')
				     socket.send(message1)
				except:
				     socket.close()
				     CONNECTION_LIST1.remove(socket)
				     sendTOocu.terminate()

def ocu_send_data(sock, message):
	for socket in CONNECTION_LIST1:
		if socket != server:
			try:
		 	    message = subDATA.encode(encoding='UTF-8')
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST1.remove(socket)

def sub_send_data(sock, message):
	for socket in CONNECTION_LIST2:
		if socket != server:
			try:
			    message = message.encode(encoding='UTF-8')
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST2.remove(socket)

def ocuserver():
	CONNECTION_LIST1 = []
	OCUserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	OCUserver.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
	OCUserver.bind((config.HOST, config.OCUPort))
	print "Starting OCUServer..."
	OCUserver.listen(10)
	
	CONNECTION_LIST1.append(OCUserver)

	while 1:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST1, [], [])
		
		for sock in read_sockets:
			if sock == OCUserver:
				sock, addr = OCUserver.accept()
				CONNECTION_LIST1.append(sock)
				send_data(sock, "Welcome to RoboGoby's OCU Server")
			else:
				try:
					sendTOocu = multiprocessing.Process(name = 'OCU Stream', target = ocu_stream, args=(sock,))
					data = sock.recv(config.RECV_BUFFER)
					floatDATA += data
					data = data.decode(encoding='UTF-8')
					if (data == "1"):
						sendTOocu.start()

				except:
					ocu_send_data(sock, "Kicking from OCUserver")
					sock.close()
					CONNECTION_LIST1.remove(sock)
					continue

def subserver():
    	CONNECTION_LIST2 = []
        SUBserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	SUBserver.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM,1)
        SUBserver.bind((config.HOST, config.SUBPort))
        print "Starting SUBServer..."
        SUBserver.listen(10)

        CONNECTION_LIST2.append(SUBserver)

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
                                except:
                                        sub_send_data(sock, "Kicking from SUBserver")
					sock.close()
                                        CONNECTION_LIST2.remove(sock)
                                        continue


def sensors():
	battery = Battery_Life()
	temp = Temperature()
	gps = RoboGPS()
	imu = IMU()
	imu.init()
	temp.init()
	battery.init()
	gps.init()
	global floatDATA
	floatDATA += "temp: "
	floatDATA += str(temp.read())
	floatDATA +="; battery: "
	floatDATA += str(battery.read_voltage())
	floatDATA +="; IMU: "
	floatDATA += str(imu.read())
	floatDATA += ";"
	print floatDATA

class RoboGoby(object):
	def init(self):
		Processes(1)

	def cleanup(self):
		print "Starting Cleanup"
		Processes(0)
		print "Cleanup Finished"
