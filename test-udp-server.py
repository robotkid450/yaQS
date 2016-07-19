#! /usr/bin/env python3
import socket
import sys
import json
import uuid
import math

HOST, PORT = "localhost", 9999

udp_buffer = 1024

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def sendMsg(sock_obj, msg):
    sock_obj.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().

def recvMsg(sock):
    received = sock.recv(udp_buffer).decode()
    return received

def sendMsgNew(sock_obj, msg):
    message_ID = str(uuid.uuid4())[:8]
    number_of_packets = 1
    packet_number = 1
    data = [message_ID, number_of_packets, packet_number, msg]
    message_len = len(json.dumps(data))
    print(message_len)
    needed_number_of_packets = int(math.ceil(message_len / udp_buffer))
    if needed_number_of_packets > number_of_packets:
        print('large')
        number_of_packets = needed_number_of_packets

    else:
        print('small')

    num_of_chars_to_store = message_len // number_of_packets
    pos, prev_pos = (0, 0)

    received = []

    for packet in range(number_of_packets):
        msg_part = []
        for item in msg:
            if pos < num_of_chars_to_store:
                msg_part.append(item)
                pos += 1
            else:
                prev_pos = pos
                num_of_chars_to_store += num_of_chars_to_store
                break

        message = ''.join(msg_part)
        data_to_send = json.dumps(
            [message_ID, needed_number_of_packets, packet, message]
        )
        print('sending', packet)
        #sock_obj.sendto(bytes(data_to_send, 'utf-8'), (HOST, PORT))
        sock_obj.sendto(data_to_send.encode(), (HOST, PORT))

    print('finished sending')



#def sendAll()


#def recvMsgNew(sock_obj):


#cmd = sys.argv[1]


#if cmd == 'a':
    #sendMsg(sock, 'addJob')

#data = json.dumps([['a','b','c'],['d','e','f']])
#sendMsg(sock, data)




'''
p1 = []
x=0
for item in cmd:
    x += 1
    if x <= c:
        p1.append(item)

s = ''.join(p1)
s



int(math.ceil(1025/1024))
'''
#sendMsgNew(sock, 'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest')
sendMsgNew(sock, 'asd')
#received = recvMsg(sock)
#received2 = recvMsg(sock)
#print('1', received)
#print('2', received2)
