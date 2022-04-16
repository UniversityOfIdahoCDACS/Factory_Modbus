"""Factory Module: High Bay Warehouse """

from factory.register import REGISTER   # Modbus Register
from factory.bit import BIT             # Modbus Bit

#*****************************
#*           HBW             *
#*****************************
class HBW():
    name = "HBW"
    def __init__(self, modbus):
        self.Task1 =        BIT(101, modbus)
        self.Task2 =        BIT(102, modbus)
        self.Task3 =        BIT(103, modbus)
        self.slot_x =       REGISTER(105, modbus)
        self.slot_y =       REGISTER(106, modbus)
        self.status_ready = BIT(130, modbus)
        self.cur_progress = REGISTER(131, modbus)
        self.status_fault = BIT(180, modbus)
        self.fault_code   = REGISTER(181, modbus)

    def IsReady(self):
        """ Return True if module is in a ready state """
        return self.status_ready.read()

    def IsFault(self):
        """ Return True if module is in a fault state """
        return self.status_fault.read()

    def CurrentProgress(self):
        """ Return the current task progress
        Returns integer between 0 and 100
        """
        return self.cur_progress.read()

    def StartTask1(self, x, y):
        """ Start Task 1
        Deliver Pallet to conveyor
        """
        self.slot_x.write(x)
        self.slot_y.write(y)
        #Set task one and clear it (simuler to pressing HMI button)
        self.Task1.set()
        self.Task1.clear()
        return 1

    def StartTask2(self, x, y):
        """ Start Task 2
        Retrieve Pallet from conveyor
        """
        self.slot_x.write(x)
        self.slot_y.write(y)
        #Set task two and clear it (simuler to pressing HMI button)
        self.Task2.set()
        self.Task2.clear()
        return 1

    def HBW_Status(self):
        """ Show bit & register statuses """
        print("************************")
        print("*      HBW STATUS      *")
        print("************************")
        print("*Task1: "+str(self.Task1.read()))
        print("*Task2: "+str(self.Task2.read()))
        print("*Task3: "+str(self.Task3.read()))
        print("*slot_x: "+str(self.slot_x.read()))
        print("*slot_y: "+str(self.slot_y.read()))
        print("*status_ready: "+str(self.status_ready.read()))
        print("*cur_progress: "+str(self.cur_progress.read()))
        print("*status_fault: "+str(self.status_fault.read()))
        print("*fault_code: "+str(self.fault_code.read()))
        print("************************")
