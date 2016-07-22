#!/usr/bin/env python3

__version__ = 1.0
import socketserver, socket
import json
import subprocess

udpAddr = ('127.0.0.1', 9999)
tcpAddr = None

def send_message(sock, command, data=''):
        data_to_encode = (command, data)
        data_to_send = json.dumps(data_to_encode)
        sock.send(data_to_send.encode())

def recv_message(sock):
    data_to_decode = sock.recv(4096).decode()
    command, data = json.loads(data_to_decode)
    return command, data

def getJob():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    send_message(sock, 'getJobToRun')
    recv_command, recv_data = recv_message(sock)
    job_ID = recv_data[0]
    job_name = recv_data[1]
    job_command = recv_data[2]
    sock.close()
    return job_ID, job_name, job_command

def runJob(name, command):
    print('running: ', name)
    result = subprocess.call(command, shell=True)
    return result

def submitJobComplete(job_ID, job_result):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    send_message(sock, 'submitJobComplete', [job_ID, job_result])
    #reply = recv_message(sock)
    #print(reply)

class UDPhandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].decode()
        sock = self.request[1]
        if data == 'discover':
            # print('discover')
            global tcpAddr
            tcpAddr = (self.client_address[0], 9998)

        elif data == 'work Available' and tcpAddr != None:
            job_ID, job_name, job_command = getJob()
            result = runJob(job_name, job_command)
            print(result)
            submitJobComplete(job_ID, result)




if __name__ == "__main__":
    server = socketserver.UDPServer(udpAddr, UDPhandler)
    server.serve_forever()
