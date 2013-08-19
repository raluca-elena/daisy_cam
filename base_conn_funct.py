#!/usr/bin/env python
import os
import socket
import struct
import random
import logging
import thread
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

TCP_IP = '127.0.0.1'
BUFFER_SIZE = 9948
   
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
          
def verify_conn(conn_pool):
    print 'just entered in board verification!'
    #global conn_pool
    print conn_pool
    while True:
        to_delete = []
        for k, v in conn_pool.copy().items():
            if  not is_alive(v):
                to_delete.append(k)
        for k in to_delete:
            print 'i am a deleeeeateeer ', k
            del conn_pool[k]
        time.sleep(5)

def is_alive(sock):
    try:
        response = sock.recv(1)
    except socket.error:
        return True
    return False
    
def initiate_board_conn(conn_pool):
    TCP_PORT = 6666
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    set_keepalive(s, after_idle_sec=1, interval_sec=3, max_fails=5)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    while True:    
        command_socket, addr = s.accept()
        set_keepalive(command_socket, after_idle_sec=1, interval_sec=3, max_fails=5)
        data = command_socket.recv(BUFFER_SIZE)
        #nr_placa = struct.unpack("l", data)[0]
        a, b = struct.unpack('>QQ', data)
        unpacked = (a << 64) | b
        nr_placa = unpacked
        command_socket.setblocking(0)
        print ('just got the id of the board that is: ' ,  nr_placa)
        conn_pool[nr_placa]= command_socket


