#!/usr/bin/env python3
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    A spam listener: listens for spam strings sent to localhost:42424
'''
import socket

def handlestring(datastring, length, delimiter):
    stringlist = datastring.split(sep=delimiter)
    filteredlist = []
    for string in stringlist:
        filteredlist.append(string[length:])
    filteredstring = delimiter.join(filteredlist)
    return filteredstring

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    data, addr = s.recvfrom(size)
    if data:
        datastring = data.decode("utf-8")
        print(handlestring(datastring, len("spam "), "\n"))    
    s.close()

host = "localhost"
port = 42424
backlog = 5
size = 1024

if __name__ == "__main__":
    main()
