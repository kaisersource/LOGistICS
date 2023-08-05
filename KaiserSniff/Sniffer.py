
#!/usr/bin/env python

import os
import sys
import signal
import subprocess
import pyshark as ps
import datetime
import signal
import asyncio
import constants as const
import threading
import argparse

date = datetime.datetime.now()
name = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

file = "Captures/"+date.isoformat()+ ".pcapng"
output = open(file,"w")

def capture_live_packets(network_interface): 
    
    """
    This function is designed to read live ICS traffic from a chosen interface
    parameter interface: wlan0, lo etc.
    """
    capture = ps.LiveCapture(
        interface=network_interface,output_file=file,
        bpf_filter = const.L7_filter
        )
    
    #capture.sniffc(timeout=time)
    capture.set_debug()

    
    for raw_packet in capture.sniff_continuously():
        print(filter_tcp(raw_packet))  
    capture.clear()
    capture.close()
    
def filter_details(packet):
    """
    This function is designed to parse specific details from an individual packet.
    parameter packet: gets raw pcap file
    return: specific packet details
    """
    packet_time = packet.sniff_time
    protocol = packet.transport_layer
    src_ip = packet.ip.src
    src_port = packet[packet.transport_layer].srcport
    dst_ip = packet.ip.dst
    dst_port = packet[packet.transport_layer].dstport
    #fc = packet.mbtcp.modbus.func_code
    
    if (src_port == 80):
        return f' Packet Timestamp: {packet_time}'\
           f'\n Protocol type: {protocol}'\
           f'\n Src IP: {src_ip}'\
           f'\n Src Port: {src_port}'\
           f'\n Dst IP: {dst_ip}'\
           f'\n Dst Port: {dst_port}'
           #f'\n Function Code: {fc}\n'
    else:
        return f' Packet Timestamp: {packet_time}'\
           f'\n Protocol type: {protocol}'\
           f'\n Src IP: {src_ip}'\
           f'\n Src Port: {src_port}'\
           f'\n Dst IP: {dst_ip}'\
           f'\n Dst Port: {dst_port}\n'
        
def filter_tcp(packet):
    """
    Parses all TCP packets
    param: raw packet
    return: filtered packet properties
    """
    if hasattr(packet, 'tcp'):
       results = filter_details(packet)
       return results

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='LOGistICS KaiserSniffer')
    parser.add_argument('-I', '--interface',
                            help='e.g. lo, wlan0',
                            default='lo')
    results = parser.parse_args(args)
    return (results.interface)

iface = check_arg(sys.argv[1:])
capture_live_packets(iface)

#output.close()

        
#We might merge pcaps using pcapmerge, then apply pcapfix as subprocess



