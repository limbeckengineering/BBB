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


def Processes(value):
 	       spooler = multiprocessing.Process(name='Spooler', target = spooler_init)
               OCUserver = multiprocessing.Process(name='OCUServer', target = ocuserver)
               SUBserver = multiprocessing.Process(name='SUBServer', target = subserver)
	       spooler.start()
	       OCUserver.start()
	       SUBserver.start()
	       if (value == 0):
			spooler.terminate()
			OCUserver.terminate()
			SUBserver.terminate()

def spooler_init():
	spooler = Stepper()
	spooler.init_pins(config.stepper1)
	spooler.init_pins(config.stepper2)
	print "Spooler Initialized"


def raspData(data, sent):
	print "in RaspData"
	sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		sock1.connect((config.RPi1HOST, config.Rasp1Port))
		#sock2.connect((config.RPi2HOST, config.Rasp2Port))
		sock1.send(data)
		#sock2.sendall(data)	
		print "data sent to RPis"
	except:
		print "Not able to connect to Raspberry Pis"
		sock.close()


def ocu_stream(sock, CONNECTION_LIST1, OCUserver):
	signal = 1
	for socket in CONNECTION_LIST1:
		if socket != OCUserver:
			while True:
				try:
				     print "Streaming to OCU"
				     if signal==1:
					     data = sensors(1) 
				     	     signal = 0
				     else:
					data = sensors(0)
				     	message2 = data.encode(encoding='UTF-8')
				        socket.senall(message2)
 					time.sleep(.5)
				except:
				     socket.close()
				     CONNECTION_LIST1.remove(socket)
				     sendTOocu.terminate()
				     s.terminate()

def ocu_send_data(CONNECTION_LIST1, OCUserver, sock, message):
	for socket in CONNECTION_LIST1:
		if socket != OCUserver:
			try:
		 	    message = "Data recieved"
			    message = message.encode(encoding='UTF-8')
			   
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST1.remove(socket)

def ocuserver():
	CONNECTION_LIST1 = []
	OCUserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	OCUserver.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
	OCUserver.bind((config.HOST, config.OCUPort))
	print "Starting OCUServer..."
	OCUserver.listen(10)
	
	CONNECTION_LIST1.append(OCUserver)
	sent = 0

	while 1:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST1, [], [])
		
		for sock in read_sockets:
			if sock == OCUserver:
				sock, addr = OCUserver.accept()
				CONNECTION_LIST1.append(sock)
				ocu_send_data(CONNECTION_LIST1, OCUserver, sock, "Welcome to RoboGoby's OCU Server")
				print "sent client the hi message"
			else:
				try:
					
					print "created multithreaded process"
					sendTOocu = multiprocessing.Process(name = "OCU Stream", target = ocu_stream, args = (sock, CONNECTION_LIST1, OCUserver,))
					data = sock.recv(config.RECV_BUFFER)
					data = data.decode(encoding='UTF-8')
					if (data):
						raspData(data,sent)
				except:
					ocu_send_data(CONNECTION_LIST1, OCUserver, sock, "Kicking from OCUserver")
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
                        else:
                                try:
                                        data2 = sock.recv(config.RECV_BUFFER)
					subsensors(1, data2)		
                                except:
					sock.close()
                                        CONNECTION_LIST2.remove(sock)
                                        continue


def sensors(signal):
	if signal == 1:
		battery = Battery_Life()
		temp = Temperature()
		gps = RoboGPS()
		imu = IMU()
		imu.init()
		temp.init()
		battery.init()
		gps.init()
	else:
		float = ""
		float += "temp: "
		float += str(temp.read())
		float +="; battery: "
		float += str(battery.read_voltage())
		float +="; IMU: "
		float += str(imu.read())
		float += ";"
		allData = float + subsensors(0, 1)
		return allData	

def subsensors(signal, data):
	subdata = " "
	if signal ==1:
		subdata = data
		return subdata
	else:
		subdata = subdata
		return
		


class RoboGoby(object):
	def init(self):
		Processes(1)

	def cleanup(self):
		print "Starting Cleanup"
		Processes(0)
		print "Cleanup Finished"
