import os
import socket
import struct
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
BUFFER_SIZE = 9948       
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_home(self):
        try:
            print('am intrat in do home')
            conn.send("give me data")
            data = conn.recv(4)
            assert len(data) == 4
            len_data = struct.unpack("I", data)[0]
            data = conn.recv(len_data)
            assert len(data) == len_data 
           
            #if not data: break
            #send code 200 response
            self.send_response(200)
            #send header first
            self.send_header('Content-type','image/jpeg')
            self.end_headers()

            #send file content to client
            self.wfile.write(data)

        except IOError as e:
            self.send_error(404, 'file not found: ' + str(e))

         
    #handle GET command
    def do_GET(self):
        print('aaaaaaaaaa'+ self.path)
        if self.path == '/image.jpg' :
                self.do_home()
        else :         
                self.send_error(404, 'file not found: ' + self.path)
       
def run():       
    print('la inceput in server')
    TCP_IP = '127.0.0.1'
    TCP_PORT = 6666
    #BUFFER_SIZE = 20
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    global conn
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)

    server_address = ('127.0.0.1', 8888)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    run()
