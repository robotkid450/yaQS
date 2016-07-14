#! /usr/bin/env python3
import socketserver
import queue
import json
import sys
import struct

'''class MessageProtocol(object):
    """docstring for MessageProtocol"""
    def __init__(self, socket):
        self.socket = socket'''


class TcpHandler(socketserver.BaseRequestHandler):

    '''def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())'''
    # The following functions define a binary protocol used to communicate
    # between the server and its clients

    # A message consists of a 4byte block containing the length of the message
    # followed by the meassage contents

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

    # End protocal functions

    def setup(self):
        self.que = q

    def handle(self):
        self.data = self.recv_message(self.request)
        if self.data == 'addJob': #adds jobs to queue
            print('adding Job')
            self.send_message(self.request, 'send job')
            self.job_to_add = json.loads(self.recv_message(self.request))
            self.que.addJob(self.job_to_add[0],self.job_to_add[1], self.job_to_add[2])
            print('added job :', self.job_to_add[0])

        elif self.data == 'getAllJobs':
            print('getting jobs')
            self.all_jobs = self.que.getAllJobs()
            self.send_message(self.request, json.dumps(self.all_jobs))

        elif self.data == 'getJobInfo':
            self.send_message(self.request, 'send ID')
            self.job_ID = self.recv_message(self.request)
            self.job_Info = self.que.getJobInfo(self.job_ID)
            self.send_message(self.request, json.dumps(self.job_Info))

        elif self.data == 'removeJob':
            self.send_message(self.request, 'send ID')
            self.job_ID = self.recv_message(self.request)
            self.result = self.que.removeJob(self.job_ID)
            self.send_message(self.request, str(self.result))

        else:
            self.send_message(self.request, 'invalid command')


    def finish(self):
        q = self.que
        self.send_message(self.request, 'done')

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
