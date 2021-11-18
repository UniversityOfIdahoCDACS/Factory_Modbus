#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "129.101.98.246"
SERVER_PORT = 502

c = ModbusClient()

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

# Variables
choice = ''
coilNumber = 209
#VGR 209
#x MHR101
#y MHR102

#********************************************
#* * * * * * * * * MAIN * * * * * * * * * * *
#********************************************
if __name__ == '__main__':
    
    print("READY")

    while choice != 'q':
        # open or reconnect TCP to server
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

        # if open() is ok, write coils (modbus function 0x01)
        if c.is_open():
            choice = input("Waiting for input: ")
            if choice == '1':
                print("write to coil: " + str(coilNumber))
                is_ok = c.write_single_coil(coilNumber, 1) #True
                #time.sleep(1)
                #is_ok = c.write_single_coil(coilNumber, False)
            elif choice == '2':
                print("write to coil: " + str(coilNumber))
                is_ok = c.write_single_coil(coilNumber, 0) #False
                #time.sleep(1)
                print("Yes")
        time.sleep(1)