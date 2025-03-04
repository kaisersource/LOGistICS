
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
        interface=network_interface, output_file=file,
        bpf_filter=const.ics_filter  # Use ics_filter
    )
    capture.set_debug()
    try:
        for raw_packet in capture.sniff_continuously():
            filtered_packet = filter_tcp(raw_packet)
            if filtered_packet:
                print(filtered_packet)
    except Exception as e:
        print(f"Error during capture: {e}")
    finally:
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

    # Check for industrial protocol ports
    if src_port in [502, 102, 20000, 44818, 34964] or dst_port in [502, 102, 20000, 44818, 34964]:
        return f' Packet Timestamp: {packet_time}'\
               f'\n Protocol type: {protocol}'\
               f'\n Src IP: {src_ip}'\
               f'\n Src Port: {src_port}'\
               f'\n Dst IP: {dst_ip}'\
               f'\n Dst Port: {dst_port}\n'
    else:
        return None 
        
def filter_tcp(packet):
    """
    Parses all industrial protocol packets
    param: raw packet
    return: filtered packet properties
    """
    if hasattr(packet, 'tcp'):
        if packet.tcp.dstport == 502 or packet.tcp.srcport == 502: #modbus check
            results = filter_details(packet)
            return results
        if packet.tcp.dstport == 102 or packet.tcp.srcport == 102: #S7 check
            results = filter_details(packet)
            return results
        #Add more checks here.

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='LOGistICS KaiserSniff')
    parser.add_argument('-I', '--interface',
                            help='e.g. lo, wlan0',
                            default='lo')
    results = parser.parse_args(args)
    return (results.interface)

iface = check_arg(sys.argv[1:])
capture_live_packets(iface)

#output.close()

        
#We might merge pcaps using pcapmerge, then apply pcapfix as subprocess



