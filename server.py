#!/usr/bin/env python
import os
import socket
import struct
import random
import logging
import thread
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

BUFFER_SIZE = 9948   
conn_pool = {}    
TCP_IP = '127.0.0.1'
sock_stream = {}

class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    
    
    def do_image_page(self, nr_placa):
        try:
            print('entered in meth do_image do_image_page')
            
            self.send_response(200)
            #send header first
            self.send_header('Content-type','text/html')
            self.end_headers()
            html_file = open('/home/maat/daisy_cam/image.html', 'rd')
            html = html_file.read() % (nr_placa, nr_placa) 
            self.wfile.write(html)
            
           
        except Exception as e:
            logging.exception("EXCEPTION IN DO IMAGE PAGE!")
            self.send_error(505, 'file not found: ' + str(e))

        
    def do_home(self):
        try:
            print('am intrat in do home')
            
            self.send_response(200)
            #send header first
            self.send_header('Content-type','text/html')
            self.end_headers()
            html_file = open('/home/maat/daisy_cam/home.html', 'rd')
            lista_placi = ""
            for nr_placa in conn_pool.keys():
                lista_placi+='<a href = "/%d/image"> placa %d </a> <br>' % (nr_placa, nr_placa)
            html = html_file.read() % lista_placi
            self.wfile.write(html)
            
           
        except Exception as e:
            logging.exception("GOT AN E!")
            self.send_error(505, 'file not found: ' + str(e))

    def do_image(self, nr_placa):
        try:
            print('am intrat in do image')    
            conn1 = self.get_listen_socket(nr_placa)
            self.send_response(200)
            #send header first
            self.send_header('Content-type','image/jpeg')
            self.end_headers()
            
            while True:
                data1 = conn1.recv(BUFFER_SIZE)
                if not data1: break
                #send file content to client
                self.wfile.write(data1)
                
        except Exception as e:
            logging.exception("GOT AN EXCEPTION IN DO IMAGE!")
            self.send_error(505, 'file not found: ' + str(e))
     
    def server_bind(self):
        HTTPServer.server_bind(self)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        
        
        #handle GET command
    def do_GET(self):
        print('the path from get is: '+ self.path)
        if self.path == '/':
                self.do_home()
        elif '/image.jpg' in self.path:
                parts = self.path.split('/')
                nr_placa = int(parts[1])
                self.do_image(nr_placa)
        elif '/image' in self.path:
                parts = self.path.split('/')
                nr_placa = int(parts[1])
                self.do_image_page(nr_placa)
    
        else :         
                self.send_error(404, 'file not found: ' + self.path)
     
    def get_listen_socket(self, nr_placa):
        TCP_PORT = random.randint(6667, 8887)
        print ('the port is ' , TCP_PORT, 'the nr board is :', nr_placa)
        command_socket = conn_pool[nr_placa]
        
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.settimeout(3)
        s1.bind((TCP_IP, TCP_PORT))
        s1.listen(1)
        command_socket.sendall(struct.pack("I", TCP_PORT))
        print ('i have sent the port from server')
        conn1, addr1 = s1.accept()
        return conn1
                 
    

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
          

def verify_conn():
    print 'just entered in board verification!'
    global conn_pool
    print conn_pool
    while True:
        to_delete = []
        for k, v in conn_pool.items():
            if  not is_alive(v):
                to_delete.append(k)
        for k in to_delete:
            del conn_pool[k]
        time.sleep(5)

def is_alive(sock):
    try:
        response = sock.recv(1)
    except socket.error:
        return True
    return False
    
def initiate_board_conn():
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
        nr_placa = struct.unpack("I", data)[0]
        command_socket.setblocking(0)
        print ('just got the id of the board that is: ' ,  nr_placa)
        global conn_pool
        conn_pool[nr_placa]= command_socket


def run():       
    print('at the beginning of the server side: ')
    thread.start_new_thread( initiate_board_conn , () )
    thread.start_new_thread(verify_conn, ())
    server_address = ('0.0.0.0', 8989)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.allow_reuse_address = True

    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
