

from factory.bit import BIT             # Modbus Bit

#*****************************
#*            SLD            *
#*****************************
class SLD():
    name = "SLD"
    def __init__(self, modbus):
        self.Task1 =        BIT(800, modbus)
        #801 - 897 buttons on HMI
        self.mc02  =        BIT(801, modbus)
        self.mc03  =        BIT(802, modbus)
        self.mc04  =        BIT(803, modbus)
        self.mc05  =        BIT(804, modbus)
        self.mc06  =        BIT(805, modbus)
        self.mc07  =        BIT(806, modbus)
        self.mc08  =        BIT(807, modbus)
        self.status_ready = BIT(808, modbus)
        self.status_white = BIT(809, modbus) # mc809 white, mc810 red, mc811 blue
        self.status_red   = BIT(810, modbus)
        self.status_blue  = BIT(811, modbus)
        self.fault_status_1  = BIT(812, modbus) # 812, 813, 814 are faults
        self.fault_status_2  = BIT(813, modbus)
        self.fault_status_3  = BIT(814, modbus)
        #self.reset           = BIT(819, modbus)

    def IsReady(self):
        """ Return True if module is in a ready state """
        return self.status_ready.read()

    def IsFault(self):
        """ Return True if module is in a fault state """
        if self.fault_status_1.read():
            return True
        elif self.fault_status_2.read():
            return True
        elif self.fault_status_3.read():
            return True
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
        print("MC801:  "+str(self.mc02.read()))
        print("MC802:  "+str(self.mc03.read()))
        print("MC803:  "+str(self.mc04.read()))
        print("MC804:  "+str(self.mc05.read()))
        print("MC805:  "+str(self.mc06.read()))
        print("MC806:  "+str(self.mc07.read()))
        print("MC807:  "+str(self.mc08.read()))
        print("MC808:  "+str(self.status_ready.read())+"  -status_ready")
        print("MC809:  "+str(self.status_white.read())+"  -status_white")
        print("MC810:  "+str(self.status_red.read())+"  -status_red")
        print("MC811:  "+str(self.status_blue.read())+"  -status_blue")
        print("MC812:  "+str(self.fault_status_1.read())+"  -fault_status_1")
        print("MC813:  "+str(self.fault_status_2.read())+"  -fault_status_2")
        print("MC814:  "+str(self.fault_status_3.read())+"  -fault_status_3")
        #print("MC819:  "+str(self.reset.read())+"  -reset")
        # REGISTERS
        # number in temp storage 1601 1602 1603
        # dump extras number 1604
        print("************************")
