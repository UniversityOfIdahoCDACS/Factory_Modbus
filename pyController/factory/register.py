""" Modbus register class
Holds address and methods to write and read from a register
"""

class REGISTER():
    """ Modbus Register class
    Holds address and methods to write and read from a register
    """
    def __init__(self, addr, modbus):
        self._addr = addr -1    # '-1' is a bugfix to correct address space differences on the PLC
        self._mb = modbus
        self.value = 0


    def read(self):
        """ Read value of this register """
        value = self._mb.read_holding_reg(self._addr)
        if value is None: # Bad read, return last value
            return self.value
        else:             # Return returned value
            self.value = value
            return value


    def write(self, value):
        """ Write (value) to register """
        self.value = value
        self._mb.write_reg(self._addr, value)


class REGISTER_Input():
    """ Modbus Holding Register class
    Holds address and methods to read from a holding register
    """
    def __init__(self, addr, modbus):
        self._addr = addr -1    # '-1' is a bugfix to correct address space differences on the PLC
        self._mb = modbus
        self.value = 0

    def read(self):
        """ Read value of this register """
        value = self._mb.read_input_reg(self._addr)
        if value is None: # Bad read, return last value
            return self.value
        else:             # Return returned value
            self.value = value
            return value
