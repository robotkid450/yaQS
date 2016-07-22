#!/usr/bin/env python3

__version__ = 1.0
import socket
import json
import argparse

# Define needed global variables
host = 'localhost'
port = 9998
SERVER_ADDR = (host, port)
# Define socket
sock = socket.socket()

# Helper functions
def send_message(sock, command, data=''): # composes & sends messages
        data_to_encode = (command, data)
        data_to_send = json.dumps(data_to_encode)
        sock.send(data_to_send.encode())

def recv_message(sock): # recives and decomposes messages
    data_to_decode = sock.recv(1024).decode()
    command, data = json.loads(data_to_decode)
    return command, data
# End helper function

def get_args(): # parses command line arguments + commands
    argParse = argparse.ArgumentParser(
        description='Interface with yaQS server.'
        )

    commandsParsers = argParse.add_subparsers(help='commands', dest='command')

    # addJob command
    addJobParser = commandsParsers.add_parser(
        'add-job', aliases=['add'], help='Add a job to queue.'
        )
    addJobParser.add_argument(
        'name', action='store', help='The name of the job.'
        )
    addJobParser.add_argument(
        'shellCommand', action='store', help='The command to be run'
        )
    addJobParser.add_argument(
        'priority',type=int, action='store', help='The jobs priority.'
        )

    # getAllJobs command
    getAllJobsParser = commandsParsers.add_parser(
        'show-jobs', aliases=['jobs'], help='Show all jobs.'
        )

    # getJobInfo command
    getJobInfoParser = commandsParsers.add_parser(
        'job-info',  aliases=['info'], help='Get a jobs info.'
        )
    getJobInfoParser.add_argument(
        'jobID', action='store', help='The ID of the desired job.'
        )

    # removeJob command
    removeJobParser = commandsParsers.add_parser(
        'remove-job', aliases=['remove'], help='Remove a job from queue.'
        )
    removeJobParser.add_argument(
        'jobID', action='store', help='The ID of the desired job.'
        )

    # shutdown command
    shutdownParser = commandsParsers.add_parser(
        'shutdown', help='Remotely shutdown yqQS server.'
        )


    # parse arguments
    args = argParse.parse_args()
    return args

def callComms(sock, args): # translates parsed args into network commands
    print(args.command)
    if args.command == 'add-job' or args.command == 'add':
        command = 'addJob'
        data = [args.name, args.shellCommand, args.priority]
        addJob(sock, command, data)
    elif args.command == 'show-jobs' or args.command == 'jobs':
        command = 'getAllJobs'
        data = ''
        getAllJobs(sock, command, data)
    elif args.command == 'job-info' or args.command == 'info':
        command = 'getJobInfo'
        data = args.jobID
        getJobInfo(sock, command, data)
    elif args.command == 'remove-job' or args.command == 'remove':
        command = 'removeJob'
        data = args.jobID
        removeJob(sock, command, data)
    elif args.command == 'shutdown':
        command = 'shutdown'
        data = ''
        shutdown(sock, command, data)
    # elif args.command ==  or args.command == :
        # pass
    else:
        return -9
    return 0

def addJob(sock, command, data): # tells server to add job
    try:
        sock.connect(SERVER_ADDR)
        send_message(sock, command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    command , recv_data = recv_message(sock)
    if recv_data == 0:
        print('Jobs added sucsessfully.')
    else:
        print('Error adding job.')
        return -2
    return 0

def getAllJobs(sock, command, data): # gets all jobs from server & prints to
    try:                             # stdout
        sock.connect(SERVER_ADDR)
        send_message(sock, command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    command , recv_data = recv_message(sock)
    if len(recv_data[0]) > 0:
        print('High Priority:')
        print('ID       | Name')
        print('---------------')
        for item in recv_data[0]:
            print(item[0]+ ' | '+ item[1])
        print('---------------\n')
    if len(recv_data[1]) > 0:
        print('Standard priority:')
        print('ID       | Name')
        print('---------------')
        for item in recv_data[1]:
            print(item[0]+ ' | '+ item[1])
        print('---------------\n')
    if len(recv_data[2]) > 0:
        print('Low priority:')
        print('ID       | Name')
        print('---------------')
        for item in recv_data[2]:
            print(item[0]+ ' | '+ item[1])
        print('---------------\n')

def getJobInfo(sock, command, data): # get specific job info & prints to stdout
    try:
        sock.connect(SERVER_ADDR)
        send_message(sock, command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    command, recv_data = recv_message(sock)
    ID = recv_data[0]
    name = recv_data[1]
    command = recv_data[2]
    print('ID:  ' + ID)
    print('Name:  ' + name)
    print('Command:  ' + Command)

def removeJob(sock, command, data): # tells server to remove job
    try:
        sock.connect(SERVER_ADDR)
        send_message(sock, command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    recv_data = recv_message(sock)
    if recv_data == 0:
        print('Job removed sucsessfully.')
    elif recv_data == -1:
        print('ERROR: Job not found.')

def shutdown(sock, command, data): # tells server to shutdown
    try:
        sock.connect(SERVER_ADDR)
        send_message(sock, command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1

if __name__ == '__main__':
    args = get_args() # calls argparser
    result = callComms(sock, args) # sends command to server
