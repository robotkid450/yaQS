#! /usr/bin/env python3

import socketserver
import json
from collections import deque
import uuid


class QueueData(object):
    """docstring for QueueData"""
    def __init__(self):
        self.HPque = deque()
        self.SPque = deque()
        self.LPque = deque()
        #self.ques = [self.HPque, self.SPque, self.LPque] #used for planned optimization

    def pickleCurrentQueue(self, db):
        pass

    def unPickleCurrentQueue(self, db):
        pass

    def addJob(self, jobName, command, priority):
        if priority == 1:
            self.HPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        elif priority == 2:
            self.SPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        elif priority == 3:
            self.LPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        else:
            print('Bad Priority, job dropped')
            return -1

    def getJobInfo(self, jobID):
        for item in self.HPque:
            if item[0] == jobID:
                return item
            else:
                pass
        for item in self.SPque:
                if item[0] == jobID:
                    return item
                else:
                    pass
        for item in self.LPque:
            if item[0] == jobID:
                return item
            else:
                pass
        else:
            return -1


        '''for item in self.ques:            #planed optimization
            for item in item[0]:
                if item[0] == jobID:
                    return item
            else:
                return -1'''

    def getAllJobs(self):
        jobs = []
        for items in self.HPque:
            pass


    def removeJob(self, jobID):
        pass

    def modJob(self, jobID, job, command, priority, complete):
        pass

class TcpHandler(socketserver.BaseRequestHandler):

    '''def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())'''

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.request.send(self.data)
        self.close()

if __name__ == "__main__":
    '''try:
        HOST, PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), TcpHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()'''

    Q = QueueData()
    Q.addJob('HPtest', 'bash', 1)
    Q.addJob('SPtest', 'bash', 2)
    Q.addJob('LPtest', 'bash', 3)
    print('HP', Q.HPque)
    print('SP', Q.SPque)
    print('LP', Q.LPque)
    print('job info', Q.getJobInfo('asdf'))
