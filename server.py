#!/usr/bin/env python3


__version__ = '1.1.1'
import asyncio
import yaqs_queuemanger.yaqsQueue as yaqsQueue
import json
import sys
import socket
import logging


# debug = True
debug = False

server_addr = ('0.0.0.0', 9999) # production

broadcast_addr = ('255.255.255.255', 9999) # production

discovery_intreval = 10   # time in seconds between discovery broadcasrs
workDispatch_intreval = 1 # time in seconds between workDispatch broadcasts

class UDPBroadcaster(object): # UDP broadcaster class
    """docstring for UDPBroadcaster"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def sendDiscovery(self): # sends discovery broadcast
        self.sock.sendto('discover'.encode(), broadcast_addr)
        logging.debug('sending discover')
        self._stop()

    def sendWorkAvailable(self): # sends work avalible broadcast
        self.sock.sendto('work Available'.encode(), broadcast_addr)
        rootLogger.debug('sending work avalible')
        self._stop()

    def _stop(self): # stops broadcast repeat loop
        self.sock.close()

def workDispatch(): # helper function for workDispatch broadcast
    if queue.getJobsAvailable() > 0:
        rootLogger.debug('work avalibe')
        UB = UDPBroadcaster()
        UB.sendWorkAvailable()
    return 0

def discovery(): # helper function for discovery broadcast
    UB = UDPBroadcaster()
    UB.sendDiscovery()
    return 0


# async Protocol object for data server TCP
class dataServerProtocol(asyncio.Protocol):
    """docstring for MessageProtocol"""
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        rootLogger.info('Connection from {}'.format(peername))
        self.transport = transport
        self.que = queue

    def data_received(self, data):
        message = data.decode()
        rootLogger.debug('Data received: {!r}'.format(message))
        command, cmd_data = json.loads(message)
        rootLogger.debug('command %s', command)
        rootLogger.debug('cmd_data %s', cmd_data)
        if command == 'addJob': #adds jobs to queue
            job_to_add = cmd_data
            result = self.que.addJob(job_to_add[0], job_to_add[1], job_to_add[2])
            rootLogger.info('added job : %s', job_to_add[0])
            self.send_message(data=result)

        elif command == 'getAllJobs': # gets all jobs currently in system
            rootLogger.debug('getting jobs')
            all_jobs = self.que.getAllJobs()
            self.send_message(data=all_jobs)

        elif command == 'getJobInfo': # get all information on a job
            rootLogger.debug('job info request')
            job_ID = cmd_data
            job_Info = self.que.getJobInfo(job_ID)
            self.send_message(data=job_Info)

        elif command == 'removeJob': # removes a job from queue DOES NOT STOP
            job_ID = cmd_data        # RUNNING JOB!!
            rootLogger.info('removing job:', job_ID)
            result = self.que.removeJob(job_ID)
            self.send_message(data=result)

        elif command == 'getJobToRun': # gets next job from queue
            rootLogger.debug('Run job request')
            job_to_run = self.que.getJobToRun()
            rootLogger.info('sending job: %s', job_to_run)
            self.send_message(data=job_to_run)

        elif command == 'submitJobComplete': # removes job from running list
            rootLogger.info('Job submitted as complete.')
            self.que.markRunningJobComplete(cmd_data[0])

        elif command == 'shutdown': # remotely kills server
            rootLogger.info('Shutdown command recived.')
            self.transport.close()
            self.quitter()

        else:
            rootLogger.warn('invalid command') # replies to invalid commands
            self.send_message(data='invalid command')

        self.transport.close()

    def connection_lost(self, exc): # executed on connection loss
        rootLogger.info('client disconnected')
        queue = self.que


    # helper functions
    def send_message(self, command='reply', data=''):# composes & sends messages
            data_to_encode = (command, data)
            data_to_send = json.dumps(data_to_encode)
            self.transport.write(data_to_send.encode())

    def quitter(self): # helper funcyion for shutdown command
        loop.stop()


class PeriodicTask(object): # base for tasks that run periodicly ex. broadcasts
    def __init__(self, func, interval):
        self.func = func
        print(func)
        self.interval = interval
        self._loop = asyncio.get_event_loop()
        self._set()
    def _set(self):
        self._handler = self._loop.call_later(self.interval, self._run)
    def _run(self):
        funcOut = self.func()
        self._set()
        return funcOut

    def _stop(self):
        self._handler.cancel()


if __name__ == '__main__':
    # Set up logging
    rootLogger = logging.getLogger(__name__)
    # consoleLogStream = logging.StreamHandler()
    fileLogOutput = logging.FileHandler('server.log')

    if debug == True:
        rootLogger.setLevel(logging.DEBUG)
    else:
        rootLogger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # consoleLogStream.setFormatter(formatter)
    fileLogOutput.setFormatter(formatter)

    # rootLogger.addHandler(consoleLogStream)
    rootLogger.addHandler(fileLogOutput)

    # Create storage queue
    queue = yaqsQueue.QueueData()

    # Create asyncio loop
    loop = asyncio.get_event_loop()
    # Create data Server Coroutine
    dataServerCoroutine = loop.create_server(
        dataServerProtocol, server_addr[0], server_addr[1])
    # run data Server Coroutine
    dataServer = loop.run_until_complete(dataServerCoroutine)
    # Create and run broadcasts
    dispatchServer = PeriodicTask(workDispatch, workDispatch_intreval)
    discoverServer = PeriodicTask(discovery, discovery_intreval)
    # Send initial discovery broadcast
    discovery()

    # Serve requests until Ctrl+C is pressed
    rootLogger.info('Serving on {}'.format(dataServer.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        rootLogger.info('Shutting down.')

    # Close the server
    dataServer.close()
    dispatchServer._stop()
    loop.run_until_complete(dataServer.wait_closed())
    loop.close()
