#!/bin/env/python

import sys
import time
import math
import config
import socket
import multiprocessing
from multiprocessing import Queue
from BBstepper import Stepper
from BBBgps import RoboGPS
import select
from RoboGobySensors import Temp, Battery_Life
from LSM303_Adafruit import LSM303


def Processes(server, spooler):
 	       spooler = multiprocessing.Process(name='Spooler', target = spooler_init)
               server = multiprocessing.Process(name='Server', target = ocuserver)
	       spooler.start()
	       server.start()
	       if (server == 0):
			server.terminate()
		if (spooler ==0):
			spooler.terminate()

def spooler_init():
	spooler = Stepper()
	spooler.init_pins(config.stepper1)
	spooler.init_pins(config.stepper2)
	print "Spooler Initialized"
	Processes(1,0)

def spool(depth):
	running = True
	while True:
		if running:
			depthold = 0
			running = false
		rotations = depth/4
		rpm = depth-depthold
		if rpm < 0:
			rpm = rpm*-1
			spooler1.spin_clockwise(config.stepper1, rotations, rpm, 1)
		else if rpm > 0:
			spooler1.spin_clockwise(config.stepper1, rotatations, rpm, 1)
		depthold = depth

def raspData(data, sent):
	print "in RaspData"
		#sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock1.connect((config.RPi1HOST, config.Rasp1Port))

		#sock2.connect((config.RPi2HOST, config.Rasp2Port))
		sock1.send(data)
		#sock2.sendall(data)	
		print "data sent to RPis"
		sock1.close()
	except:
		print "Not able to connect to Raspberry Pis"
		sock1.close()

def read_sub():
		values = { }
		beaglesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			
		beaglesock.connect((config.beagleHost, config.beaglePort))
		beaglesock.sendall("1")
		subDATA = beaglesock.recv(config.RECV_BUFFER)
		subD = subDATA.split(";")
		for i in range(0, len(subD)):
			values[i] = subD[i].split(":")
		spool(values[0][1])
		beaglesock.close()
		return subDATA

def ocu_stream(sock, CONNECTION_LIST1, OCUserver):
	signal = 1
	for socket in CONNECTION_LIST1:
			if socket != OCUserver:
				try:
				     	while True:
						if signal==1:	
					     		data = sensors(1) 
					     		signal = 0
					     		data2 = read_sub()
							data = data + ";" + data2
							message2 = data.encode(encoding='UTF-8')
					     		socket.sendall(message2)   
				     		else:
					     		data = sensors(0)
					     		data2 = read_sub()
							data = data + ";" + data2
				     	     		message2 = data.encode(encoding='UTF-8')
				             		socket.sendall(message2)
				except:
				     socket.close()
				     CONNECTION_LIST1.remove(socket)
				     
def ocu_send_data(CONNECTION_LIST1, OCUserver, sock, message):
	for socket in CONNECTION_LIST1:
		if socket != OCUserver:
			try:
			    message = message.encode(encoding='UTF-8')
			   
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST1.remove(socket)

def ocuserver():
	CONNECTION_LIST1 = []
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
	server.bind((config.HOST, config.OCUPort))
	print "Starting OCUServer..."
	server.listen(10)
	
	CONNECTION_LIST1.append(server)
	sent = 0

	while 1:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST1, [], [])
		
		for sock in read_sockets:
			if sock == server:
				sock, addr = server.accept()
				CONNECTION_LIST1.append(sock)
				ocu_send_data(CONNECTION_LIST1, server, sock, "Welcome to RoboGoby's OCU Server")
				print "Sent the startup message"
			else:
				try:
						
						data = sock.recv(config.RECV_BUFFER)
						data = data.decode(encoding='UTF-8')
						if (data=="1"):
							sendTOocu = multiprocessing.Process(name = "OCU Stream", target = ocu_stream, args = (sock, CONNECTION_LIST1, server,))
							sendTOocu.start()
						if (data =="0"):
							sendTOocu.terminate()
							readSUB.terminate()
						else:
							print data
							#raspData(data,sent)
							sent = 1
				except:
					ocu_send_data(CONNECTION_LIST1, server, sock, "Kicking from OCUserver")
					sock.close()
					CONNECTION_LIST1.remove(sock)
					continue

def gps(que):
	gps = RoboGPS()
	while True:	
		if gps.init():
			gpsData = gps.init()
			que.put(gpsData)
		else:
			que.put("N/A")

def sensors(signal):
	gpsqueue = Queue()
	floatData = ""
	temp = Temp()
	battery = Battery_Life()
	lsm303 = LSM303()
	if signal == 1:
		temp.init()
		battery.init()
	gpsProc = multiprocessing.Process(name="GPS", target = gps, args=(gpsqueue,))	
	gpsProc.start()
	gpsData = gpsqueue.get()
	gpsProc.terminate()
	floatData += "tempF:" + str(temp.read()) + ";bat:" + str(battery.read())
	floatData += ";heading:" + str(lsm303.read()) + ";gps:" + gpsData 
	return floatData


class RoboGoby(object):
	def init(self):
		Processes(1, 1)

	def cleanup(self):
		print "Starting Cleanup"
		Processes(0, 1)
		print "Cleanup Finished"
