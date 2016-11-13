#!/usr/bin/env python3


__version__ = '2.3.2'
import asyncio
import yaqs.queue as yaqsQueue
import yaqs.protocol as protocol
#import json
import sys
import socket
import logging


# debug = True
debug = False

server_addr = ('0.0.0.0', 9999) # production

broadcast_addr = ('255.255.255.255', 9999) # production

discovery_intreval = 10   # time in seconds between discovery broadcasrs
work_dispatch_intreval = 1 # time in seconds between workDispatch broadcasts

class UDPBroadcaster(object): # UDP broadcaster class
    """docstring for UDPBroadcaster"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def sendDiscovery(self): # sends discovery broadcast
        self.sock.sendto('discover'.encode(), broadcast_addr)
        logging.debug('Sending Discovery packet.')
        self._stop()

    def sendWorkAvailable(self): # sends work avalible broadcast
        self.sock.sendto('work Available'.encode(), broadcast_addr)
        root_logger.debug('Sending work avalible.')
        self._stop()

    def sendShutdown(self): # sends work avalible broadcast
        self.sock.sendto('shutdown'.encode(), broadcast_addr)
        root_logger.debug('Sending shutdown.')
        self._stop()

    def _stop(self): # stops broadcast repeat loop
        self.sock.close()

def workDispatch(): # helper function for workDispatch broadcast
    if queue.getJobsAvailable() > 0:
        root_logger.debug('Work Avalibe')
        UDP_broadcaster = UDPBroadcaster()
        UDP_broadcaster.sendWorkAvailable()
    return 0

def discovery(): # helper function for discovery broadcast
    UDP_broadcaster = UDPBroadcaster()
    UDP_broadcaster.sendDiscovery()
    return 0


# async Protocol object for data server TCP
class dataServerProtocol(asyncio.Protocol):
    """docstring for MessageProtocol"""
    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peer_name')
        root_logger.info('Connection from {}'.format(peer_name))
        self.transport = transport
        self.que = queue

    def data_received(self, data):
        conn = protocol.Server(self.transport, data)
        command, cmd_data = conn.recvMessage()
        #root_logger.debug('Data received: {!r}'.format(message))
        #command, cmd_data = json.loads(message)
        root_logger.debug('command %s', command)
        root_logger.debug('cmd_data %s', cmd_data)
        if command == 'addJob': #adds jobs to queue
            job_to_add = cmd_data
            if job_to_add[3] !=0:
                result = self.que.addJob(
                    job_to_add[0], job_to_add[1], job_to_add[2], job_to_add[3]
                    )
            else:
                result = self.que.addJob(
                    job_to_add[0], job_to_add[1], job_to_add[2], None
                    )
            root_logger.info('added job : %s', job_to_add[0])
            conn.sendMessage(data=result)

        elif command == 'getAllJobs': # gets all jobs currently in system
            root_logger.debug('getting jobs')
            all_jobs = self.que.getAllJobs()
            conn.sendMessage(data=all_jobs)

        elif command == 'getJobInfo': # get all information on a job
            root_logger.debug('job info request')
            job_ID = cmd_data
            job_Info = self.que.getJobInfo(job_ID)
            conn.sendMessage(data=job_Info)

        elif command == 'removeJob': # removes a job from queue
            job_ID = cmd_data        # DOES NOT STOP RUNNING JOB!!
            root_logger.info('removing job: %s', job_ID)
            result = self.que.removeJob(job_ID)
            conn.sendMessage(data=result)

        elif command == 'getJobToRun': # gets next job from queue
            root_logger.debug('Run job request')
            job_to_run = self.que.getJobToRun()
            root_logger.info('sending job: %s', job_to_run)
            conn.sendMessage(data=job_to_run)

        elif command == 'submitJobComplete': # removes job from running list
            root_logger.info('Job submitted as complete.')
            root_logger.info('cmd id : %s ', cmd_data[0])
            self.que.markRunningJobComplete(cmd_data[0], cmd_data[1])

        elif command == 'shutdown': # remotely kills server
            root_logger.info('Shutdown command recived.')
            self.transport.close()
            self.quitter()

        else:
            root_logger.warn('invalid command recived') # replies to invalid commands
            conn.sendMessage(data='invalid command')

        self.transport.close()

    def connection_lost(self, exc): # executed on connection loss
        root_logger.info('client disconnected')
        queue = self.que


    # helper functions
    def quitter(self): # helper funcyion for shutdown command
        UDP_broadcaster = UDPBroadcaster()
        UDP_broadcaster.sendShutdown()
        loop.stop()


class PeriodicTask(object): # base for tasks that run periodicly ex. broadcasts
    def __init__(self, func, interval):
        self.func = func
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


def configureLogging():
    # Set up logging
    root_logger = logging.getLogger(__name__)
    # consoleLogStream = logging.StreamHandler()
    file_log_output = logging.FileHandler('server.log')

    if debug == True:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # consoleLogStream.setFormatter(logging_formatter)
    file_log_output.setFormatter(logging_formatter)

    # root_logger.addHandler(consoleLogStream)
    root_logger.addHandler(file_log_output)

    return root_logger

if __name__ == '__main__':

    # run configure logging
    root_logger = configureLogging()

    # Create storage queue
    queue = yaqsQueue.QueueData()

    # Create asyncio loop
    loop = asyncio.get_event_loop()
    # Create data Server Coroutine
    data_server_coroutine = loop.create_server(
        dataServerProtocol, server_addr[0], server_addr[1])
    # run data Server Coroutine
    data_server = loop.run_until_complete(data_server_coroutine)
    # Create and run broadcasts
    dispatch_server = PeriodicTask(workDispatch, work_dispatch_intreval)
    discover_server = PeriodicTask(discovery, discovery_intreval)
    # Send initial discovery broadcast
    discovery()

    # Serve requests until Ctrl+C is pressed
    root_logger.info('Serving on {}'.format(data_server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        root_logger.info('Shutting down.')

    # Close the server
    data_server.close()
    loop.run_until_complete(data_server.wait_closed())
    loop.close()
