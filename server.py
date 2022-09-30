#  coding: utf-8 

#    Copyright 2022 Johnson Zhao

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html

#curl -i -X POST -d "fake data" 127.0.0.1:8080
import socketserver
from os.path import exists

def encode_and_send(soc, data):
    data = data.encode('utf-8')
    soc.sendall(data)
    print('Data sent back to client')

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.addr = self.request.getpeername()
        print(f'Connection from {self.addr}')

        self.recvd_data = self.request.recv(1024).strip()
        self.recvd_data = self.recvd_data.decode('utf-8')
        print (f"Got a request of:\n{self.recvd_data}")
        self.req_list = []
        self.req_list = self.recvd_data.split('\r\n')
        self.req1 = []
        self.req1 = self.req_list[0].split(' ')
        print(self.req1)

        #['GET', '/favicon.ico', 'HTTP/1.1']
        if self.req1[0] != 'GET':
            self.response = 'HTTP/1.1 405 Method Not Allowed\r\n'
            self.response += 'Content-Type: text/html;\r\n'
            self.response += 'oh no!'
            encode_and_send(self.request, self.response)

        else:
            if self.req1[1] == '/':
                self.i = open("www/index.html", "r")
                self.i = self.i.read()
                self.response = ''
                self.response += 'HTTP/1.1 200 OK\r\n'  #  status response
                self.response += 'Content-Type: text/html;\r\n'  # content HTML
                self.response += self.i + '\r\n'
                encode_and_send(self.request, self.response)

            else:
                self.file_dir = self.req1[1]
                self.file_dir = 'www' + self.file_dir

                if exists(self.file_dir):
                    self.file = open(self.file_dir, 'r')
                    self.file = self.file.read()
                    self.response = ''
                    self.response += 'HTTP/1.1 200 OK\r\n'  #  status response
                    self.response += 'Content-Type: text/html;'  # content HTML
                    self.response += self.file + '\r\n'
                    encode_and_send(self.request, self.response)

                else:
                    self.response = ''
                    self.response += 'HTTP/1.1 404 Not Found\r\n'
                    self.response += 'Content-Type: text/html;\r\n'
                    self.response += 'you put in a no no link'
                    encode_and_send(self.request, self.response)
                    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    print(f'Server on {HOST} port {PORT}')

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()