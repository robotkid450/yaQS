#! /usr/bin/env python3
import socketserver
import yaqsQueue
import json
import sys
import MessageProtocol


class TcpHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.que = q
        self.MP = MessageProtocol.Message(self.request)

    def handle(self):
        self.data = self.MP.recv_message()
        if self.data == 'addJob': #adds jobs to queue
            print('adding Job')
            self.MP.send_message('send job')
            self.job_to_add = json.loads(self.MP.recv_message())
            self.que.addJob(self.job_to_add[0],self.job_to_add[1], self.job_to_add[2])
            print('added job :', self.job_to_add[0])

        elif self.data == 'getAllJobs':
            print('getting jobs')
            self.all_jobs = self.que.getAllJobs()
            self.MP.send_message(json.dumps(self.all_jobs))

        elif self.data == 'getJobInfo':
            print('job info request')
            self.MP.send_message('send ID')
            self.job_ID = self.MP.recv_message()
            self.job_Info = self.que.getJobInfo(self.job_ID)
            self.MP.send_message(json.dumps(self.job_Info))

        elif self.data == 'removeJob':
            print('job remove request')
            self.MP.send_message('send ID')
            self.job_ID = self.MP.recv_message()
            print('removing job:', self.job_ID)
            self.result = self.que.removeJob(self.job_ID)
            self.MP.send_message(str(self.result))

        else:
            self.MP.send_message('invalid command')


    def finish(self):
        q = self.que
        self.MP.send_message('done')

if __name__ == "__main__":
    try:
        q = yaqsQueue.QueueData()

        HOST, PORT = "localhost", int(sys.argv[1])

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), TcpHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
