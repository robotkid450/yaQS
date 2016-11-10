def _send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def _recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def _recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data



def sendMessage(sock, command, data=''): # composes & sends messages
    data_to_json = (command, data)
    data_to_send = json.dumps(data_to_encode)
    _send_msg(sock, data_to_send.encode())
    #sock.send(data_to_send.encode())

def recvMessage(sock): # recives and decomposes messages
    data_to_decode = _recv_msg(sock)
    command, data = json.loads(data_to_decode)
    return command, data


