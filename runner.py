#!/usr/bin/env python3

__version__ = '1.1.1'
import socketserver, socket
import json
import subprocess

udpAddr = ('127.0.0.1', 9999)
# udpAddr = ('0.0.0.0', 9999)
tcpAddr = None

def send_message(sock, command, data=''): # composes & sends messages
        data_to_encode = (command, data)
        data_to_send = json.dumps(data_to_encode)
        sock.send(data_to_send.encode())

def recv_message(sock): # recives and decomposes messages
    data_to_decode = sock.recv(4096).decode()
    command, data = json.loads(data_to_decode)
    return command, data

def getJob(): # connectes and retrives a job from to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    send_message(sock, 'getJobToRun')
    recv_command, recv_data = recv_message(sock)
    job_ID = recv_data[0]
    job_name = recv_data[1]
    job_command = recv_data[2]
    sock.close()
    return job_ID, job_name, job_command

def runJob(name, command): # runs the retrived job
    print('running: ', name)
    result = subprocess.call(command, shell=True)
    return result

def submitJobComplete(job_ID, job_result): # reports completed jobs to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    send_message(sock, 'submitJobComplete', [job_ID, job_result])
    #reply = recv_message(sock)
    #print(reply)

class UDPhandler(socketserver.BaseRequestHandler): # broadcast reciver

    def handle(self): # recives & processes all broadcasts
        data = self.request[0].decode()
        sock = self.request[1]

        '''discovers and sets data server address must be run or
         manually set before jobs can be processed'''
        if data == 'discover':
            global tcpAddr
            tcpAddr = (self.client_address[0], 9998)

        #recives work avalible broadcast & acts accordingly
        elif data == 'work Available' and tcpAddr != None:
            job_ID, job_name, job_command = getJob()
            result = runJob(job_name, job_command)
            print(result)
            submitJobComplete(job_ID, result)




if __name__ == "__main__":
    # Creates broadcast reciver
    server = socketserver.UDPServer(udpAddr, UDPhandler)
    # starts runner
    server.serve_forever()
