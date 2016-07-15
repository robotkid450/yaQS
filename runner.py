#! /usr/bin/env python3
import socket, MessageProtocol, json # imports for network
import shelex, subprocess #imports for running jobs
import sys # temp import for defining port

#define socket
host, port = '127.0.0.1', sys.argv[1]
s = socket.socket()
MP = MessageProtocol.Message(s)

#connect and recive job info
print('retriving job')
s.connect(host, port)
MP.send_message('get job')
job = recv_message()
s.close()
if job != 'none':
    print('job recived: ', job)

else:
    print('no jobs avalible')
    sys.exit(-1)
#run job and recive exit code
job_result = subprocess.call(job[2], shell=True)

#send job compleat + exit code
s.connect(host, port)
MP.send_message('submit finished job')
responce = recv_message()
if responce == 'send EX code':
    MP.send_message(job_result)
    done = recv_message()
    if done = 'done':
        s.close()
        print('sent job result sucsessfully')
        sys.exit(0)

    else:
        print('ERROR end handshake failed')
        s.close()
        sys.exit(-2)

else:
    print('server side error')
    s.close()
    sys.exit(-3)
