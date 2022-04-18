"""Factory Module: SSC-LED """

from factory.bit import BIT             # Modbus Bit

#*****************************
#*           SSC             *
#*****************************
class SSC_LED():
    name = "SSC_LED"
    def __init__(self, modbus):
        self.GLED = BIT(60, modbus)
        self.YLED = BIT(61, modbus)
        self.RLED = BIT(62, modbus)

    def LEDclear(self):
        """ Turn off all LEDs """
        self.GLED.clear()
        self.YLED.clear()
        self.RLED.clear()

    def LEDset(self, g, y, r):
        """ Sets LEDs from g y r bits """
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

    def IsReady(self):
        """ Return True if module is in a ready state
        Not implemented for this module
        """
        return True

    def IsFault(self):
        """ Return True if module is in a fault state
        Not implemented for this module
        """
        return False

    def SSC_Status(self):
        """ Show bit & register statuses """
        print("************************")
        print("*      SSC STATUS      *")
        print("************************")
        print("GLED:  %s" % str(self.GLED.read()))
        print("YLED:  %s" % str(self.YLED.read()))
        print("RLED:  %s" % str(self.RLED.read()))
