from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QSpinBox
from apscheduler.schedulers.background import BackgroundScheduler
from pyModbusTCP.client import ModbusClient
from PyQt5 import uic
import FactoryUI
import time
import sys

#*****************************
#*          MODBUS           *
#*****************************
class MODBUS():
    # REF: https://pymodbus.readthedocs.io/en/latest/readme.html
    def __init__(self,ip,port):
        print ("Modbus initializing")
        # Connect to Client
        self.client = ModbusClient(host=ip,port=port,unit_id=1, auto_open=True)  # Always connect 
        self.ip = ip
        self.port = port
    
    def __del__(self):
        #self.client.close()
        pass
    
    def connection_check(self):
        if not self.client.is_open():
            if not self.client.open():
                print ("Unable to connect to %s:%d" % (self.ip, self.port))
                raise "Unable to connecto to PLC controller"
        return True
    
    def refresh(self):
        #pull from modbus
        pass
    
    def send(self):
        print ("Sending")

    def read_coil(self,addr):
        self.connection_check()
        #print ("Reading")
        return self.client.read_coils(addr,1)

    def write_coil(self,addr,value):
        self.connection_check()
        #print ("Writing")
        responce = self.client.write_single_coil(addr,value)
        return responce
        
    def read_reg(self,addr):
        self.connection_check()
        response =  self.client.read_holding_registers(addr,1)
        #print ("Modbus read_reg responce: %r" % response)
        return response
    
    def write_reg(self,addr,val):
        self.connection_check()
        #print("Modbus write reg value: %r" % val)
        return self.client.write_single_register(addr, val)

#***********************************
#*               BIT               *
#* Modbus connection info (modbus) *
#* and coil number (addr) are      *
#* passed into here to write and   *
#* read from a coil                *
#***********************************
class BIT():
    def __init__(self,addr,modbus):
        self.addr = addr -1
        self.value = 0
        self.mb = modbus
    
    # 'set' writes 1 (True) to a given modbus coil (addr)
    def set(self):
        self.value = 1
        return self.mb.write_coil(self.addr, 1)

    # 'clear' writes 0 (False) to a given modbus coil (addr)
    def clear(self):
        self.value = 0
        self.mb.write_coil(self.addr, 0)

    ''' # like set or clear but the user can define the value
    def write(self, value):
        self.value = value
        self.mb.write_coil(self.addr, value)
    '''
    # 'read' reads a coil at the (addr)
    def read(self):
        #print ("BIT Val: %r" % self.value)
        self.value = str(self.mb.read_coil(self.addr))
        if self.value == "[True]":
            return True
        elif self.value == "[False]":
            return False
        else:
            print("NOT a bool value")
            return self.value

#***********************************
#*              REGISTER           *
#* Modbus connection info (modbus) *
#* and register number (addr) are  *
#* passed into here to write and   *
#* read from a register            *
#***********************************
class REGISTER():
    def __init__(self,addr,modbus):
        self.addr = addr -1
        self.value = 0
        self.mb = modbus
    
    def write(self,value):
        self.value = value
        self.mb.write_reg(self.addr, value)
    
    def read(self):
        self.value = str(self.mb.read_reg(self.addr))
        #print ("REG Val: %r" % self.value)
        return self.value

#*****************************
#*           HBW             *
#*****************************    
class HBW():
    def __init__(self,modbus):
        self.Task1 =        BIT(101,modbus)
        self.Task2 =        BIT(102,modbus)
        self.Task3 =        BIT(103,modbus)
        self.slot_x =       REGISTER(105,modbus)
        self.slot_y =       REGISTER(106,modbus)
        self.status_ready = BIT(130,modbus)
        self.cur_progress = REGISTER(131,modbus)
        self.status_fault = BIT(180,modbus)
        self.fault_code   = REGISTER(181,modbus)

    def IsReady(self):
        #print("**************ADD READS***")
        return self.status_ready.read()
    
    def StartTask1(self,x,y):
        # wait or verify
        self.slot_x.write(x)
        self.slot_y.write(y)
        # wait or verify
        #Set task one and clear it (simuler to pressing HMI button)
        self.Task1.set()
        self.Task1.clear()
        return 1

    def StartTask2(self,x,y):
        # wait or verify
        self.slot_x.write(x)
        self.slot_y.write(y)
        # wait or verify
        #Set task two and clear it (simuler to pressing HMI button)
        self.Task2.set()
        self.Task2.clear()
        return 1

    def HBW_Status(self):
        print("Task1: "+str(self.Task1.read()))
        print("Task2: "+str(self.Task2.read()))
        print("Task3: "+str(self.Task3.read()))
        print("slot_x: "+str(self.slot_x.read()))
        print("slot_y: "+str(self.slot_y.read()))
        print("status_ready: "+str(self.status_ready.read()))
        print("cur_progress: "+str(self.cur_progress.read()))
        print("status_fault: "+str(self.status_fault.read()))
        print("fault_code: "+str(self.fault_code.read()))

#*****************************
#*            VGR            *
#*****************************     
class VGR():
    def __init__(self,modbus):
        self.Task1 =        BIT(210,modbus) #210, 220, 230, 240
        #self.Task2 =        BIT(54,modbus)
        self.status_ready = BIT(397,modbus)
        #self.status_flag1 = BIT(51,modbus)
        #self.status_flag2 = BIT(52,modbus)
        
    def IsReady(self):
        return self.status_ready.read()
    
    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

    def VGR_Status(self):
        print("Task1: "+str(self.Task1.read()))
        print("Task2: "+str(self.Task2.read()))
        print("Task3: "+str(self.Task3.read()))
        print("slot_x: "+str(self.slot_x.read()))
        print("slot_y: "+str(self.slot_y.read()))
        print("status_ready: "+str(self.status_ready.read()))
        print("cur_progress: "+str(self.cur_progress.read()))
        print("status_fault: "+str(self.status_fault.read()))
        print("fault_code: "+str(self.fault_code.read()))

#*****************************
#*            MPO            *
#*****************************     
class MPO():
    def __init__(self,modbus):
        self.Task1 =        BIT(400,modbus)
        self.status_ready = BIT(402,modbus)
        #self.status_flag1 = BIT(51,modbus)
        #self.status_flag2 = BIT(52,modbus)

    def IsReady(self):
        return self.status_ready.read()
    
    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1
    
    def EndTask1(self):
        self.Task1.clear()
        return 1

#*****************************
#*            SLD            *
#*****************************
class SLD():
    def __init__(self,modbus):
        self.Task1 =        BIT(800,modbus)
        self.status_ready = BIT(808,modbus)
        self.status_flag1 = BIT(809,modbus) # mc809 white, mc810 red, mc811 blue,  812, 813, 814 are faults
        #self.status_flag2 = BIT(52,modbus) 

    def IsReady(self):
        #print("HERE: ", self.status_ready.read())
        return self.status_ready.read()
    
    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

#*****************************
#*           SSC             *
#*****************************
class SSC():
    def __init__(self,modbus):
        self.GLED = BIT(60,modbus)
        self.YLED = BIT(61,modbus)
        self.RLED = BIT(62,modbus)

    def LEDclear(self):
        self.GLED.clear()
        self.YLED.clear()
        self.RLED.clear()
    
    def LEDset(self,g,y,r):
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

#*****************************
#*         FACTORY           *
#*****************************
class FACTORY():
    def __init__(self, ip, port):
        self.mb = MODBUS(ip, port)
        self.hbw = HBW(self.mb)
        self.vgr = VGR(self.mb)
        self.mpo = MPO(self.mb)
        self.sld = SLD(self.mb)
        self.ssc = SSC(self.mb)
        print("ready stuff here")
        #check ready status
        self.hbw.IsReady()
        self.vgr.IsReady()
        self.mpo.IsReady()
        self.sld.IsReady()
        #self.hbw.HBW_Status()
    
    def status(self):
        self.hbw.HBW_Status()
        return 1
        
    
    def order(self, x_value, y_value):
        run_flag = False

        ready_status = str(self.hbw.IsReady())
        if ready_status == "True":
            print("HBW Is Ready: "+ready_status)
            self.hbw.StartTask1(x_value, y_value)
            run_flag = True
        else:
            print("HBW Is Not Ready: "+ready_status)
        #run factory
        while run_flag:
            if str(self.hbw.IsReady()) == "True":
                self.vgr.StartTask1()#Add values to change 
                time.sleep(29)
                self.hbw.StartTask2(x_value, y_value)
                self.mpo.StartTask1()#Add values to change 
                time.sleep(38)
                self.sld.StartTask1()#Add values to change
                time.sleep(4)
                run_flag = False
            
    def hbw_task1(self, x_value, y_value):
        ready_status = str(self.hbw.IsReady())
        if ready_status == "True":
            print("HBW Is Ready: "+ready_status)
            self.hbw.StartTask1(x_value, y_value)
        else:
            print("HBW Is Not Ready: "+ready_status)

    def hbw_task2(self, x_value, y_value):
        ready_status = str(self.hbw.IsReady())
        if ready_status == "True":
            print("HBW Is Ready: "+ready_status)
            self.hbw.StartTask2(x_value, y_value)
        else:
            print("HBW Is Not Ready: "+ready_status)
    
    def vgr_task1(self):
        print("Started vgr")
        self.vgr.StartTask1()

    def mpo_task1(self):
        print("Started mpo")
        self.mpo.StartTask1()

    def sld_task1(self):
        print("Started sld")
        self.sld.StartTask1()

    def restock(self):
        pass

#*****************************
#*          TESTS            *
#*****************************
#factory = FACTORY(ip="192.101.98.246",port=502)

#factory.order()
#factory.status()
#factory.restock()
'''
# Quick test object to validate modbus communications
c = MODBUS("129.101.98.246", 502)
b = BIT(101, c)
v = REGISTER(101,c)

b.set()
b.read()
b.clear()
print(b.read())

v.write(5)
v.read()
v.write(2)
print(v.read())
'''

#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
    #Initialize UI App
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()