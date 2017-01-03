#! /usr/bin/env python
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    Client and server for udp (datagram) echo that demonstrates reliable
    data transfer with ACKs, sequence numbers, and corruption responses.

    Dropped packets occur in most network mediums.
    Undp.py can introduced demo corrupted messages.

    Usage: udpecho -s [port]            (to start a server)
    or:    udpecho -c host [port] <file (client)
'''

import sys
from socket import *

ECHO_PORT = 50000 + 7
BUFSIZE = 1024
corruptstring = 'Your message is corrupt!!!'

def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        client()
    else:
        usage()

def usage():
    sys.stdout = sys.stderr
    print('Usage: python rdtecho.py -s [port]           (to run server)')
    print('or:    python rdtecho.py -c [port]           (to run client)')
    sys.exit(2)

def server():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = ECHO_PORT
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', port))
    serversequence = 0;
    lastmessage = 'no message'
    print('Server: udp echo server ready')
    while 1:
        data, addr = s.recvfrom(BUFSIZE)
        sequence = data[0] - 48 #utf-8 for 0 is 48, 1 is 49
        if(sequence == serversequence):
            print('Server: recieved DATA message %r with SEQNUM %d' % (data[2:].decode('UTF-8'), sequence))
            #Correct sequence, insert last good message and change serversequence
            lastmessage = data[2:].decode('UTF-8');
            serversequence = int(not(serversequence))
        elif (sequence == int(not(serversequence))):
            #Not the sequence we wanted, change nothing
            print('Server: recieved DATA message %r with SEQNUM %d' % (data[2:].decode('UTF-8'), sequence))
        else:
            #Corrupted message, change nothing
            print('Server: server received corrupted message from' + str(addr))
        #For all scenerios, send ACK for last good message on last sequence recieved
        packet = str(int(not(serversequence))) + 'A' + lastmessage;
        print('Server: sending ACK message %r with SEQNUM %d \n' % (lastmessage,  int(not(serversequence))))
        s.sendto(packet.upper().encode('utf-8'), addr)

def client():
    if len(sys.argv) < 2:
        usage()
    host = '127.0.0.1'
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = ECHO_PORT
    print("using port",port)
    addr = (host, port)
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    clientsequence = 0;
    print('Client: udp echo client ready, reading stdin')
    while 1:
        line = sys.stdin.readline()
        datapacket = str(clientsequence) + 'D' + line
        print("Client: sending", line)
        if not line:
            break
        #Send/receive until we get an ACK
        while(True):
            s.sendto(datapacket.encode('utf-8'), addr)
            data, fromaddr = s.recvfrom(BUFSIZE)
            if(data[1] == 65): #utf-8 for 'A' is decimal 65
                break
        sequence = data[0] - 48 #utf-8 for '0' is decimal 48, '1' is decimal 49
        while(sequence != clientsequence):
            if(sequence == int(not(clientsequence))):
                #Not the sequence we wanted, change nothing, resend message
                print('Client: recieved ACK message %r with SEQNUM %d' % (data[2:].decode('UTF-8'), sequence))
                print('Client: server did not receive the last message - resend last message.')
            else:
                print('Client: recieved CORRUPT message %r' % (data.decode('UTF-8')))
                #Corrupted message, change nothing, resend message
                print('Client: client and/or server received corrupted message - resend last message.')
            s.sendto(datapacket.encode('utf-8'), addr)
            data, fromaddr = s.recvfrom(BUFSIZE)
            sequence = data[0] - 48 #utf-8 for 0 is 48, 1 is 49
        print('Client: recieved ACK message %r with SEQNUM %d' % (data[2:].decode('UTF-8'), sequence))
        print('Client: server successfully received the last message - send next message. \n')
        #Correct sequence, change clientsequence
        clientsequence = int(not(clientsequence))

main()
