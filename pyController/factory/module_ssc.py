

from factory.bit import BIT             # Modbus Bit

#*****************************
#*           SSC             *
#*****************************
class SSC():
    name = "SSC"
    def __init__(self, modbus):
        self.GLED = BIT(60, modbus)
        self.YLED = BIT(61, modbus)
        self.RLED = BIT(62, modbus)

    def LEDclear(self):
        self.GLED.clear()
        self.YLED.clear()
        self.RLED.clear()

    def LEDset(self, g, y, r):
        # No input validation. g,y,r shoud be 1 or 0
        if g:
            self.GLED.set()
        else:
            self.GLED.clear()

        if y:
            self.YLED.set()
        else:
            self.YLED.clear()

        if r:
            self.RLED.set()
        else:
            self.RLED.clear()

    def SSC_Status(self):
        """ Show bit & register statuses """
        print("************************")
        print("*      SSC STATUS      *")
        print("************************")
