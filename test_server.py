#! /usr/bin/env python3
import sys
import socket
import json
import struct

host = 'localhost'
port = 9998

def send_message(sock, command, data=''):
        data_to_encode = (command, data)
        data_to_send = json.dumps(data_to_encode)
        sock.send(data_to_send.encode())

def recv_message(sock):
    data_to_decode = sock.recv(1024).decode()
    command, data = json.loads(data_to_decode)
    return command, data


s = socket.socket()
s.connect((host, port))

cmd = sys.argv[1]

if cmd == 'a':
    send_message(s, 'addJob', ["HPtest", "bash", 1])
    command, result = recv_message(s)
    print('result', result)
    s.close()

elif cmd == 'j':
    send_message(s, 'getAllJobs')
    command, jobs = recv_message(s)
    print(jobs)
    s.close()

elif cmd == 'i':
    send_message(s, 'getJobInfo', str(sys.argv[2]))
    command, job_Info = recv_message(s)
    if job_Info != -1:
        print(job_Info)
    else:
        print('bad ID')
    s.close()

elif cmd == 'r':
    send_message(s, 'removeJob', str(sys.argv[2]))
    command, result = recv_message(s)
    if result != 0:
        print('bad ID')
    s.close()

elif cmd == 'q':
    send_message(s, 'shutdown')



else:
    print('invalid command')
    sys.exit(-1)
