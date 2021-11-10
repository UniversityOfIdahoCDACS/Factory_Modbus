#!/usr/bin/env python
# -*- coding: utf-8 -*-

# write_bit
# write 4 bits to True, wait 2s, write False, restart...
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "129.101.98.246"
SERVER_PORT = 502

c = ModbusClient()

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

toggle = True

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write coils (modbus function 0x01)
    if c.is_open():
        # write 4 bits in modbus address 0 to 3
        print("")
        print("write bits")
        print("----------")
        print("")
        for addr in range(1):
            is_ok = c.write_single_coil(132, toggle)
            if is_ok:
                print("bit #" + str(132) + ": write to " + str(toggle))
            else:
                print("bit #" + str(132) + ": unable to write " + str(toggle))
            time.sleep(0.5)

        time.sleep(1)

        print("")
        print("read bits")
        print("---------")
        print("")
        bits = c.read_coils(120, 131)
        if bits:
            print("bits #0 to 3: "+str(bits))
        else:
            print("unable to read")

    toggle = not toggle
    # sleep 2s before next polling
    time.sleep(1)