#!/bin/env/python

import sys
import smbus
import time
import math
import config
import socket
import multiprocessing
from Sensors import Temp, IMU, Depth



def sensors():
	data = ""
	data += Depth()
	data += Temp()
	data += IMU()
	return data 

class BoneClient():
	def __init__(self):

		
		socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			socket.connect((configbone.FloatHOST, configbone.BoneSocket))
			while True:
				data = sensors()
				socket.send(data)
		except:
			sock.close()


