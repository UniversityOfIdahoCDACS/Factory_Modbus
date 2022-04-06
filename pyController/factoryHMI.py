
import logging
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QSpinBox
import utilities
from PyQt5 import uic
import FactoryUI


#*****************************
#*            UI             *
#*****************************
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        config = utilities.load_env()
        #self.factory = fm.FACTORY(config['FACTORY_IP'], config['FACTORY_PORT'])
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
        self.button_hbw_status = self.findChild(QPushButton, "pushButton_7")
        self.button_vgr_status = self.findChild(QPushButton, "pushButton_8")
        self.button_mpo_status = self.findChild(QPushButton, "pushButton_9")
        self.button_sld_status = self.findChild(QPushButton, "pushButton_10")

        #Actions
        self.t1button_hbw.clicked.connect(self.hbw_t1_clicker)
        self.t2button_hbw.clicked.connect(self.hbw_t2_clicker)
        self.t1button_vgr.clicked.connect(self.vgr_t1_clicker)
        self.t1button_mpo.clicked.connect(self.mpo_t1_clicker)
        self.t1button_sld.clicked.connect(self.sld_t1_clicker)
        self.button_start.clicked.connect(self.start_clicker)
        self.button_hbw_status.clicked.connect(self.hbw_status_clicker)
        self.button_vgr_status.clicked.connect(self.vgr_status_clicker)
        self.button_mpo_status.clicked.connect(self.mpo_status_clicker)
        self.button_sld_status.clicked.connect(self.sld_status_clicker)
        
        #Show App
        self.show()

    # Actions when the HBW task 1 button is clicked
    def hbw_t1_clicker(self):  
        #print(self.spinBoxX.cleanText())
        #print(self.spinBoxY.cleanText())
        x_value = int(self.spinBoxX.cleanText())
        y_value = int(self.spinBoxY.cleanText())
        #self.factory.hbw_task1(x_value, y_value)
        return 1

    # Actions when the HBW task 2 button is clicked
    def hbw_t2_clicker(self):
        #print(self.spinBoxX.cleanText())
        #print(self.spinBoxY.cleanText())
        x_value = int(self.spinBoxX.cleanText())
        y_value = int(self.spinBoxY.cleanText())
        #self.factory.hbw_task2(x_value, y_value)
        return 1

    # Actions from FACTORY class when the vgr task 1 button is clicked
    def vgr_t1_clicker(self):    
        #self.factory.vgr_task1()
        return 1

    # Actions from FACTORY class when the MPO task 1 button is clicked
    def mpo_t1_clicker(self):
        #self.factory.mpo_task1()
        return 1

    # Actions from FACTORY class when the SLD task 1 button is clicked
    def sld_t1_clicker(self):
        #self.factory.sld_task1()
        return 1

    # Actions from FACTORY class when the START button is clicked
    def start_clicker(self):
        x_value = int(self.spinBoxX.cleanText())
        y_value = int(self.spinBoxY.cleanText())
        #self.factory.order(x_value, y_value)
        return 1

    # Actions from FACTORY class when the SLD task 1 button is clicked
    def hbw_status_clicker(self):
        #self.factory.hbw_status()
        return 1

    # Actions from FACTORY class when the SLD task 1 button is clicked
    def vgr_status_clicker(self):
        #self.factory.vgr_status()
        return 1

    # Actions from FACTORY class when the SLD task 1 button is clicked
    def mpo_status_clicker(self):
        #self.factory.mpo_status()
        return 1

    # Actions from FACTORY class when the SLD task 1 button is clicked
    def sld_status_clicker(self):
        #self.factory.sld_status()
        return 1

#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
    #Initialize UI App
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
