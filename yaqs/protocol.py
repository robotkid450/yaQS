#!/usr/bin/env python3
__version__ = '2.3.2'

import struct
import json


class Client:

    def __init__(self, sock):
        self.sock = sock

    def _send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        print("_send_msg msg len", len(msg))
        msg = struct.pack('>I', len(msg)) + msg
        msglen = struct.unpack('>I', msg[:4])#[0]
        print("_send_msg msg raw len", msglen)
        self.sock.sendall(msg)

    def _recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = self._recvall(4)
        print("raw msg len", raw_msglen)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        print(" msg len", msglen)
        return self._recvall(msglen)

    def _recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''.encode()
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


    #end helper functions
    def sendMessage(self, command, data=''): # composes & sends messages
        data_to_json = (command, data)
        data_to_send = json.dumps(data_to_json)
        self._send_msg(data_to_send.encode())


    def recvMessage(self): # recives and decomposes messages
        data_to_decode = self._recv_msg()
        command, data = json.loads(data_to_decode.decode())
        return command, data

class Server:
    def __init__(self, transport, data):
        self.data = data
        self.trans = transport
   
    def _send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        self.trans.write(msg)

    def _recv_msg(self, packed_message):
        # Read message length and unpack it into an integer
        msglen = struct.unpack('>I', packed_message[:4])[0]
        print("server msglenn recev", msglen)
        if not msglen:
            return None
        msg = packed_message[4:msglen+4]
        #print("msg payload follows")
        #print(msg)
        return msg

    def sendMessage(self, command='reply', data=''): # composes & sends messages
        data_to_json = (command, data)
        data_to_send = json.dumps(data_to_json)
        self._send_msg(data_to_send.encode())


    def recvMessage(self): # recives and decomposes messages
        data_to_decode = self._recv_msg(self.data)
        command, data = json.loads(data_to_decode.decode())
        return command, data

