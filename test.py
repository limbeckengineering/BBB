#!/bin/env/python

from RoboGoby import Server
from RoboGoby import RoboGoby
import time
import SocketServer 

HOST, PORT = "10.0.1.202", 1234


server = SocketServer.TCPServer((HOST,PORT), Server)



server.serve_forever()


