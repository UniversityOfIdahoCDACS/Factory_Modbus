

from factory.bit import BIT             # Modbus Bit

#*****************************
#*            MPO            *
#*****************************
class MPO():
    name = "MPO"
    def __init__(self, modbus):
        self.Task1          = BIT(400, modbus) #go
        self.status_manual  = BIT(401, modbus) #manual control mode
        self.status_reset   = BIT(402, modbus) #reset

        self.oven_ligh_status = BIT(500, modbus) #modbus input 400 0ven on light
        self.saw_status =   BIT(501, modbus)
        self.ready_status = BIT(502, modbus)
        self.fault_status = BIT(503, modbus)
        self.light_start =  BIT(504, modbus)
        self.light_end =    BIT(505, modbus)


    def IsReady(self):
        """ Return True if module is in a ready state """
        return self.ready_status.read()

    def IsFault(self):
        """ Return True if module is in a fault state """
        return self.fault_status.read()

    def Reset(self):
        """ Reset Module """
        self.status_reset.pulse()

    def StartTask1(self):
        """ Start Task 1
        Start cooking operation
        """
        self.Task1.set()
        self.Task1.clear()
        return 1

    def StartSensorStatus(self):
        """ Returns the status of light barrier at start """
        return self.light_start.read()

    def EndSensorStatus(self):
        """ Returns the status of light barrier at end """
        return self.light_end.read()

    def MPO_Status(self):
        """ Show bit & register statuses """
        print("************************")
        print("*      MPO STATUS      *")
        print("************************")
        print("Task1: "+str(self.Task1.read()))
        print("status_manual: "+str(self.Task1.read()))
        print("Reset status: "+str(self.status_reset.read()))
        print("Oven Light Status: "+str(self.oven_ligh_status.read()))
        print("Active Saw: "+str(self.saw_status.read()))
        print("Ready: "+str(self.ready_status.read()))
        print("Fault_Status: "+str(self.fault_status.read()))
        print("Start Light Sensor: "+str(self.light_start.read()))
        print("End Light Sensor: "+str(self.light_end.read()))
        print("************************")
