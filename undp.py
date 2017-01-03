#! /usr/bin/env python
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    An unreliable channel that forwards messages recieved on [myport] to [srvport]
    with a pseudo-random number of corrupted messages determined by the [corrupt%]
    corruption rate.

    To be used with rdtecho.py to demonstrate corruption response.

    Usage: python unrel.py [my port] [srv port] [corrupt%])
'''

import sys
from socket import *
from random import randint

BUFSIZE = 1024

def main():
    if len(sys.argv) < 4:
        usage()
    else:
        forward()

def usage():
    sys.stdout = sys.stderr
    print('Usage: python undp.py [my port] [srv port] [corrupt%]')
    sys.exit(2)

def corrupt(message,corruption):
    if corruption > randint(0,99):
        message = 'Your message is corrupt!!!'
        print('Undp: Corrupting message...')
    return message

def forward():
    myport = eval(sys.argv[1])
    srvport = eval(sys.argv[2])
    corruption = eval(sys.argv[3])
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('127.0.0.1', myport))
    print('Unreliable transport channel ready, listening on port', myport,
          ', providing reliable delivery to port', srvport)
    while 1:
        data, addr = s.recvfrom(BUFSIZE)
        print('Undp: received %r from %r' % (data.decode('utf8'), addr))
        message = corrupt(data.decode('utf8'),corruption)
        if addr[1] != srvport:
            cliport = addr[1]
            print('Undp: forwarding to', srvport, '\n')
            s.sendto(message.upper().encode('utf-8'), (addr[0],srvport))
        else:
            print('Undp: forwarding to', cliport, '\n')
            s.sendto(message.upper().encode('utf-8'), (addr[0],cliport))

main()
