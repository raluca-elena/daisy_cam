#!/usr/bin/env python
import httplib
import sys
import socket
import time
import struct
import urllib2
import random
TCP_IP = '127.0.0.1'
#TCP_IP = 'daysi-cam-23675.euw1.actionbox.io'

TCP_PORT = 6666
BUFFER_SIZE = 40

my_name = random.randint(2000, 3000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

nr_bytes = s.send(struct.pack("I", my_name))
print 'sending id_placa: ', nr_bytes
print('running client')
while True:
        data = s.recv(BUFFER_SIZE)
        print 'received new port', data, len(data)
        new_port = struct.unpack("I", data)[0]


        s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_data.connect((TCP_IP, new_port))
        print ('just instantiated new socket s_data')
        start = time.time()
        imgData = urllib2.urlopen("http://192.168.1.6:8080/?action=snapshot").read()
        print "this lasted  ---------: " , time.time() - start


        s_data.sendall(imgData)
        s_data.close()



