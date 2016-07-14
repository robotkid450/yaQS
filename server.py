#! /usr/bin/env python3
import socketserver
import queue
import json
import sys
import struct

class TcpHandler(socketserver.BaseRequestHandler):

    '''def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())'''

    def send_message(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg.encode()
        sock.sendall(msg)

    def recv_message(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen).decode()

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def setup(self):
        self.que = q

    def handle(self):
        self.data = self.recv_message(self.request)
        print('self.data = ', self.data)
        if self.data == 'addJob':
            print('addJob')
            self.send_message(self.request, 'send job')
            self.job_to_add = self.recv_message(self.request)
            self.job_to_add = json.loads(self.job_to_add)
            print('job_to_add = ', self.job_to_add)

        self.send_message(self.request, 'done')

    def finish(self):
        q = self.que


if __name__ == "__main__":
    try:
        q = queue.QueueData()

        HOST, PORT = "localhost", int(sys.argv[1])

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), TcpHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
