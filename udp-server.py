#!/usr/bin/env python3
import socketserver
import json



class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def discovery(self, data):
        pass


    def setup(self):
        self.socket = self.request[1]

    '''def handle(self):
        data = self.request[0]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        self.socket.sendto(data.upper(), self.client_address)'''

    def handle(self):
        messages = []
        data = self.request[0]
        #self.socket.sendto(json.dumps(data).encode(), self.client_address)
        if json.loads(data.decode())[1] > 1:
            messages.append(data)
            number_of_packets = json.loads(data.decode())[1]
            for packet in range(number_of_packets - 1):
                data = self.socket.recv(1024)
                print('data', data)
                print('messages', messages)

                #messages.append(data)
                #self.socket.sendto(data2, self.client_address)
        else:
            messages.append(data)
        print('messages', messages)
        print('all received')


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
