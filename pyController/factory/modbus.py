"""Modbus handler
This module handles all modbus communications
"""

import time
import os
import logging
from logging.handlers import RotatingFileHandler
from pyModbusTCP.client import ModbusClient

#*****************************
#*          MODBUS           *
#*****************************
class MODBUS():
    # REF: https://pymodbus.readthedocs.io/en/latest/readme.html
    def __init__(self, ip, port):
        print("Modbus initializing")

        # Setup logging
        self.logger = logging.getLogger('factory_modbus')
        self.logger.setLevel(logging.DEBUG) # sets default logging level for this module

        # Create formatter
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')
        # Logger: create console handle
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)     # set logging level for console
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Setup trace debugger
        self.trace_logger = logging.getLogger('factory_modbus_trace')
        self.trace_logger.setLevel(logging.DEBUG) # sets default logging level for this module

        # Logger: create rotating file handler
        log_file_path = os.path.dirname(os.path.realpath(__file__)) + "/app_rot.log"
        rfh = RotatingFileHandler(log_file_path)
        rfh.maxBytes = 1024*1024          # maximum size of a log before being rotated
        rfh.backupCount = 2               # how many rotated files to keep
        rfh.setFormatter(formatter)     # set format
        rfh.setLevel(logging.DEBUG)     # set level for file logging
        self.trace_logger.addHandler(rfh)          # add filehandle to logger


        # Connect to _client
        self._client = ModbusClient(host=ip, port=port, unit_id=1, auto_open=True)  # Always connect
        self._ip = ip
        self._port = port
        self.connection_check()


    def __del__(self):
        """ Gracefully close Modbus client """
        self._client.close()

    def connection_check(self):
        if not self._client.is_open():
            if not self._client.open():
                print("Unable to connect to %s:%s" % (self._ip, self._port))
                raise Exception("Unable to connecto to PLC controller")
        return True

    def read_coil(self, addr):
        self.connection_check()
        try:
            val = self._client.read_coils(addr, 1)
            #logger.debug("Reading coil %s, Val: %s", addr, str(val))
        except ValueError:
            self.logger.error("Value error occured while readying coil %s", addr)
            return 0

        # val validation & conversion
        if val == "[True]":
            return True
        elif val == "[False]":
            return False
        else:
            print("NOT a bool value while readying coil %s" % addr)
            return False

        return val

    def write_coil(self, addr, value):
        self.connection_check()
        #print ("Writing")
        responce = self._client.write_single_coil(addr, value)
        return responce

    def read_reg(self, addr):
        self.connection_check()
        try:
            response = self._client.read_holding_registers(addr, 1)
        except ValueError:
            self.logger.error("Value error occured while readying reg %s", addr)
            response = [0] # Not great but it prevents the logic from crashing
        #print (f"Modbus read_reg responce: {response}, type: {type(response)}")

        if response is None:
            self.logger.warning("Response is None trying again")
            time.sleep(0.3)
            try:
                response = self._client.read_holding_registers(addr, 1)
            except ValueError:
                self.logger.error("Value error occured while readying reg %s", addr)

            if response is None:
                response = [0]


        try:
            return_val = int(response[0])
        except ValueError:
            print(f"Value error occured while converting to int {addr}")
            return_val = 0

        return return_val

    def write_reg(self, addr, val):
        self.connection_check()
        #print("Modbus write reg value: %r" % val)
        return self._client.write_single_register(addr, val)
