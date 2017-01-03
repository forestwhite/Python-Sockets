#!/usr/bin/env python3
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    Packet sniffer for the UDP port only, which parses each UDP header
'''

import socket
import struct

def parse_ip(packet):
    header_length_in_bytes = (packet[0] & 0x0F) * 4
    header = packet[0:header_length_in_bytes]
    data = packet[header_length_in_bytes:]
    ip_header = struct.unpack("!BBHHHBBH4s4s", header)
    total_length = ip_header[2]
    protocol = ip_header[6] 
    source_address = socket.inet_ntoa(ip_header[8])
    destination_address = socket.inet_ntoa(ip_header[9])
    return total_length, protocol, source_address, destination_address, data

def parse_udp(packet):
    header = packet[0:8]
    data = packet[8:]
    (source_port, dest_port, 
     data_length, checksum) = struct.unpack("!HHHH", header)
    return source_port, dest_port, data_length, checksum, data

def main():
    #create an INET, raw UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    # receive UDP packets and parse
    while True:
        (total_length, protocol, source_address, 
         destination_address, data) = parse_ip(s.recvfrom(size))
        print("Total Length: {}\nProtocol: {}\n"
          "Source Address: {}\nDestination Address: {}\n".format(
              total_length, protocol, source_address, destination_address))
        print("Source Port: {}\nDestination Port: {}\nData Length: {}\n"
          "Checksum: {}\nData: {}\n".format(parse_udp(data)))

size = 65565

if __name__ == "__main__":
    main()
