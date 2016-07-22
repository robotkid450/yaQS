#!/usr/bin/env python3
import subprocess
import json
import asyncio
udpAddr = ('127.0.0.1', 9999)
tcpAddr = None


class dataClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print('connection_made')
        self.transport = transport
        self.send_message('getJobToRun')

    def data_received(self, data):
        command, job_data = self.recv_message(data)
        print('job recived')
        job_name = job_data[1]
        job_command = job_data[2]
        self.create_command_task(job_name, job_command)

    def connection_lost(self, exc):
        print('client disconnected')


    def send_message(self, command, data=''):
            data_to_encode = (command, data)
            data_to_send = json.dumps(data_to_encode)
            self.transport.write(data_to_send.encode())

    def recv_message(self, raw_data):
        data_to_decode = raw_data.decode()
        command, data = json.loads(data_to_decode)
        return command, data


    def create_command_task(self, name, command):
        loop = asyncio.get_event_loop()
        jobFuture = asyncio.Future()
        asyncio.ensure_future(runJob(command, jobFuture))
        jobFuture.add_done_callback(self.sendRunResult(jobFuture))
        # jobRunnerCoro = loop.create_task(runJob(command))
        # result = await runJob(command)
        # jobRunnerCoro.add_done_callback(self.sendRunResult)
        # result = await runJob(command)

    def sendRunResult(self, future):
        print(future.result())

@asyncio.coroutine
def runJob(command, future):
    # print('rJ command: ', command)
    print('running job')
    # result = subprocess.run(command, shell=True)
    result = 1
    future.set_result(result)
    # print(result)
    # return result


class dispatchReciver():
    """docstring for dispatchReciver"""
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        if message == 'discover':
            global tcpAddr
            tcpAddr = addr[0]
        if message == 'work Available' and tcpAddr != None:
            print(tcpAddr)
            loop = asyncio.get_event_loop()
            dataClientCoro = loop.create_connection(dataClientProtocol, tcpAddr, 9998)
            dataClientFUT = loop.create_task(dataClientCoro)
            dataClientFUT.add_done_callback(self.foo)

    def foo(self, *args):
        print('dataClientCoro done')


loop = asyncio.get_event_loop()
# One protocol instance will be created to serve all client requests
udp_recv = loop.create_datagram_endpoint(
    dispatchReciver, local_addr=udpAddr)
transport, protocol = loop.run_until_complete(udp_recv)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()
