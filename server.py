import os
import socket
import struct
import random
import logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
BUFFER_SIZE = 9948       
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_home(self):
        try:
            print('am intrat in do home')
            #data = conn.recv(4)
            #no_placa = struct.unpack("I", data)[0]
            
            TCP_PORT = random.randint(6667, 8887)
            print ('the port is ' , TCP_PORT)

            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s1.bind((TCP_IP, TCP_PORT))
            s1.listen(1)
            command_socket.sendall(struct.pack("I", TCP_PORT))
            print ('i have sent the posrt from server')

            conn1, addr1 = s1.accept()
            #send code 200 response
            self.send_response(200)
            #send header first
            self.send_header('Content-type','image/jpeg')
            self.end_headers()
            
            while True:
                data1 = conn1.recv(BUFFER_SIZE)
                if not data1: break
                #send file content to client
                self.wfile.write(data1)
                break
            

        except Exception as e:
            logging.exception("I HATE AVWEONE!")
            self.send_error(505, 'file not found: ' + str(e))

         
    #handle GET command
    def do_GET(self):
        print('aaaaaaaaaa'+ self.path)
        if self.path == '/image.jpg' :
                self.do_home()
        else :         
                self.send_error(404, 'file not found: ' + self.path)
       
def run():       
    print('la inceput in server')
    global TCP_IP
    TCP_IP = '127.0.0.1'
    TCP_PORT = 6666
    #BUFFER_SIZE = 20

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    global command_socket
    command_socket, addr = s.accept()
    data = command_socket.recv(BUFFER_SIZE)
    nr_placa = struct.unpack("I", data)[0]
    print ('tocmai am primit numarul placii care este: ' ,  nr_placa)
        

    server_address = ('127.0.0.1', 8888)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
