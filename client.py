import httplib
import sys
import socket
import time
import struct
import urllib2
TCP_IP = '127.0.0.1'

TCP_PORT = 6666
BUFFER_SIZE = 40
MESSAGE = "aloha"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

data = s.recv(BUFFER_SIZE)
#s.setblocking(0)
print('la inceput in client')
while(len(data)) :
        someType = urllib2.urlopen("http://192.168.1.6:8080/?action=snapshot").read()
        MESSAGE = someType
        s.sendall(struct.pack("I", len(MESSAGE)))
        s.sendall(MESSAGE)
#s.close()



