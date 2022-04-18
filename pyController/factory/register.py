""" Modbus register class
Holds address and methods to write and read from a register
"""

class REGISTER():
    """ Modbus bit class
    Holds address and methods to write and read from a register
    """
    def __init__(self, addr, modbus):
        self._addr = addr -1    # '-1' is a bugfix to correct address space differences on the PLC
        self._mb = modbus
        self.value = 0


    def read(self):
        """ Read value of this register """
        self.value = self._mb.read_reg(self._addr)
        return self.value


    def write(self, value):
        """ Write (value) to register """
        self.value = value
        self._mb.write_reg(self._addr, value)
