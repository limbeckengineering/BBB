#!/bin/env/python

import sys
import smbus
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


def Processes(value):
 	       spooler = multiprocessing.Process(name='Spooler', target = spooler_init)
               server = multiprocessing.Process(name='Server', target = server)
	       spooler.start()
	       server.start()
	       if (value == 0):
			spooler.terminate()
			server.terminate()

def spooler_init():
	spooler = Stepper()
	spooler.init_pins(config.stepper1)
	spooler.init_pins(config.stepper2)
	print "Spooler Initialized"


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

def read_sub(sock, CONNECTION_LIST1, OCUserver, addr):
	values = {}
	try:
		while True:
			print "in while lloop"
			subDATA = sock.recv(config.RECV_BUFFER)
			subD = subDATA.split(";")
			for i in range(0, len(subD)):
				values[i] = subD[i].split(":")
			print values
			spool(values[0][1])
			for socket in CONNECTION_LIST1:
				if socket != server:
					print "about to sendall SUB"
					socket.sendall(subDATA)	
					print "sent all SUB"
	except:
		socket.close()
		CONNECTION_LIST1.remove(socket)		

def ocu_stream(sock, CONNECTION_LIST1, OCUserver):
	signal = 1
	for socket in CONNECTION_LIST1:
			if socket != OCUserver:
				try:
				     	print "Streaming to OCU"
				     	while True:
						if signal==1:	
					     		print "in if block"
					     		data = sensors(1) 
				     	     		print "recieved data with signal 1"
					     		signal = 0
					     		message2 = data.encode(encoding='UTF-8')
					     		socket.sendall(message2)   
					     		print "sent data1 message"
				     		else:
					     		print "in else block"
					     		data = sensors(0)
					     		print "recieved data with signal 2"
				     	     		message2 = data.encode(encoding='UTF-8')
				             		socket.sendall(message2)
 					     		time.sleep(.5)
					     		print "all other data sent"
				except:
				     socket.close()
				     CONNECTION_LIST1.remove(socket)
				     
def send_data(CONNECTION_LIST1, server, sock, message):
	for socket in CONNECTION_LIST1:
		if socket != server:
			try:
			    message = message.encode(encoding='UTF-8')
			   
			    socket.sendall(message)
			except:
			    socket.close()
			    CONNECTION_LIST1.remove(socket)

def server():
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
				
					if str(addr[0]) == "10.0.1.119":
						readSUB = multiprocessing.Process(name = "readSUB", target = read_sub, args = (sock, CONNECTION_LIST1, server, addr[0],))
						readSUB.start()
					
					else:
						sendTOocu = multiprocessing.Process(name = "OCU Stream", target = ocu_stream, args = (sock, CONNECTION_LIST1, server,))
						data = sock.recv(config.RECV_BUFFER)
						data = data.decode(encoding='UTF-8')
						if (data=="1"):
							sendTOocu.start()
						if (data =="0"):
							sendTOocu.terminate()
							readSUB.terminate()
						else:
							print data
							#raspData(data,sent)
							sent = 1
				except:
					send_data(CONNECTION_LIST1, server, sock, "Kicking from Server")
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
		Processes(1)

	def cleanup(self):
		print "Starting Cleanup"
		Processes(0)
		print "Cleanup Finished"
