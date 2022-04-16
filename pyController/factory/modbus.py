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
        log_file_path = os.path.dirname(os.path.realpath(__file__)) + "/modbus.log"
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
        """ Checks connection to PLC controller
        Raises an exception if connection is closed
        """
        if not self._client.is_open():
            if not self._client.open():
                print("Unable to connect to %s:%s" % (self._ip, self._port))
                raise Exception("Unable to connecto to PLC controller")
        return True

    def read_coil(self, addr, retry_count=2):
        self.connection_check()
        try:
            val = self._client.read_coils(addr, 1)
            #self.logger.debug("Reading coil %s, Val: %s", addr, str(val[0]))
        except ValueError as e:
            self.logger.error(e)
            self.logger.error("Value error occured while readying coil %s", addr)
            return False

        # val validation & conversion
        if val is None:
            if retry_count > 0:
                log_msg = "None retuned for coil %s" % str(addr + 1)  # The '+1' is to counteract the '-1' fix in Bit class
                self.logger.warning(log_msg)
                time.sleep(0.01)
                val_retry = self.read_coil(addr, retry_count=retry_count-1) # Will return value instead of list

                # Test
                if val_retry is None:
                    if retry_count < 2:
                        # This is a retry call. Return None
                        return None
                    else:
                        # This is the main call. Return value as all retries have returned None
                        return False # Return False value as a default
                else:
                    # log_msg = f"rc: {retry_count} | r.out | type: {type(val_retry)} | value: {val_retry}"
                    # self.logger.info(log_msg)
                    return val_retry
        else:
            return val[0]


    def write_coil(self, addr, value):
        self.connection_check()
        #print ("Writing")
        responce = self._client.write_single_coil(addr, value)
        return responce

    def read_reg(self, addr, retry_count=2):
        self.connection_check()
        try:
            val = self._client.read_coils(addr, 1)
            #self.logger.debug("Reading Register %s, Val: %s", addr, str(val[0]))
        except ValueError as e:
            self.logger.error(e)
            self.logger.error("Value error occured while readying Register %s", addr)
            return 0

        # val validation & conversion
        if val is None:
            if retry_count > 0:
                log_msg = "None retuned for Register %s" % str(addr + 1)  # The '+1' is to counteract the '-1' fix in Bit class
                self.logger.warning(log_msg)
                time.sleep(0.01)
                val_retry = self.read_reg(addr, retry_count=retry_count-1) # Will return value instead of list

                # Test
                if val_retry is None:
                    if retry_count < 2:
                        # This is a retry call. Return None
                        return None
                    else:
                        # This is the main call. Return value as all retries have returned None
                        return 0 # Return False value as a default
                else:
                    # log_msg = f"rc: {retry_count} | r.out | type: {type(val_retry)} | value: {val_retry}"
                    # self.logger.info(log_msg)
                    return val_retry
        else:
            return val[0]


    def write_reg(self, addr, val):
        self.connection_check()
        #print("Modbus write reg value: %r" % val)
        return self._client.write_single_register(addr, val)
