"""Factory Module: Webcam control """

from factory.register import REGISTER   # Modbus Register
from factory.bit import BIT             # Modbus Bit

#*****************************
#*       SSC_Webcam          *
#*****************************
class SSC_Webcam():
    name = "SSC_Webcam"
    def __init__(self, modbus):
        self._TaskReset      = BIT(600, modbus) #reset
        self._Task1          = BIT(601, modbus) #Start routine
        self._status_ready   = BIT(000, modbus) # Ready status flag
        self._status_fault   = BIT(000, modbus) # Fault status flag

        self._target_pan     = REGISTER(000, modbus) #pan
        self._target_tilt    = REGISTER(000, modbus) #tilt

        # point table
        self._points = [(100, 100), # Pan, Tilt
                       (200, 200),
                       (300, 300),
                       (400, 400),
                       (500, 500),
                       (600, 600)
                       ]

    def IsReady(self):
        """ Return True if module is in a ready state """
        return self._status_ready.read()

    def IsFault(self):
        """ Return True if module is in a fault state
        Not implemented for this module
        """
        return False

    def StartTask1(self):
        """ Execute Task 1 """
        self._Task1.pulse()

    def go_to_point(self, point):
        """ Move webcam to point's (pan, tilt) value """
        if self.IsReady():
            print("Moving webcam to point #%d with value %s" % (point, str(self._points[point])))
            self._target_pan(self._points[point][0])
            self._target_tilt(self._points[point][1])
            self._Task1.pulse()
