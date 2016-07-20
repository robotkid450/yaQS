#!/usr/bin/env python3

import socket
import json
import argparse

# Define needed global variables
host = 'localhost'
tcpPort = 9998
udpPort = 9999

# Define socket
sock = socket.socket()

# Helper functions
def send_message(sock, command, data=''):
        data_to_encode = (command, data)
        data_to_send = json.dumps(data_to_encode)
        sock.send(data_to_send.encode())

def recv_message(sock):
    data_to_decode = sock.recv(1024).decode()
    command, data = json.loads(data_to_decode)
    return command, data
# End helper function
