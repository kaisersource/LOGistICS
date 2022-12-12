#!/usr/bin/env python
'''
KaiserSource  
'''
#---------------------------------------------------------------------------# 
# import various server implementations
#---------------------------------------------------------------------------# 
from pymodbus import datastore
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.asynchronous import StartUdpServer
from pymodbus.server.asynchronous import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

from twisted.internet.task import LoopingCall

import sys
import logging
import argparse
import socket

import numpy as np
#---------------------------------------------------------------------------# 
# configure server parameters
#---------------------------------------------------------------------------# 

import template_selector as ts


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Set Modbus server parameters.')
    parser.add_argument('-H','--host',
                        help='IP address',
                        default='')
    parser.add_argument('-P', '--port',
                        help='port of the Modbus slave',
                        default='502')
    parser.add_argument('-T', '--template',
                        help='default 1: Schneider',
                        default='1')
  
    results = parser.parse_args(args)
    return (results.host, results.port,results.template)


#---------------------------------------------------------------------------# 
# callback processes for simulating register updating on its own
#---------------------------------------------------------------------------# 

# increments holding regsiters register #0x0 
def updating_writer(a):
    logging.debug("Updating registers...")
    context = a[0]
    slaveid = 0x00
    holdingRegister = 3
    coil = 1
    
    # access holding registers addr 0 - 3 = drums 1 - 4 
    drumsAddress = 0x0
    drums = context[slaveid].getValues(holdingRegister, drumsAddress, count=4)
    # access coils addr 0 - 3 = pumps 1 - 4 
    pumpsAddress = 0x0
    pumps = context[slaveid].getValues(coil, pumpsAddress, count=4)

    # access coils addr 10 - 11 = input and output valves respectively
    valvesAddress = 0x0a # dec 10 = hex 0x0a
    valves = context[slaveid].getValues(coil, valvesAddress, count=2)


    
    
    # update drums 
    if valves[0] == True: 
        drums[1] +=1
    
    if valves[1] == True:
        drums[0] -=1

    if pumps[0] == True:
        if drums[0] > 0:
            drums[1] += 1
            drums[0] -=1
       
    if pumps[1] == True:
        if drums[2] > 0:
            drums[0] += 1
            drums[2] -= 1
    if pumps[2] == True:
        if drums[3] > 0:
            drums[2] += 1
            drums[3] -=1
    if pumps[3] == False:
        if drums[1] > 0:
            drums[3] +=1
            drums[1] -=1
            
    for i in range(0,4):
        if drums[i] >= 50:
            drums[i] = 50
        if drums[i] <= 0:
            drums[i] = 0

    context[slaveid].setValues(holdingRegister, drumsAddress, drums)


   

def log_to_dest(a):
    context = a[0]
    slaveid = 0x00
    holdingRegister = 3
    coil = 1
    
  
    drumsAddress = 0x0
    drums = context[slaveid].getValues(holdingRegister, drumsAddress, count=4)

    pumpsAddress = 0x0
    pumps = context[slaveid].getValues(coil, pumpsAddress, count=4)

    valvesAddress = 0x0a # dec 10 = hex 0x0a
    valves = context[slaveid].getValues(coil, valvesAddress, count=2)

    for i in range(0,4):
        logging.info("PLC Status: Drum level: " + str(i+1) + " coil number: " + str(drums[i]))
        if pumps[i]:
            pumps[i] = 'On'
        else:
            pumps[i] = 'Off'
        logging.info("PLC Status: Pump number: " + str(i+1) + " coil status: " + pumps[i])

    for i in range(0,2):
        if valves[i]:
            valves[i] = 'On'
        else:
            valves[i] = 'Off'








"New Function"
"Assigns template to Modbus Identity "
def set_Template(idt,t):
    
    #Invoking template selector according to t value
    my_selector= ts.selector(t)
    
    t=int(t)
  
    idt.VendorName,idt.ProductCode,idt.VendorUrl,idt.ProductName,idt.ModelName,idt.MajorMinorRevision = my_selector
   


'''
   La funzione selector oltre a garantire estensibilita' del template, rende anche la personalizzazione semplice tramite un file 
   csv. In letteratura questa feature e' unica. Inoltre tramite l'uso della libreria pandas si ovvia all'uso degli if in cascata 
   che rende il codice macchinoso e esteticamente.

    if t == 1:
        idt.VendorName,idt.ProductCode,idt.VendorUrl,idt.ProductName,idt.ModelName,idt.MajorMinorRevision = tp.template_1
    elif t == 2:
        idt.VendorName,idt.ProductCode,idt.VendorUrl,idt.ProductName,idt.ModelName,idt.MajorMinorRevision = tp.template_2
    elif t == 3:
        idt.VendorName,idt.ProductCode,idt.VendorUrl,idt.ProductName,idt.ModelName,idt.MajorMinorRevision = tp.template_3
    elif t == 4:
        idt.VendorName,idt.ProductCode,idt.VendorUrl,idt.ProductName,idt.ModelName,idt.MajorMinorRevision = tp.template_4

    else:
        idt.VendorName,idt.ProductCode,idt.VendorUrl,idt.ProductName,idt.ModelName,idt.MajorMinorRevision = tp.template_1

'''



def run_Serv(h,p,t):
	
    log = logging.getLogger()
    #logging.basicConfig(filename='log_asynchro_srv.log')
    #logging.FileHandler('log_ser.log')
    log.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    #---------------------------------------------------------------------------# 
    # Initialize coils and registers
    #---------------------------------------------------------------------------# 
    #Tuple of registers
    store = ModbusSlaveContext(
    #1-bit (Boolean) registers
    di = ModbusSequentialDataBlock(0, [True]*20),
    co = ModbusSequentialDataBlock(0, (83, 103, 85, 107, 88, 112, 50, 115, 53, 118, 56, 121, 47, 66, 63, 69)),
    #16-bits registers
    hr = ModbusSequentialDataBlock(0,(20,20,20,20,20,20,80,71,84,123, 104, 111, 108, 100, 95, 109, 121, 95, 98, 101, 101, 114, 125)),
    ir = ModbusSequentialDataBlock(0,(20,20,20,20,20,20,104,116,116,112,115,58,47,47,116, 101, 114, 109, 115, 97, 110, 100, 99, 111, 110, 100, 105, 116, 105, 111, 110, 115, 46, 103, 97, 109,101,47)))
    
    context = ModbusServerContext(slaves=store, single=True)
  
    
    #Invoke template
    #Todo : istantiate multiple profiles 
   
   
   
    idt = ModbusDeviceIdentification()

    set_Template(idt,t)
  

    time_loop0 = 500
    time_loop1 = 500
    loop0 = LoopingCall(f=log_to_dest, a=(context,))
    loop1 = LoopingCall(f=updating_writer, a=(context,))
    loop0.start(time_loop0, now=True)
    loop1.start(time_loop1, now=True)
    StartTcpServer(context, identity=idt, address=(h, int(p)))


#---------------------------------------------------------------------------# 
# Start running the server
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    h, p, t = check_arg(sys.argv[1:])
    run_Serv(h,p,t)
    

