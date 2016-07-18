#!/usr/bin/env python3
# coding=utf-8

import asyncio
import yaqsQueue
import json
import sys
import struct


class MessenagerProtocal(asyncio.Protocol):
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

    def quitter(self):
        loop.stop()

    # helper functions
    def send_message(self, command='reply', data=''):
            data_to_encode = (command, data)
            data_to_send = json.dumps(data_to_encode)
            self.transport.write(data_to_send.encode())

    # def send_message_bin(self, msg): # sends binary data !!MUST BE SERIALIZED!!
    #     # Prefix each message with a 4-byte length (network byte order)
    #     msg = struct.pack('>I', len(msg)) + msg
    #     self.transport.write(msg)
    #
    # def recv_message_bin(self): # recives binary data !!MUST BE SERIALIZED!!
    #     # Read message length and unpack it into an integer
    #     raw_msglen = self.recvall(4)
    #     if not raw_msglen:
    #         return None
    #     msglen = struct.unpack('>I', raw_msglen)[0]
    #     # Read the message data
    #     return self.recvall(msglen)
    #
    #
    # def send_message(self, msg): # sends strings
    #     # Prefix each message with a 4-byte length (network byte order)
    #     msg = struct.pack('>I', len(msg)) + msg.encode()
    #     self.transport.write(msg)
    #
    # def recv_message(self): # recives strings
    #     # Read message length and unpack it into an integer
    #     raw_msglen = self.recvall(4)
    #     if not raw_msglen:
    #         return None
    #     msglen = struct.unpack('>I', raw_msglen)[0]
    #     # Read the message data
    #     return self.recvall(msglen).decode()
    #
    # def recvall(self, n):
    #     # Helper function to recv n bytes or return None if EOF is hit
    #     data = b''
    #     while len(data) < n:
    #         packet = self.transport.read(n - len(data))
    #         if not packet:
    #             return None
    #         data += packet
    #     return data
    #

if __name__ == '__main__':
    #create storage queue
    queue = yaqsQueue.QueueData()

    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(MessenagerProtocal, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
