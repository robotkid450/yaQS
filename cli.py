#!/usr/bin/env python3

__version__ = '2.3.2'
import socket
#import json
import argparse
import sys
import yaqs.protocol as protocol
# Define needed global variables

server_addr = None
# example
# server_addr = ('192.168.1.x', 9999)
server_addr = ('localhost', 9999)

# Define socket
sock = socket.socket()

# Helper functions
'''def sendMessage(sock, command, data=''): # composes & sends messages
        data_to_encode = (command, data)
        data_to_send = json.dumps(data_to_encode)
        sock.send(data_to_send.encode())

def recvMessage(sock): # recives and decomposes messages
    data_to_decode = sock.recv(1024).decode()
    command, data = json.loads(data_to_decode)
    return command, data'''

def listQueue(queue, queue_name):
    print('%s:' % queue_name)
    print('ID       | Name')
    print('---------------')
    for item in queue:
        print(item[0]+ ' | '+ item[1])
    print('---------------\n')
# End helper function

def getArgs(): # parses command line arguments + commands
    argParse = argparse.ArgumentParser(
        description='Interface with yaQS server.'
        )

    commandsParsers = argParse.add_subparsers(help='commands', dest='command')

    # addJob command
    add_job_parser = commandsParsers.add_parser(
        'add-job', aliases=['add'], help='Add a job to queue.'
        )
    add_job_parser.add_argument(
        'name', action='store', help='The name of the job.'
        )
    add_job_parser.add_argument(
        'shell_command', action='store', help='The command to be run'
        )
    add_job_parser.add_argument(
        '-w','--working-directory', nargs='?', default=0, action='store',
        help='The directory for the command to be run in.'
        )
    add_job_parser.add_argument(
        '-p','--priortiy', nargs='?', type=int, default=2, action='store',
        help='The jobs priority.'
        )

    # getAllJobs command
    get_all_jobs_parser = commandsParsers.add_parser(
        'show-jobs', aliases=['jobs'], help='Show all jobs.'
        )

    # getJobInfo command
    get_job_info_parser = commandsParsers.add_parser(
        'job-info',  aliases=['info'], help='Get a jobs info.'
        )
    get_job_info_parser.add_argument(
        'jobID', action='store', help='The ID of the desired job.'
        )

    # removeJob command
    remove_job_parser = commandsParsers.add_parser(
        'remove-job', aliases=['remove'], help='Remove a job from queue.'
        )
    remove_job_parser.add_argument(
        'jobID', action='store', help='The ID of the desired job.'
        )

    # shutdown command
    shutdown_parser = commandsParsers.add_parser(
        'shutdown', help='Remotely shutdown yqQS server.'
        )


    # parse arguments
    args = argParse.parse_args()
    return args

def callComms(sock, args): # translates parsed args into network commands
    # print(args.command)
    if args.command == 'add-job' or args.command == 'add':
        command = 'addJob'
        data = [args.name, args.shell_command, args.priortiy]
        data.append(args.working_directory)
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
        sock.connect(server_addr)
        trans = protocol.Client(sock)
        trans.sendMessage(command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    command , recv_data = trans.recvMessage()
    if recv_data == 0:
        print('Jobs added sucsessfully.')
    else:
        print('Error adding job.')
        return -2
    return 0

def getAllJobs(sock, command, data): # gets all jobs from server & prints to
    try:                             # stdout
        sock.connect(server_addr)
        trans = protocol.Client(sock)
        trans.sendMessage(command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    command , recv_data = trans.recvMessage()
    jobsFound = False
    
    if len(recv_data[3]) > 0:
        jobsFound = True
        listQueue(recv_data[3], 'Running')

    if len(recv_data[0]) > 0:
        jobsFound = True
        listQueue(recv_data[0], 'High priority')

    if len(recv_data[1]) > 0:
        jobsFound = True
        listQueue(recv_data[1], 'Standard priority')

    if len(recv_data[2]) > 0:
        jobsFound = True
        listQueue(recv_data[2], 'Low priority')
    
    if len(recv_data[4]) > 0:
        jobsFound = True
        listQueue(recv_data[4], 'Finished')

    if not jobsFound:
        print('No jobs currently queued or running.')

def getJobInfo(sock, command, data): # get specific job info & prints to stdout
    try:
        sock.connect(server_addr)
        trans = protocol.Client(sock)
        trans.sendMessage(command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    command, recv_data = trans.recvMessage()
    ID = recv_data[0]
    name = recv_data[1]
    command = recv_data[2]
    working_directory = recv_data[3]
    result = recv_data[4]
    print('ID:  ' , ID)

    print('Name:  ' , name)

    print('Command:  ' , command)
    
    if working_directory != None:
        print('working Directory:' , working_directory)
    
    if result != None:
        print('result :' , result)


def removeJob(sock, command, data): # tells server to remove job
    try:
        sock.connect(server_addr)
        trans = protocol.Client(sock)
        trans.sendMessage(command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1
    recv_data = trans.recvMessage()
    if recv_data == 0:
        print('Job removed sucsessfully.')
    elif recv_data == -1:
        print('ERROR: Job not found.')

def shutdown(sock, command, data): # tells server to shutdown
    try:
        sock.connect(server_addr)
        trans = protocol.Client(sock)
        trans.sendMessage(command, data)
    except BrokenPipeError:
        print('ERROR: Broken Pipe, Check network connection')
        return -1

if __name__ == '__main__':
    if server_addr == None:
        print('''Please edit this file and set proper server address in server_adder variable.''')
        sys.exit(-2)
    else:
        args = getArgs() # calls argparser
        result = callComms(sock, args) # sends command to server
