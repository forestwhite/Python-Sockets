#!/usr/bin/env python3
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    A spam listener: listens for spam strings sent via STREAM socket on
                     localhost:42424
'''
import socket

def handle(passedconn):
    data = b""
    newdata = passedconn.recv(size)
    while newdata:
        data += newdata
        newdata = passedconn.recv(size)
    if data:
        datastring = data.decode("utf-8")
        print(handlestring(datastring, len("spam "), "\n"))
    passedconn.close()

def handlestring(datastring, length, delimiter):
    stringlist = datastring.split(sep=delimiter)
    filteredlist = []
    for string in stringlist:
        filteredlist.append(string[length:])
    filteredstring = delimiter.join(filteredlist)
    return filteredstring

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    for i in [1,2,3]:
        conn, clientaddress = s.accept()
        handle(conn)
    s.close()

host = "localhost"
port = 42424
backlog = 5
size = 1024

if __name__ == "__main__":
    main()
