#! /usr/bin/env python3
import sys
import socket
import json
import struct

host = 'localhost'
port = int(sys.argv[1])

def send_message(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg.encode()
    sock.sendall(msg)

def recv_message(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen).decode()

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

s = socket.socket()
s.connect((host, port))
send_message(s, 'addJob')
data = recv_message(s)
if data == 'send job':
    msg_to_send = json.dumps(["HPtest", "bash", 1])
    print(msg_to_send)
    send_message(s, msg_to_send)
data2 = recv_message(s)
print(data2)
