#!/usr/bin/env python3

__version__ = '2.3.2'
import socketserver, socket
import yaqs.protocol as protocol
#import json
import subprocess
import logging
import os

udpAddr = ('0.0.0.0', 9999)
tcpAddr = None

debug = True

'''def sendMessage(sock, command, data=''): # composes & sends messages
    data_to_encode = (command, data)
    data_to_send = json.dumps(data_to_encode)
    sock.send(data_to_send.encode())

def recvMessage(sock): # recives and decomposes messages
    data_to_decode = sock.recv(4096).decode()
    command, data = json.loads(data_to_decode)
    return command, data'''

def getJob(): # connectes and retrives a job from to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    conn = protocol.Client(sock)
    conn.sendMessage('getJobToRun')
    command, data = conn.recvMessage()
    #print('data = ', data)
    if data != -1:
        recv_data = data
        job_ID = recv_data[0]
        job_name = recv_data[1]
        job_command = recv_data[2]
        job_working_directory = recv_data[3]
        sock.close()
        return job_ID, job_name, job_command, job_working_directory
    else:
        return None

def runJob(name, command, working_directory=os.getcwd()): # runs the retrived job
    print('running: ', name)
    original_working_directory=os.getcwd()
    if working_directory != None:
        print(working_directory)
        try:
            os.chdir(working_directory)

        except:
            result = -9
        else:
            try :
                result = subprocess.check_output(command, shell=True)
                print(result)
            except:
                result = -8

        finally:
            os.chdir(original_working_directory)

    else:
        result = subprocess.check_output(command, shell=True)

    return result.decode('utf-8')



def submitJobComplete(job_ID, job_result): # reports completed jobs to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    conn = protocol.Client(sock)
    conn.sendMessage('submitJobComplete', [job_ID, job_result])
    #reply = recvMessage()
    #print(reply)

class UDPhandler(socketserver.BaseRequestHandler): # broadcast reciver

    stopped = False

    def serve_Forever(self):
        while not self.stopped:
            self.handle_request()

    def handle(self): # recives & processes all broadcasts
        data = self.request[0].decode()
        sock = self.request[1]

        '''discovers and sets data server address must be run or
         manually set before jobs can be processed'''
        if data == 'discover':
            global tcpAddr
            tcpAddr = (self.client_address[0], 9999)

        #recives work avalible broadcast & acts accordingly
        elif data == 'work Available' and tcpAddr != None:
            job = getJob()
            #print('job=',job)
            if job != None:
                job_ID, job_name, job_command, job_working_directory = job
                result = runJob(job_name, job_command, job_working_directory)
                print(result)
                submitJobComplete(job_ID, result)
            else:
                pass

        elif data == 'shutdown':
            print('stoping')
            sock.close()
            self.stopped = True

def configureLogging():
    # Set up logging
    root_logger = logging.getLogger(__name__)
    # consoleLogStream = logging.StreamHandler()
    file_log_output = logging.FileHandler('server.log')

    if debug == True:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # consoleLogStream.setFormatter(formatter)
    file_log_output.setFormatter(formatter)

    # root_logger.addHandler(consoleLogStream)
    root_logger.addHandler(file_log_output)

    return root_logger

if __name__ == "__main__":
    # Creates broadcast reciver
    server = socketserver.UDPServer(udpAddr, UDPhandler)
    root_logger = configureLogging()
    root_logger.info('test')

    # starts runner
    try:
        server.serve_forever()
    except ValueError:
        print('shutdown')
