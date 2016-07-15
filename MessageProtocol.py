#! /usr/bin/env python3
import struct

class Message(object):
    """docstring for MessageProtocol"""
    def __init__(self, socket):
        self.sock = socket

        # The following functions define a binary protocol used to communicate
        # between the server and its clients

        # A message consists of a 4byte block containing the length of the message
        # followed by the meassage contents

    def send_message_bin(self, msg): # sends binary data !!MUST BE SERIALIZED!!
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        self.sock.sendall(msg)

    def recv_message_bin(self): # recives binary data !!MUST BE SERIALIZED!!
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)


    def send_message(self, msg): # sends strings
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg.encode()
        self.sock.sendall(msg)

    def recv_message(self): # recives strings
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen).decode()

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

if __name__ == '__main__':
    pass
