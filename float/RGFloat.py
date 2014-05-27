#!/bin/env/python

import sys
import smbus
import time
import math
import config
import socket
import SocketServer
import multiprocessing
from BBstepper import Stepper
from BBBgps import RoboGPS
import select
from Sensors import Temp, Battery_Life, Compass,
from LSM303_Adafruit import LSM303

def Processes(value):
 	       spooler = multiprocessing.Process(name='Spooler', target = spooler, args=(1, depth,))
               OCUserver = multiprocessing.Process(name='OCUServer', target = ocuserver)
               SUBserver = multiprocessing.Process(name='SUBServer', target = subserver)
	       spooler.start()
	       OCUserver.start()
	       SUBserver.start()
	       if (value == 0):
			spooler.terminate()
			OCUserver.terminate()
			SUBserver.terminate()

def spooler(signal, depth):
	
	if signal == 1:
		spooler1 = Stepper()
		spooler2 = Stepper()
		spooler1.init_pins(config.stepper1)
		spooler2.init_pins(config.stepper2)
		print "Spooler Initialized"
		depthold = 0	
	else: 
		rotations = depth/4
		rpm = depthold-depth
		if rpm < 0:
			rpm = rpm*-1
			spooler1.spin_clockwise(config.stepper1, rotations, rpm, 1)
		else if rpm > 0:
			spooler1.spin_clockwise(config.stepper1, rotations, rpm, 1)
		depthold = depth		




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
					     data = sensors() 
				     	     signal = 0
				     else:
					data = sensors()
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


def sensors():
	floatData = ""
	floatData += "floatT:" + str(Temp())";bat" + str(Battery_Life())
	floatData +=";gps:" + str(RoboGPS()) + ";heading:" + str(LSM303()) + ";"
	subData = subsensors(0,1)
	subDat = subData.split(";")
	for i in range(0, len(subDa):
		values[i] = subDat.split(":")
	spool(values[0][1])
	allData = floatData + subData
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
