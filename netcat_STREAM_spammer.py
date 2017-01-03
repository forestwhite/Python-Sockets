#!/user/bin/env python3
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    A spam generator: sends spam strings via STREAM socket to localhost:42424
'''
import socket

s=socket.create_connection(("localhost", 42424))
stringbuf = ""
for i in range(0,1000):
    stringbuf = stringbuf + "spam " + str(i) + "\n"
buf = stringbuf.encode("utf-8")
s.sendall(buf)
s.close()
