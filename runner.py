#!/usr/bin/env python3
import subprocess
import json
import asyncio
udpAddr = ('127.0.0.1', 9999)
tcpAddr = None


class dataClientProtocol():
    def connection_made(self, transport):
        print('connection_made')
        self.transport = transport
        self.transport.write('getJobToRun'.encode())

    def data_received(self, data):
        print(data)


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
            dataClientFUT = asyncio.async(dataClientCoro)
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
