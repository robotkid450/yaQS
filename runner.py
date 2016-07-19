#! /usr/bin/env python3
import socket, MessageProtocol, json # imports for network
import subprocess #imports for running jobs
import sys # temp import for defining port

#define socket
host, port = '127.0.0.1', int(sys.argv[1])

def makeSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messenger = MessageProtocol.Message(sock)
    return sock, messenger

def getJob(): #messenger = message protocol object
    #connect and recive job info
    sock, messenger = makeSocket()
    print('retriving job')
    sock.connect((host, port))
    messenger.send_message('get job')
    job = messenger.recv_message()
    ds_job = json.loads(job) # ds_job is deserialized copy of job
    done1 = messenger.recv_message()
    sock.close()
    return ds_job

def runJob(job):
    #run job and recive exit code
    print('running job:',job[1])
    job_result = subprocess.call(job[2], shell=True)
    return job_result

def submitCompletion(job_result, job):
    #send job compleat + exit code
    sock, messenger = makeSocket()
    sock.connect((host, port))
    messenger.send_message('submit finished job')
    responce = messenger.recv_message()
    if responce == 'send EX code':
        messenger.send_message(job_result)
        done =  messenger.recv_message()
        if done == 'done':
            sock.close()
            print('sent job result sucsessfully')
            return 0

        else:
            print('ERROR end handshake failed')
            sock.close()
            return -2

    else:
        print('server side error')
        sock.close()
        return -3

if __name__ == '__main__':
    while True:
        job = getJob()
        if job != -1:
            print('job recived: ', job)
            job_run_result = runJob(job)
            submitCompletion(job_run_result, job)

        else:
            print('no jobs avalible')
