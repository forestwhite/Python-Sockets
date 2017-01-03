#!/usr/bin/env python3
#author: forestwhite/_kingfisher - https://github.com/forestwhite

'''
    Packet sniffer for all ports, which distinguishes between UDP packets
    and non-UDP packets.

    In a typical network setting, this sniffer reads a lot messages a
    large volument of messages in a short amount of time.
'''

import socket
import struct

def mac_address (address) :
    mac = "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", address)
    return mac

def parse_ethernet(packet):
    header = packet[0:14]
    ethernet_header = struct.unpack("!6s6sH", header)
    ethernet_destination = mac_address(ethernet_header[0])
    ethernet_source = mac_address(ethernet_header[1])
    if(ethernet_header[2] == 0x8100):
        type_code = struct.unpack("!H",packet [16:18])
        data = packet[18:]
    else:
        type_code = ethernet_header[2]
        data = packet[14:]
    return ethernet_source, ethernet_destination, type_code, data

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
    #create an INET, raw socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.ntohs(0x0003))
    # receive packets
    while True:
        (ethernet_source, ethernet_destination, type_code, 
         data) = parse_ethernet(s.recvfrom(size))
        print("Ethernet Source: {}\nEthernet Destination: {}\nType Code: {}\n"
         .format(ethernet_source, ethernet_destination, type_code))
        (total_length, protocol, source_address, 
         destination_address, data) = parse_ip(s.recvfrom(size))
        print("Total Length: {}\nProtocol: {}\n"
          "Source Address: {}\nDestination Address: {}\n".format(
              total_length, protocol, source_address, destination_address))
        # If UDP, parse the header
        if (protocol == 17):
            print("Source Port: {}\nDestination Port: {}\nData Length: {}\n"
             "Checksum: {}\nData: {}\n".format(parse_udp(data)))
        # If not UDP, print raw
        else:
            print("Protocol {} is not UDP\n".format(protocol))

size = 65565

if __name__ == "__main__":
    main()
