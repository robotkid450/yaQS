#!/usr/bin/env python3
# coding=utf-8

import asyncio
import yaqsQueue
import json
import sys
import struct
import socket


class dataServerProtocol(asyncio.Protocol):
    """docstring for MessageProtocol"""
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.que = queue

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        command, cmd_data = json.loads(message)
        print('command', command)
        print('cmd_data', cmd_data)
        if command == 'addJob': #adds jobs to queue
            print('adding Job')
            job_to_add = cmd_data
            self.que.addJob(job_to_add[0], job_to_add[1], job_to_add[2])
            print('added job :', job_to_add[0])
            self.send_message(data='1')

        elif command == 'getAllJobs':
            print('getting jobs')
            all_jobs = self.que.getAllJobs()
            self.send_message(data=all_jobs)

        elif command == 'getJobInfo':
            print('job info request')
            job_ID = cmd_data
            job_Info = self.que.getJobInfo(job_ID)
            self.send_message(data=job_Info)

        elif command == 'removeJob':
            print('job remove request')
            job_ID= cmd_data
            print('removing job:', job_ID)
            result = self.que.removeJob(job_ID)
            self.send_message(data=result)

        elif command == 'shutdown':
            self.transport.close()
            self.quitter()

        else:
            print('invalid command')
            self.send_message(data='invalid command')

        self.transport.close()

    def connection_lost(self, exc):
        print('con lost')
        queue = self.que


    # helper functions
    def send_message(self, command='reply', data=''):
            data_to_encode = (command, data)
            data_to_send = json.dumps(data_to_encode)
            self.transport.write(data_to_send.encode())

    def quitter(self):
        #used to remotly kill server
        loop.stop()


class PeriodicTask(object):
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
        # self.func()
        self._set()
        return funcOut

    def _stop(self):
        self._handler.cancel()

def workDispatch():

    return 0

if __name__ == '__main__':
    #create storage queue
    queue = yaqsQueue.QueueData()

    message = "Hello World!"

    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    dataServerCoroutine = loop.create_server(dataServerProtocol, '127.0.0.1', 9998)
    dataServer = loop.run_until_complete(dataServerCoroutine)
    dispatchServer = PeriodicTask(workDispatch, 1)


    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(dataServer.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    dataServer.close()
    dispatchServer._stop()
    loop.run_until_complete(dataServer.wait_closed())
    loop.close()
