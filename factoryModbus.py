from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QSpinBox
from pyModbusTCP.client import ModbusClient
from PyQt5 import uic
import FactoryUI
import time
import sys

#*****************************
#*            UI             *
#*****************************
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        mb = MODBUS('129.101.98.246', 502)
        self.hbw = HBW(mb)
        self.vgr = VGR(mb)
        self.mpo = MPO(mb)
        self.sld = SLD(mb)
        #check ready status
        self.hbw.IsReady()
        self.vgr.IsReady()
        self.mpo.IsReady()
        self.sld.IsReady()

        #Load UI File
        uic.loadUi("FactoryUI.ui", self)

        #Define Widgets
        self.spinBoxX = self.findChild(QSpinBox, "spinBox_x")
        self.spinBoxY = self.findChild(QSpinBox, "spinBox_y")
        self.t1button_hbw = self.findChild(QPushButton, "pushButton")
        self.t2button_hbw = self.findChild(QPushButton, "pushButton_2")
        self.t1button_vgr = self.findChild(QPushButton, "pushButton_4")
        self.t1button_mpo = self.findChild(QPushButton, "pushButton_3")
        self.t1button_sld = self.findChild(QPushButton, "pushButton_5")

        #Actions
        self.t1button_hbw.clicked.connect(self.hbw_t1_clicker)
        self.t2button_hbw.clicked.connect(self.hbw_t2_clicker)
        self.t1button_vgr.clicked.connect(self.vgr_t1_clicker)
        self.t1button_mpo.clicked.connect(self.mpo_t1_clicker)
        self.t1button_sld.clicked.connect(self.sld_t1_clicker)
        
        #Show App
        self.show()

    # Actions when the HBW task 1 button is clicked
    def hbw_t1_clicker(self):  
        print(self.spinBoxX.cleanText())
        x_value = int(self.spinBoxX.cleanText())
        print(self.spinBoxY.cleanText())
        y_value = int(self.spinBoxY.cleanText())

        if self.hbw.IsReady():
            self.hbw.StartTask1(x_value, y_value)
        return 1

    # Actions when the HBW task 2 button is clicked
    def hbw_t2_clicker(self):
        print(self.spinBoxX.cleanText())
        x_value = int(self.spinBoxX.cleanText())
        print(self.spinBoxY.cleanText())
        y_value = int(self.spinBoxY.cleanText())

        if self.hbw.IsReady():
            self.hbw.StartTask2(x_value, y_value)
        return 1

    # Actions when the vgr task 1 button is clicked
    def vgr_t1_clicker(self):
        if self.vgr.IsReady():
            self.vgr.StartTask1()#Add values to change 
        return 1

    # Actions when the MPO task 1 button is clicked
    def mpo_t1_clicker(self):
        if self.mpo.IsReady():
            self.mpo.StartTask1()#Add values to change 
        return 1

    # Actions when the SLD task 1 button is clicked
    def sld_t1_clicker(self):
        if self.sld.IsReady():
            self.sld.StartTask1()#Add values to change 
        return 1

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
        print ("Reading")
        return self.client.read_coils(addr,1)

    def write_coil(self,addr,value):
        self.connection_check()
        print ("Writing")
        responce = self.client.write_single_coil(addr,value)
        return responce
        
    def read_reg(self,addr):
        self.connection_check()
        response =  self.client.read_holding_registers(addr,1)
        print ("Modbus read_reg responce: %r" % response)
        return response
    
    def write_reg(self,addr,val):
        self.connection_check()
        print("Modbus write reg value: %r" % val)
        return self.client.write_single_register(addr, val)

#*****************************
#*            BIT            *
#*****************************
class BIT():
    def __init__(self,addr,modbus):
        self.addr = addr -1
        self.value = 0
        self.mb = modbus
    
    def set(self):
        self.value = 1
        return self.mb.write_coil(self.addr, 1)
    
    def clear(self):
        self.value = 0
        self.mb.write_coil(self.addr, 0)

    def write(self, value):
        self.value = value
        self.mb.write_coil(self.addr, value)

    def read(self):
        self.value = self.mb.read_coil(self.addr)
        print ("BIT Val: %r" % self.value)
        return self.value

#*****************************
#*         REGISTER          *
#*****************************
class REGISTER():
    def __init__(self,addr,modbus):
        self.addr = addr -1
        self.value = 0
        self.mb = modbus
    
    def write(self,value):
        self.value = value
        self.mb.write_reg(self.addr, value)
    
    def read(self):
        self.value = self.mb.read_reg(self.addr)
        #print ("REG Val: %r" % self.value)
        return self.value
    
#*****************************
#*           HBW             *
#*****************************    
class HBW():
    def __init__(self,modbus):
        self.Task1 =        BIT(101,modbus)
        self.Task2 =        BIT(102,modbus)
        self.slot_x =       REGISTER(105,modbus)
        self.slot_y =       REGISTER(106,modbus)
        self.status_ready = BIT(130,modbus)
        self.status_fault = BIT(180,modbus)
        self.fault_code   = REGISTER(181,modbus)

    def IsReady(self):
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

#*****************************
#*            VGR            *
#*****************************     
class VGR():
    def __init__(self,modbus):
        self.Task1 =        BIT(201,modbus)
        #self.Task2 =        BIT(54,modbus)
        self.status_ready = BIT(202,modbus)
        #self.status_flag1 = BIT(51,modbus)
        #self.status_flag2 = BIT(52,modbus)
        
    def IsReady(self):
        return self.status_ready.read()
    
    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

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
        #self.Task1.clear()
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
        print("HERE: ", self.status_ready.read())
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
        self.mpo = MPO(self.mb)
        self.ssc = SSC(self.mb)
    
    def status(self):
        return "We're working on it. Please wait"
    
    def order(self):
        pass
    
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
    #mb = MODBUS('129.101.98.246', 502)
    # mb = simbus() # Simulator

    #hbw = HBW(mb)
    #mpo = MPO(mb)
    #ssc = SSC(mb)

    #hbw.Reset()
    #hbw.IsReady()
    #hbw.IsFault()

    #if hbw.IsReady():
        #hbw.StartTask1(1,2)

    #Initialize UI App
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

    #if all are ready with no faults then run make an order
    # HBW(x,y) task1 -> VGR task1 -> MPO(disk color) task1 -> SSC task1

    '''
    if mpo.IsReady():
        mpo.StartTask1()
    '''
    # Control/read a bit directly
    #hbw.slot_x.write(5)
    #val = hbw.status_flag1.read()
    '''
    ssc.LEDset(1,0,1)
    ssc.LEDclear()
    ssc.GLED.set()
    '''
