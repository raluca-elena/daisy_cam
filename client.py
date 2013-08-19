#!/usr/bin/env python
import httplib
import sys
import socket
import time
import struct
import urllib2
import random
import uuid
TCP_IP = '127.0.0.1'

def set_keepalive(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


TCP_PORT = 6666
BUFFER_SIZE = 40
board_uuid = uuid.uuid4()
max_int64 = 0xFFFFFFFFFFFFFFFF
packed_board_uuid  = struct.pack('>QQ', (board_uuid.int >> 64) & max_int64, board_uuid.int & max_int64)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

nr_bytes = s.send(packed_board_uuid)
set_keepalive(s, after_idle_sec=1, interval_sec=3, max_fails=5)
         
print 'sending id_placa as %d bytes '% nr_bytes
print('running client')
while True:
        data = s.recv(BUFFER_SIZE)
        print 'received new port', data, len(data)
        new_port = struct.unpack("I", data)[0]


        s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_data.connect((TCP_IP, new_port))
        
        print ('just instantiated new socket s_data')
        start = time.time()
        imgData = urllib2.urlopen("http://192.168.1.3:8080/?action=snapshot").read()
        print "this lasted  ---------: " , time.time() - start


        s_data.sendall(imgData)
        s_data.close()



