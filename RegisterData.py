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
                regs = c.read_holding_registers(3,10)
                print(regs) 
            elif choice == '2':
                print("Yes")
        time.sleep(1)