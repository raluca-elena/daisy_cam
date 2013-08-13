import httplib
import sys
import socket
import time
import struct
import urllib2
import random
TCP_IP = '127.0.0.1'

TCP_PORT = 6666
BUFFER_SIZE = 40
my_name = random.randint(2000, 3000)
#MESSAGE = "aloha"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(struct.pack("I", my_name))


#s.setblocking(0)
print('la inceput in client')
while True:
        data = s.recv(BUFFER_SIZE)
        new_port = struct.unpack("I", data)[0]
        print('received new port', new_port)
        s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_data.connect((TCP_IP, new_port))
        print ('just instantiated new socket s_data')

        imgData = urllib2.urlopen("http://192.168.1.6:8080/?action=snapshot").read()


        s_data.sendall(imgData)
        s_data.close()



