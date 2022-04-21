""" Modbus bit class
Holds address and methods to set and clear a bit
"""

from time import sleep

class BIT():
    """ Modbus bit class
    Holds address and methods to set and clear a bit
    """
    def __init__(self, addr, modbus):
        self._addr = addr -1    # '-1' is a bugfix to correct address space differences on the PLC
        self._mb = modbus
        self.value = 0


    def set(self):
        """ Writes 1 to this bit """
        self.value = 1
        self._mb.write_coil(self._addr, 1)


    def clear(self):
        """ Writes 0 to this bit """
        self.value = 0
        self._mb.write_coil(self._addr, 0)


    def pulse(self):
        """ Generate a pulse
        This writes 1 to this bit then writes 0 to create a short pulse
        Acts like a very fast momentary button """
        self._mb.write_coil(self._addr, 1)
        sleep(0.007)    # Sleep long enough for a few PLC cycles to pass
        self._mb.write_coil(self._addr, 0)
        self.value = 0


    def read(self):
        """ Read value of this bit """
        value = self._mb.read_coil(self._addr)
        if value is None: # Bad read, return last value
            return self.value
        else:             # Return returned value
            self.value = value
            return value


    def write(self, value):
        """ Write (value) to bit """
        if value > 1:
            value = 1
        self.value = value
        self._mb.write_coil(self._addr, value)


class BIT_DInput():
    """ Bit variant using read discret input """
    def __init__(self, addr, modbus):
        self._addr = addr -1    # '-1' is a bugfix to correct address space differences on the PLC
        self._mb = modbus
        self.value = 0

    def read(self):
        """ Read discret input value of this bit """
        value = self._mb.read_discreet_input(self._addr)
        if value is None: # Bad read, return last value
            return self.value
        else:             # Return returned value
            self.value = value
            return value
