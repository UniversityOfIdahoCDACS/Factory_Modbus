"""Factory Module: Vacuume Gripper Robot """

from factory.register import REGISTER   # Modbus Register
from factory.bit import BIT             # Modbus Bit

#*****************************
#*            VGR            *
#*****************************
class VGR():
    name = "VGR"
    def __init__(self, modbus):
        self.Reset =        BIT(200, modbus)
        self.Task1 =        BIT(210, modbus)
        self.Task2 =        BIT(220, modbus)
        self.Task3 =        BIT(230, modbus)
        self.Task4 =        BIT(240, modbus)
        self.status_ready = BIT(397, modbus)
        self.vgr_b5       = REGISTER(400, modbus)
        self.fault_code   = REGISTER(799, modbus)

    def IsReady(self):
        """ Return True if module is in a ready state """
        return self.status_ready.read()

    def IsFault(self):
        """ Return True if module is in a fault state """
        value = self.fault_code.read()
        if value > 0: 
            return True
        else:
            return False

    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

    def VGR_Status(self):
        """ Show bit & register statuses """
        print("************************")
        print("*      VGR STATUS      *")
        print("************************")
        print("Reset: "+str(self.Reset.read()))
        print("Task1: "+str(self.Task1.read()))
        print("Task2: "+str(self.Task2.read()))
        print("Task3: "+str(self.Task3.read()))
        print("Task4: "+str(self.Task4.read()))
        print("status_ready: "+str(self.status_ready.read()))
        print("vgr_b5: "+str(self.vgr_b5.read()))
        print("fault_code: "+str(self.fault_code.read()))
        print("************************")
