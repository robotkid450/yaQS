#! /usr/bin/env python3

import socketserver


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
    #production code
    '''try:
        HOST, PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), TcpHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()'''

#temporary testing code
    q = QueueData()
    q.addJob('HPtest', 'bash', 1)
    q.addJob('HPtest2', 'bash', 1)
    q.addJob('SPtest', 'bash', 2)
    q.addJob('SPtest2', 'bash', 2)
    q.addJob('LPtest', 'bash', 3)
    q.addJob('LPtest2', 'bash', 3)

    a = q.getAllJobs()

    print('a 0 0', a[0][0][0])
    i = a[0][0][0]

    b = q.removeJob(i)
    print('b ', b)

    n = q.getAllJobs()
    print('jobs after removal', n)
