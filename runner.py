#!/usr/bin/env python3
import subprocess
import json
import asyncio
UDPADDR = ('127.0.0.1', 9999)
TCPADDR = None


class dataClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        


class dispatchReciver():
    """docstring for dispatchReciver"""
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        if message == 'discover':
            global TCPADDR
            TCPADDR = (addr, 9998)
        if message == 'work Available' and TCPADDR != None:
            loop = asyncio.get_event_loop()
            dataClientCoro = loop.create_connection(dataClientProtocol, TCPADDR)


loop = asyncio.get_event_loop()
# One protocol instance will be created to serve all client requests
UDP_RECV = loop.create_datagram_endpoint(
    dispatchReciver, local_addr=UDPADDR)
transport, protocol = loop.run_until_complete(UDP_RECV)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()
