#!/usr/bin/python

import socket

s = socket.socket()
host - socket.gethostname()
port = 12345
s.bind((host,port))

s.listen(5)

c, addr = s.accept()

print 'Connection from: ', addr

c.send('Hello this is the BeagleBone black')
