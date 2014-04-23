#!/usr/bin/python

import socket
import time
import config


data = {"temp": "67.45", "thruster 1": "5"} 

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host,port))

s.listen(5)

c, addr = s.accept()

print 'Connection from: ', addr

c.send(data)
