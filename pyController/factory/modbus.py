"""Modbus handler
This module handles all modbus communications
"""

import time
import os
import logging
from logging.handlers import RotatingFileHandler
from pymodbus.client.sync import ModbusTcpClient
import utilities

#*****************************
#*          MODBUS           *
#*****************************
class MODBUS():
    # REF: https://pymodbus.readthedocs.io/en/latest/readme.html
    def __init__(self, ip, port):
        # Setup logging
        self.logger = logging.getLogger('modbus')
        self.logger.setLevel(logging.DEBUG) # sets default logging level for this module

        # Setup trace debugger
        self.trace_logger = logging.getLogger('modbus_trace')
        self.trace_logger.setLevel(logging.DEBUG) # sets default logging level for this module
        self.trace_logger.propagate = False       # Prevents this logger from outputing to root logger

        # Logger: create rotating file handler
        script_path = os.path.dirname(os.path.realpath(__file__))
        utilities.create_log_dir(script_path + "/logs")
        log_file_path = script_path + "/logs/modbus.log"
        # Create formatter
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')
        # Create File handler
        rfh = RotatingFileHandler(log_file_path)
        rfh.maxBytes = 1024*1024          # maximum size of a log before being rotated
        rfh.backupCount = 2               # how many rotated files to keep
        rfh.setFormatter(formatter)     # set format
        rfh.setLevel(logging.DEBUG)     # set level for file logging
        self.trace_logger.addHandler(rfh)          # add filehandle to logger

        self.logger.info("Modbus connecting")
        self.trace_logger.info("Modbus connecting")

        # Connect to _client
        self._client = ModbusTcpClient(host=ip, port=port)
        self._ip = ip
        self._port = port
        self.connection_check()

        self.logger.info("Modbus Initialized")
        self.trace_logger.info("Modbus Initialized")


    def __del__(self):
        """ Gracefully close Modbus client """
        self._client.close()

    def connection_check(self):
        """ Checks connection to PLC controller
        Raises an exception if connection is closed
        """
        if not self._client.connect():
            print("Unable to connect to %s:%s" % (self._ip, self._port))
            raise Exception("Unable to connecto to PLC controller")
        return True

    def read_coil(self, addr, retry_count=2):
        self.connection_check()
        self.trace_logger.debug("Reading coil %s", str(addr + 1))
        try:
            val = self._client.read_coils(addr, 1)
            val = val.bits
            self.trace_logger.debug(">Reading coil %s,\tVal: %s,\tretry_count: %d", str(addr + 1), str(val), retry_count)
        except ValueError as e:
            self.logger.error(e)
            self.logger.error("Value error occured while reading coil %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Value error occured while reading coil %s", addr)
            return None
        except AttributeError as e:
            # This can occure when _sock is none in client.py
            self.logger.error(e)
            self.logger.error("Attribute error occured while reading coil %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Attribute error occured while reading coil %s", addr)
            val = None


        # val validation & conversion
        if val is None:
            if retry_count > 0:
                log_msg = "None retuned for coil %s" % str(addr + 1)  # The '+1' is to counteract the '-1' fix in Bit class
                self.logger.warning(log_msg)
                time.sleep(0.01)
                val_retry = self.read_coil(addr, retry_count=retry_count-1) # Will return value instead of list
                self.trace_logger.debug(">Retry returned %s", val_retry)
                return val_retry
            else:
                return None
        else:
            return val[0]
    
    def read_discreet_input(self, addr, retry_count=2):
        """ Read discreet input """
        self.connection_check()
        try:
            val = self._client.read_discrete_inputs(addr, 1)
            self.trace_logger.debug("Reading coil %s,\tVal: %s,\tretry_count: %d", str(addr + 1), str(val), retry_count)
        except ValueError as e:
            self.logger.error(e)
            self.logger.error("Value error occured while reading coil %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Value error occured while reading coil %s", addr)
            return False
        except AttributeError as e:
            # This can occure when _sock is none in client.py
            self.logger.error(e)
            self.logger.error("Attribute error occured while reading input %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Attribute error occured while reading input %s", addr)
            val = None

        # val validation & conversion
        if val is None:
            if retry_count > 0:
                log_msg = "None retuned for coil %s" % str(addr + 1)  # The '+1' is to counteract the '-1' fix in Bit class
                self.logger.warning(log_msg)
                time.sleep(0.01)
                val_retry = self.read_discreet_input(addr, retry_count=retry_count-1) # Will return value instead of list
                self.trace_logger.debug(">Retry returned %s", val_retry)
                return val_retry
            else:
                return None
        else:
            return val[0]

    def read_holding_reg(self, addr, retry_count=2):
        self.connection_check()
        try:
            val = self._client.read_holding_registers(addr, 1)
            val = val.registers
            self.trace_logger.debug("Reading reg %s,\tVal: %s,\tretry_count: %d", str(addr + 1), str(val), retry_count)
        except ValueError as e:
            self.logger.error(e)
            self.logger.error("Value error occured while reading Register %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Value error occured while reading Register %s", addr)
            return 0
        except AttributeError as e:
            # This can occure when _sock is none in client.py
            self.logger.error(e)
            self.logger.error("Attribute error occured while reading reg %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Attribute error occured while reading reg %s", addr)
            val = None

        # val validation & conversion
        if val is None:
            if retry_count > 0:
                log_msg = "None retuned for Register %s" % str(addr + 1)  # The '+1' is to counteract the '-1' fix in Bit class
                self.logger.warning(log_msg)
                time.sleep(0.01)
                val_retry = self.read_holding_reg(addr, retry_count=retry_count-1) # Will return value instead of list
                self.trace_logger.debug(">Retry returned %s", val_retry)
                return val_retry
            else:
                return None
        else:
            return val[0]
        
    def read_input_reg(self, addr, retry_count=2):
        self.connection_check()
        try:
            val = self._client.read_input_registers(addr, 1)
            self.trace_logger.debug("Reading reg %s,\tVal: %s,\tretry_count: %d", str(addr + 1), str(val), retry_count)
        except ValueError as e:
            self.logger.error(e)
            self.logger.error("Value error occured while reading Register %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Value error occured while reading Register %s", addr)
            return 0
        except AttributeError as e:
            # This can occure when _sock is none in client.py
            self.logger.error(e)
            self.logger.error("Attribute error occured while reading input reg %s", addr)
            self.trace_logger.error(e)
            self.trace_logger.error("Attribute error occured while reading inputreg %s", addr)
            val = None

        # val validation & conversion
        if val is None:
            if retry_count > 0:
                log_msg = "None retuned for Register %s" % str(addr + 1)  # The '+1' is to counteract the '-1' fix in Bit class
                self.logger.warning(log_msg)
                time.sleep(0.01)
                val_retry = self.read_input_reg(addr, retry_count=retry_count-1) # Will return value instead of list
                self.trace_logger.debug(">Retry returned %s", val_retry)
                return val_retry
            else:
                return None
        else:
            return val[0]

    def write_coil(self, addr, value):
        self.connection_check()
        self.trace_logger.debug("Writing %d to addr %s", value, str(addr + 1))
        responce = self._client.write_coil(addr, value)
        return responce

    def write_reg(self, addr, value):
        self.connection_check()
        self.trace_logger.debug("Writing %d to addr %s", value, str(addr + 1))
        return self._client.write_register(addr, value)
