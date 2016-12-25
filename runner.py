#!/usr/bin/env python3

__version__ = '2.3.2'
import socketserver, socket
import yaqs.protocol as protocol
import argparse
import subprocess
import logging
import os


def getJob(): # connectes and retrives a job from to server
    root_logger.info("Requesting job.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    root_logger.info('Connection established')
    conn = protocol.Client(sock)
    conn.sendMessage('getJobToRun')
    command, data = conn.recvMessage()
    root_logger.debug('Recived message: command: %s data: %s', command, data)
    if data != -1:
        recv_data = data
        job_ID = recv_data[0]
        job_name = recv_data[1]
        job_command = recv_data[2]
        job_working_directory = recv_data[3]
        sock.close()
        return job_ID, job_name, job_command, job_working_directory
    else:
        root_logger.info("No jobs avalible.")
        return None

def runJob(name, command, working_directory=os.getcwd()): # runs the retrived job
    root_logger.info('Running job : %s', name)
    original_working_directory=os.getcwd()
    if working_directory != None:
        root_logger.debug('Attempting to change to directory : %s', working_directory)
        try:
            os.chdir(working_directory)

        except:
            root_logger.error('Could not change to %s.', working_directory)
            return -9

        else:
            try :
                result = subprocess.check_output(command, shell=True)
                root_logger.debug("Command result: %s", result)

            except:
                root_logger.error("ERROR executing job %s", name)
                return -8

        finally:
            root_logger.debug("Returning to %s", original_working_directory)
            os.chdir(original_working_directory)

    else:
        try:
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            root_logger.debug("Command result: %s", result)

        except:
            root_logger.error("ERROR executing job %s", name)
            return -1

    return result.decode('utf-8')

def submitJobComplete(job_ID, job_name, job_result): # reports completed jobs to server
    root_logger.info("Submitting %s as completed.", job_name)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(tcpAddr)
    root_logger.info('Connection established')
    conn = protocol.Client(sock)
    conn.sendMessage('submitJobComplete', [job_ID, job_result])

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
            tcpAddr = (self.client_address[0], udpAddr[1])
            root_logger.info('Master server found.')
            root_logger.debug('Master server address: %s', str(tcpAddr))

        #recives work avalible broadcast & acts accordingly
        elif data == 'work Available':
            root_logger.info('Work Avalible')
            if tcpAddr == None:
                global tcpAddr
                tcpAddr = (self.client_address[0], udpAddr[1])
                root_logger.info('Master server found.')
                root_logger.debug('Master server address: %s', str(tcpAddr))

            job = getJob()
            if job != None:
                job_ID, job_name, job_command, job_working_directory = job
                result = runJob(job_name, job_command, job_working_directory)
                submitJobComplete(job_ID, job_name, result)

            else:
                pass

        elif data == 'shutdown':
            root_logger.info("Shutting down.")
            sock.close()
            self.stopped = True

def configureLogging(debugMode):
    # Set up logging
    root_logger = logging.getLogger(__name__)
    consoleLogStream = logging.StreamHandler()
    file_log_output = logging.FileHandler('logs/runner.log')

    if debugMode == 'True':
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    logging_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    consoleLogStream.setFormatter(logging_formatter)
    file_log_output.setFormatter(logging_formatter)

    root_logger.addHandler(consoleLogStream)
    root_logger.addHandler(file_log_output)

    return root_logger

def getArgs():
    argParse = argparse.ArgumentParser(
        description='Run yaQS jobs.'
        )

    argParse.add_argument('-p', dest='port', type=int, nargs=1, default=9999,
        help="Port that the runner will use to communicate with the server.")

    argParse.add_argument('-d', dest='debug', action='store_const', const='True',
        default='False', help='Enable debug mode.')

    args = argParse.parse_args()
    return args

if __name__ == "__main__":
    # Creates broadcast reciver
    args = getArgs()

    udpAddr = ("0.0.0.0", args.port[0])
    tcpAddr = None
    
    server = socketserver.UDPServer(udpAddr, UDPhandler)
    root_logger = configureLogging(args.debug)
    root_logger.debug('Debug logging test entry.')

    # starts runner
    try:
        server.serve_forever()
    except ValueError:
        print('shutdown')
