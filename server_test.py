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

cmd = sys.argv[2]

if cmd == 'a':
    send_message(s, 'addJob')
    data = recv_message(s)
    if data == 'send job':
        msg_to_send = json.dumps(["HPtest", "bash", 1])
        print(msg_to_send)
        send_message(s, msg_to_send)
    done = recv_message(s)
    print('done = ', done)
    s.close()

if cmd == 'j':
    send_message(s, 'getAllJobs')
    jobs = json.loads(recv_message(s))
    print(jobs)
    done = recv_message(s)
    print('done = ', done)
    s.close()

if cmd == 'i':
    send_message(s, 'getJobInfo')
    data = recv_message(s)
    if data == 'send ID':
        send_message(s, sys.argv[3])
        job_Info = json.loads(recv_message(s))
        if job_Info != -a:
            print('job info: ', job_Info)
            done = recv_message(s)
            print('done = ', done)
            s.close()
        else:
            print('bad id')
            s.close()

    else:
        print('error bad reply')
        s.close()
