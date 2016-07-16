#!/usr/bin/env python3
import socketserver
import MessageProtocol

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def setup(self):
        self.socket = self.request[1]
        self.MP = MessageProtocol.Message(self.socket)

    def handle(self):
        data = self.request[0]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        self.socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
