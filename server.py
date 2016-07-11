#! /usr/bin/env python3

import socketserver
import json
from collections import deque
import uuid


class QueueData(object):
    """docstring for QueueData
       This is a basic multi-priority job queueing system."""

    def __init__(self):
        self.HPque = deque()    #Creates high priority que
        self.SPque = deque()
        self.LPque = deque()

    def pickleCurrentQueue(self, db):
        pass

    def unPickleCurrentQueue(self, db):
        pass

    def addJob(self, jobName, command, priority):   #adds a job to specified que

        if priority == 1:
            self.HPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        elif priority == 2:
            self.SPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        elif priority == 3:
            self.LPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        else:
            print('Bad Priority, job dropped')
            return -1

    def getJobInfo(self, jobID):    # Retrives a jobs info
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

    def getAllJobs(self):   #Gets all job names + IDs

        jobsHP = [] #High priority jobs
        jobsSP = [] #standard priority jobs
        jobsLP = [] #Low priority jobs

        for item in self.HPque:                 #These loop through ques
            jobsHP.append([item[0], item[1]])   #and extract the job name
                                                #plus the jobs ID
        for item in self.SPque:
            jobsSP.append([item[0], item[1]])

        for item in self.LPque:
            jobsLP.append([item[0], item[1]])

        return jobsHP, jobsSP, jobsLP


    def removeJob(self, jobID): #Removes jobs from que
        for item in self.HPque:
            if item[0] == jobID:
                print(item)
                self.HPque.remove(item)
                break
            else:
                pass

        for item in self.SPque:
            if item[0] == jobID:
                self.SPque.remove(item)
                break
            else:
                pass

        for item in self.LPque:
            if item[0] == jobID:
                self.LPque.remove(item)
                break
            else:
                pass

        else:
            return -1

        return 0

        
    def modJob(self, jobID, job, command, priority):
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

if __name__ == "__main__":  #temporary testing code
    '''try:
        HOST, PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), TcpHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()'''

    q = QueueData()
    q.addJob('HPtest', 'bash', 1)
    q.addJob('HPtest2', 'bash', 1)
    q.addJob('SPtest', 'bash', 2)
    q.addJob('SPtest2', 'bash', 2)
    q.addJob('LPtest', 'bash', 3)
    q.addJob('LPtest2', 'bash', 3)

    a = q.getAllJobs()
    print('jobs:', a)
