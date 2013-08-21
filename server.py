#!/usr/bin/env python
import os
import socket
import struct
import random
import logging
import thread
import threading
import time
import base_conn_funct
import db
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

BUFFER_SIZE = 9948   

TCP_IP = '127.0.0.1'
sock_stream = {}

class TestLock:
   def acquire(self):
       print 'acquire'
       return
       
   def release(self):
       print 'release'
       return
       
class TestDict(dict):
    def copy(self):
       return self
       
class ProtectedDictionary():
   
    def  __init__(self):
        self.dict = {}
        self.lock = threading.Lock()
        #self.lock = TestLock()
    
    def __getitem__(self, key):
        with self.lock:
            retrieved_val = self.dict[key]
        return retrieved_val

    def __delitem__(self, key):
        with self.lock:
            del self.dict[key]
        
    def __setitem__(self, key, val):
        with self.lock:
            self.dict[key] = val

    def copy(self):
        with self.lock:
            d = dict(self.dict)
        return d
        
    def __repr__(self):
        with self.lock:
            r = repr(self.dict)
        return r
        
    def __str__(self):
        with self.lock:
            s = str(self.dict)
        return s

conn_pool = ProtectedDictionary()    
#conn_pool =  TestDict()   

class HTTPRequestHandler(BaseHTTPRequestHandler):
    
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
            for nr_placa in conn_pool.copy().keys():
                lista_placi+='<a href = "/%d/image"> placa %d </a> <br>' % (nr_placa, nr_placa)
            html = html_file.read() % lista_placi
            self.wfile.write(html)
            
           
        except Exception as e:
            logging.exception("GOT AN Exception!")
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
                
        elif '/do_register_board' in self.path:
               data = self.path[13:]
               user = data.split('&')[0].split('=')[1]
               uuid = data.split('&')[1].split('=')[1]
               db.try_insert(user, uuid)
               self.do_image_page(uuid)
    
        else :         
                self.send_error(404, 'file not found: ' + self.path)
    
    def do_POST(self):
        content_len = self.headers.getheader('content-length')
        print len(content_len)
        post_body = self.rfile.read(content_len) 
        print 'got a POST'
        print post_body
        
        self.do_home()
        
        
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
                 
def run():       
    print('at the beginning of the server side: ')
    thread.start_new_thread( base_conn_funct.initiate_board_conn , (conn_pool, ) )
    thread.start_new_thread(base_conn_funct.verify_conn, (conn_pool, ))
    server_address = ('0.0.0.0', 8989)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print('http server is running...')
    httpd.allow_reuse_address = True

    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
