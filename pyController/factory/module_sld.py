

from factory.bit import BIT             # Modbus Bit

#*****************************
#*            SLD            *
#*****************************
class SLD():
    name = "SLD"
    def __init__(self, modbus):
        self.TaskReset =    BIT(819, modbus)
        self.Task1 =        BIT(800, modbus)
        self.status_ready = BIT(808, modbus)
        self.fault_status_1  = BIT(812, modbus) # 812, 813, 814 are faults
        self.fault_status_2  = BIT(813, modbus)
        self.fault_status_3  = BIT(814, modbus)
        #self.reset           = BIT(819, modbus)

    def IsReady(self):
        """ Return True if module is in a ready state """
        return self.status_ready.read()

    def IsFault(self):
        """ Return True if module is in a fault state """
        if self.fault_status_1.read() or self.fault_status_2.read() or self.fault_status_3.read():
            return True
        else:
            return False

    def StartTask1(self):
        """ Start Task 1
        Pickup puck from HBW and deliver to MPO
        """
        self.Task1.set()
        self.Task1.clear()
        return 1

    def SLD_Status(self):
        """ Show bit & register statuses """
        print("************************")
        print("*      SLD STATUS      *")
        print("************************")
        print("MC800:  "+str(self.Task1.read()) +"  -Task1")
        print("MC808:  "+str(self.status_ready.read())+"  -status_ready")
        print("MC812:  "+str(self.fault_status_1.read())+"  -fault_status_1")
        print("MC813:  "+str(self.fault_status_2.read())+"  -fault_status_2")
        print("MC814:  "+str(self.fault_status_3.read())+"  -fault_status_3")
        print("************************")
