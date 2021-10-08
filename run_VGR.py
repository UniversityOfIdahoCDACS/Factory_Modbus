#!/usr/bin/env python
# -*- coding: utf-8 -*-

# write_bit
# write 4 bits to True, wait 2s, write False, restart...
from pyModbusTCP.client import ModbusClient
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import time
import sys

SERVER_HOST = "129.101.98.246"
SERVER_PORT = 502

c = ModbusClient()

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

toggle = True

# Coils
test_coil = 0
rotate_cw = 131
rotate_ccw = 132
horiz_forward = 133
horiz_backward = 134

# PyQt5 Layout Setup
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def rotate_cw_button_clicked(self):
        coil_connection = c.write_single_coil(test_coil, toggle)
        #self.label.setText("you pressed the button")
        self.update(coil_connection, test_coil)

    def initUI(self):
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("VGR Control Panel")

        #self.label = QtWidgets.QLabel(self)
        #self.label.setText("my first label!")
        #self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton("Toggle", self)
        self.b1.setText("Rotate CW")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.changeColor)
        self.b1.setStyleSheet("background-color : lightgrey")
        self.b1.clicked.connect(self.rotate_cw_button_clicked)

    def update(self, coil_connection, coil_number):
        if coil_connection:
            print("bit #" + str(coil_number) + ": write to " + str(toggle))
        else:
            print("bit #" + str(coil_number) + ": unable to write " + str(toggle))

    # method called by button
    def changeColor(self):
        # if button is checked
        if self.b1.isChecked():
            # setting background color to light-blue
            self.b1.setStyleSheet("background-color : lightblue")
        # if it is unchecked
        else:
            # set background color back to light-grey
            self.b1.setStyleSheet("background-color : lightgrey")


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write coils (modbus function 0x01)
    if c.is_open():
        window()

'''
while True:

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write coils (modbus function 0x01)
    if c.is_open():
        # write 4 bits in modbus address 0 to 3
        print("")
        print("write bits")
        print("----------")
        print("")
        for addr in range(1):
            is_ok = c.write_single_coil(0, toggle)
            if is_ok:
                print("bit #" + str(0) + ": write to " + str(toggle))
            else:
                print("bit #" + str(0) + ": unable to write " + str(toggle))
            time.sleep(0.5)

        time.sleep(1)

        print("")
        print("read bits")
        print("---------")
        print("")
        bits = c.read_coils(0, 5)
        if bits:
            print("bits #0 to 3: "+str(bits))
        else:
            print("unable to read")

    toggle = not toggle

    # sleep 2s before next polling
    time.sleep(1)
    '''