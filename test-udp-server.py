#! /usr/bin/env python3
import socket
import sys

HOST, PORT = "localhost", 9999

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendMsg(sock_obj, msg):
    sock_obj.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().

def recvMsg(sock):
    received = str(sock.recv(1024), "utf-8")
    return recived


cmd = sys.argv[1]

if cmd == 'a':
    sendMsg(sock, 'addJob')



#print("Sent:     {}".format(data))
#print("Received: {}".format(received))
