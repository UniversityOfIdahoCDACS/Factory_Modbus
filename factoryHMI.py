from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QSpinBox
from apscheduler.schedulers.background import BackgroundScheduler
from pyModbusTCP.client import ModbusClient
import factoryModbus as fm
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
        self.factory = fm.FACTORY('129.101.98.246', 502)
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
        self.button_start = self.findChild(QPushButton, "pushButton_6")

        #Actions
        self.t1button_hbw.clicked.connect(self.hbw_t1_clicker)
        self.t2button_hbw.clicked.connect(self.hbw_t2_clicker)
        self.t1button_vgr.clicked.connect(self.vgr_t1_clicker)
        self.t1button_mpo.clicked.connect(self.mpo_t1_clicker)
        self.t1button_sld.clicked.connect(self.sld_t1_clicker)
        self.button_start.clicked.connect(self.start_clicker)
        
        #Show App
        self.show()

    # Actions when the HBW task 1 button is clicked
    def hbw_t1_clicker(self):  
        #print(self.spinBoxX.cleanText())
        #print(self.spinBoxY.cleanText())
        x_value = int(self.spinBoxX.cleanText())
        y_value = int(self.spinBoxY.cleanText())
        self.factory.hbw_task1(x_value, y_value)
        return 1

    # Actions when the HBW task 2 button is clicked
    def hbw_t2_clicker(self):
        #print(self.spinBoxX.cleanText())
        #print(self.spinBoxY.cleanText())
        x_value = int(self.spinBoxX.cleanText())
        y_value = int(self.spinBoxY.cleanText())
        self.factory.hbw_task2(x_value, y_value)
        return 1

    # Actions from FACTORY class when the vgr task 1 button is clicked
    def vgr_t1_clicker(self):    
        self.factory.vgr_task1()
        return 1

    # Actions from FACTORY class when the MPO task 1 button is clicked
    def mpo_t1_clicker(self):
        self.factory.mpo_task1()
        return 1

    # Actions from FACTORY class when the SLD task 1 button is clicked
    def sld_t1_clicker(self):
        ready_status = str(self.sld.IsReady())
        if ready_status == "True":
            print("SLD Is Ready: "+ready_status)
            self.sld.StartTask1()#Add values to change
        else:
            print("SLD Is Not Ready: "+ready_status)
        return 1

    # Actions from FACTORY class when the START button is clicked
    def start_clicker(self):
        x_value = int(self.spinBoxX.cleanText())
        y_value = int(self.spinBoxY.cleanText())

        hbw_ready_status = str(self.hbw.IsReady())
        if hbw_ready_status == "True":
            print("HBW Is Ready: "+hbw_ready_status)
            self.hbw.StartTask1(x_value, y_value)
            run_flag = True
        else:
            print("HBW Is Not Ready: "+hbw_ready_status)
        #run factory
        while run_flag:
            if str(self.hbw.IsReady()) == "True":
                self.vgr.StartTask1()#Add values to change 
                time.sleep(20)
                self.mpo.StartTask1()#Add values to change 
                self.sld.StartTask1()#Add values to change
                run_flag = False
        return 1

#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
    #Initialize UI App
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()