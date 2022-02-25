from pyModbusTCP.client import ModbusClient
import time

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
                raise Exception ("Unable to connecto to PLC controller")
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
        #print("**************READY STATUS***")
        return self.status_ready.read()

    def CurrentProgress(self):
        return self.cur_progress.read()
    
    def StartTask1(self,x,y):
        self.slot_x.write(x)
        self.slot_y.write(y)
        #Set task one and clear it (simuler to pressing HMI button)
        self.Task1.set()
        self.Task1.clear()
        return 1

    def StartTask2(self,x,y):
        self.slot_x.write(x)
        self.slot_y.write(y)
        #Set task two and clear it (simuler to pressing HMI button)
        self.Task2.set()
        self.Task2.clear()
        return 1

    def HBW_Status(self):
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

#*****************************
#*            VGR            *
#*****************************     
class VGR():
    def __init__(self,modbus):
        self.Reset =        BIT(200,modbus)
        self.Task1 =        BIT(210,modbus)
        self.Task2 =        BIT(220,modbus)
        self.Task3 =        BIT(230,modbus)
        self.Task4 =        BIT(240,modbus)
        self.man_control  = BIT(300,modbus)
        self.mc301 =        BIT(301,modbus)
        self.mc302 =        BIT(302,modbus)
        self.mc303 =        BIT(303,modbus)
        self.mc304 =        BIT(304,modbus)
        self.mc305 =        BIT(305,modbus)
        self.mc306 =        BIT(306,modbus)
        self.mc307 =        BIT(307,modbus)
        self.mc350 =        BIT(350,modbus)
        self.status_ready = BIT(397,modbus)
        self.vgr_b5       = REGISTER(400,modbus)
        self.fault_code   = REGISTER(799,modbus)

    def IsReady(self):
        return self.status_ready.read()
    
    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

    def VGR_Status(self):
        print("************************")
        print("*      VGR STATUS      *")
        print("************************")
        print("Reset: "+str(self.Reset.read()))
        print("Task1: "+str(self.Task1.read()))
        print("Task2: "+str(self.Task2.read()))
        print("Task3: "+str(self.Task3.read()))
        print("Task4: "+str(self.Task4.read()))
        print("man_control: "+str(self.man_control.read()))
        print("mc301: "+str(self.mc301.read()))
        print("mc302: "+str(self.mc302.read()))
        print("mc303: "+str(self.mc303.read()))
        print("mc304: "+str(self.mc304.read()))
        print("mc305: "+str(self.mc305.read()))
        print("mc306: "+str(self.mc306.read()))
        print("mc307: "+str(self.mc307.read()))
        print("mc350: "+str(self.mc350.read()))
        print("status_ready: "+str(self.status_ready.read()))
        print("vgr_b5: "+str(self.vgr_b5.read()))
        print("fault_code: "+str(self.fault_code.read()))
        print("************************")

#*****************************
#*            MPO            *
#*****************************     
class MPO():
    def __init__(self,modbus):
        self.Task1          = BIT(400,modbus) #go
        self.status_manual  = BIT(401,modbus) #manual control mode
        self.status_reset   = BIT(402,modbus) #reset
        '''
        self.mc2   =        BIT(403,modbus) #compressor
        self.mc3   =        BIT(404,modbus) #oven motor in
        self.mc4   =        BIT(405,modbus) #oven motor out
        self.mc5   =        BIT(406,modbus) #oven door
        self.mc6   =        BIT(407,modbus) #vaccum
        self.mc7   =        BIT(408,modbus) #vaccum towards the turn table
        self.mc8   =        BIT(409,modbus) #vaccum towards the oven
        self.mc499 =        BIT(499,modbus)
        '''
        self.oven_ligh_status = BIT(500,modbus) #modbus input 400 0ven on light
        self.saw_status   =        BIT(501,modbus)
        self.ready_status =   BIT(502,modbus)
        self.fault_status   =        BIT(503,modbus)
        self.light_start   =      BIT(504,modbus)
        self.light_end   =        BIT(505,modbus)
        #self.status_flag2 = BIT(52,modbus) #modbus input 401 saw on light
        #self.status_ready = REGISTER(402,modbus) #modbus input 402 ready light
                                            #modbus input 403 fault light
                                            #modbus input 404 start light sensor
                                            #modbus input 405 end light sensor
        #MHR800 oven
        #MHR801 Saw

    def IsReady(self):
        return self.ready_status.read()

    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

    def StartSensorStatus(self):
        return str(self.light_start.read())

    def EndSensorStatus(self):
        return str(self.light_end.read())

    def MPO_Status(self):
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

#*****************************
#*            SLD            *
#*****************************
class SLD():
    def __init__(self,modbus):
        self.Task1 =        BIT(800,modbus)
        #801 - 897 buttons on HMI
        self.mc02  =        BIT(801,modbus) 
        self.mc03  =        BIT(802,modbus) 
        self.mc04  =        BIT(803,modbus) 
        self.mc05  =        BIT(804,modbus) 
        self.mc06  =        BIT(805,modbus) 
        self.mc07  =        BIT(806,modbus) 
        self.mc08  =        BIT(807,modbus) 
        self.status_ready = BIT(808,modbus)
        self.status_white = BIT(809,modbus) # mc809 white, mc810 red, mc811 blue
        self.status_red   = BIT(810,modbus)
        self.status_blue  = BIT(811,modbus)
        self.fault_status_1  = BIT(812,modbus) # 812, 813, 814 are faults
        self.fault_status_2  = BIT(813,modbus)
        self.fault_status_3  = BIT(814,modbus)
        #self.reset           = BIT(819,modbus)
    def IsReady(self):
        #print("HERE: ", self.status_ready.read())
        return self.status_ready.read()
    
    def StartTask1(self):
        self.Task1.set()
        self.Task1.clear()
        return 1

    def SLD_Status(self):
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

    def SSC_Status(self):
        print("************************")
        print("*      SSC STATUS      *")
        print("************************")

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
        self.mpo.StartSensorStatus()
        self.sld.IsReady()
        #self.hbw.HBW_Status()
        
    def order(self, x_value, y_value):
        stage_1_flag = False #HBW -> VGR -> MPO also HBW return pallet
        stage_2_flag = False #
        stage_3_flag = False

        hbw_ready_status = str(self.hbw.IsReady())
        # Run HBW
        if hbw_ready_status == "True":
            print("HBW Is Ready: "+hbw_ready_status)
            self.hbw.StartTask1(x_value, y_value) #HBW STARTS
            stage_1_flag = True
        else:
            print("HBW Is Not Ready: "+hbw_ready_status)
        # Run VGR and HBW return
        while stage_1_flag:
            hbw_ready_status = str(self.hbw.IsReady())
            if str(self.hbw.CurrentProgress()) == "[80]":
                self.vgr.StartTask1() #VGR STARTS
            elif hbw_ready_status == "True":
                time.sleep(2)
                self.hbw.StartTask2(x_value, y_value)#Return Pallet
                stage_1_flag = False
                stage_2_flag = True

        while stage_2_flag:
            mpo_start_light = str(self.mpo.StartSensorStatus())
            if mpo_start_light == "False":
                time.sleep(1)
                self.mpo.StartTask1()#Add values to change 
                stage_2_flag = False
                stage_3_flag = True

        while stage_3_flag:
            mpo_end_light = str(self.mpo.EndSensorStatus())
            #print("stage 3 end light: "+mpo_end_light)
            if mpo_end_light == "False":
                self.sld.StartTask1()
                stage_3_flag = False

    # HBW Factory Logic 
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

    def hbw_status(self):
        self.hbw.HBW_Status()
        return 1
    
    # VGR Factory Logic
    def vgr_task1(self):
        print("Started vgr")
        self.vgr.StartTask1()

    def vgr_status(self):
        self.vgr.VGR_Status()
        return 1

    # MPO Factory Logic
    def mpo_task1(self):
        print("Started mpo")
        self.mpo.StartTask1()

    def mpo_status(self):
        self.mpo.MPO_Status()
        return 1

    # SLD Factory Logic
    def sld_task1(self):
        print("Started sld")
        self.sld.StartTask1()

    def sld_status(self):
        self.sld.SLD_Status()
        return 1

    def restock(self):
        pass

#*****************************
#*          TESTS            *
#*****************************
#factory = FACTORY(ip="0.0.0.0",port=502)

#factory.order()
#factory.status()
#factory.restock()

#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
    #Main is not used
    print("****************************")
    print("* start factory with       *")
    print("* $python3 factoryHMI.py   *")
    print("*            or            *")
    print("* $python3 factoryMQTT.py  *")
    print("****************************")