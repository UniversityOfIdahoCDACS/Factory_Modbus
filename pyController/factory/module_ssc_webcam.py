"""Factory Module: Webcam control """

from factory.register import REGISTER   # Modbus Register
from factory.bit import BIT             # Modbus Bit

#*****************************
#*       SSC_Webcam          *
#*****************************
class SSC_Webcam():
    def __init__(self, modbus):
        self.reset          = BIT(600, modbus) #reset
        self.Task1          = BIT(601, modbus) #Start routine

        self.target_pan     = REGISTER(000, modbus) #pan
        self.target_tilt    = REGISTER(000, modbus) #tilt

        # point table
        self.points = [(100, 100), # Pan, Tilt
                       (200, 200),
                       (300, 300),
                       (400, 400),
                       (500, 500),
                       (600, 600)
                       ]

    def IsReady(self):
        """ Return True if module is in a ready state """
        return True
    
    def IsFault(self):
        """ Return True if module is in a fault state """
        #return self.status_fault.read()
        return None

    def StartTask1(self):
        """ Execute Task 1 """
        self.Task1.set()
        self.Task1.clear()

    def go_to_point(self, point):
        """ Move webcam to point's (pan, tilt) value """
        print("Moving webcam to point #%d with value %s" % (point, str(self.points[point])))
        self.target_pan(self.points[point][0])
        self.target_tilt(self.points[point][1])
