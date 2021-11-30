from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from datetime import datetime
import factoryModbus as fm
import time,logging,sys
import json
import os

mqttBroker = "mqtt.eclipseprojects.io"
port = 8883

#*********************************************
#* * * * * * * * * HANDSHAKE * * * * * * * * *
#*********************************************
def handshake(client, hand_shake):
    client.publish("UofICapstone_Sim", payload=json.dumps(hand_shake))
    print("....SENT HANDSHAKE...")

#*********************************************
#* * * * * * * * ON MESSAGE * * * * * * * * *
#*********************************************
def on_message(client, userdata, message):
    print("GOT THE MESSAGE!")
    factory = fm.FACTORY('129.101.98.246', 502)
    x_value = 2
    y_value = 3
    factory.order(x_value, y_value)
    got_Once = False
'''    
class MQTT(QMainWindow):
    def __init__(self):
        super(MQTT, self).__inti__()
        self.factory = fm.FACTORY('129.101.98.246', 502)
'''
got_Once = True
#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
     ### MQTT Set up ###
    print("CREATING CLIENT")
    client = mqtt.Client("Factory Sim")
    client.connect(mqttBroker)
    client.loop_start()
    client.subscribe("UofICapstone_Cloud")
    while got_Once:
        client.on_message = on_message

