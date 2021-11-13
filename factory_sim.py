#!/usr/bin/python

"""factory_sim.py: Runs a simulation of the factory 4.0. """
__author__      = "Doug Barnes"
__version__     = "1.0.0"
__maintainer__  = "Doug Barnes"
__email__       = "barn1855@vandals.uidaho.edu"
__status__      = "Production"

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from datetime import datetime
import time,logging,sys
import json
import os

mqttBroker = "mqtt.eclipseprojects.io"
port = 8883

#LOOK UP JSON LIB
#import psycopg2
#from psycopg2 import Error

# Flags
message_received_flag = False
perform_inventory_flag = False
order_canceled = False
cancel_flag = False
factory_running = False
hbw_flag = False
vgr_flag = False
mpo_flag = False
ssc_flag = False
sld_flag = False

# Variables
fc_number = 1000
os_number = 1000

# Dictionaries
hand_shake={
    "msg_type": "message confirmation",
    "msg_confirmation_id": "FC1000",
    "msg_type_received": "order"
}
#hand_shake["msg_confirmation_id"] = "CC1000"

order_status={
    "msg_type": "factory status",
    "cloud_id": "SO1000",
    "disk_color_id": "RED01", 
    "order_complete": "True"
}

status={
    "msg_type": "request status",
    "cloud_id": "SO1000",
    "running": "False", 
    "HBW": "False",
    "VGR": "False", 
    "MPO": "False",
    "SSC": "False", 
    "SLD": "False"
}

inventory={
    "msg_type": "inventory",
    "cloud_id": "PI1000",

    "location01": "RED01", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location02": "RED02", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location03": "RED03", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location04": "BLUE01", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location05": "BLUE02", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location06": "BLUE03", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location07": "White01", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location08": "White02", 
    "disk_stored": "True", 
    "pallet_stored": "True",

    "location09": "White03", 
    "disk_stored": "True", 
    "pallet_stored": "True",
}

cancel_status={
    "msg_type": "cancel status",
    "cloud_id": "CO####",
    "canceled": "False"
}

webcam_status={
    "msg_type": "webcam status",
    "cloud_id": "WP1000", #or CW1000
    "power": "False",
    "y_turntable": "0",
    "x_turntable": "0"
}

unable_status={
    "msg_type": "unable status",
    "cloud_id": "PI####"
}

#*********************************************
#* * * * * * * FACTORY MASTER * * * * * * * * 
#*********************************************
def factory_master():
    global message_received_flag, order_canceled, factory_running, cancel_flag, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag

    ### MQTT Set up ###
    print("CREATING CLIENT")
    client = mqtt.Client("Factory Sim")
    client.connect(mqttBroker)
    client.loop_start()
    client.subscribe("UofICapstone_Cloud")
    client.on_message = on_message

    #print("Factory Check ....")
    while True:
        time.sleep(0.5)
        #***************************
        #* * * * RUN FACTORY * * * *
        #***************************
        if message_received_flag == True:
            handshake(client, hand_shake)
            factory_running = True
            print("Factory Started ....")

            update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag)
            print(status)
            time.sleep(1)

            #* * * * HBW * * * *
            if order_canceled == True:
                print("ORDER HAS BEEN CANCELED")
            else:
                print("HBW Start ....")
                hbw_flag = True
                update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag)
                time.sleep(5)
                hbw_flag = False
                print("HBW End ....")

            #* * * * VGR * * * *
            if order_canceled == True:
                print("ORDER HAS BEEN CANCELED")
            else:
                print("VGR Start ....")
                vgr_flag = True
                update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag)
                time.sleep(5)
                vgr_flag = False
                print("VGR End ....")
            
            #* * * * MPO * * * *
            if order_canceled == True:
                print("ORDER HAS BEEN CANCELED")
            else:
                print("MPO Start ....")
                mpo_flag = True
                cancel_flag = True
                update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag)
                time.sleep(4)
                mpo_flag = False
                print("MPO End ....")

            #* * * * SLD * * * *
            if order_canceled == True:
                print("ORDER HAS BEEN CANCELED")
            else:
                print("SLD Start ....")
                sld_flag = True
                update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag)
                time.sleep(4)
                sld_flag = False
                print("SLD End ....")
                client.publish("UofICapstone_Sim", payload=json.dumps(order_status))

            message_received_flag = False
            factory_running = False
            order_canceled = False
            update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag)
            print("Factory Ended ....")
            cancel_flag = False

        elif perform_inventory_flag == True:
            print("Performing inventory")
            #perform inventory
         
#*********************************************
#* * * * * * * UPDATE STATUS * * * * * * * * *
#*********************************************
def update_status(factory_running, hbw_flag, vgr_flag, mpo_flag, ssc_flag, sld_flag):
    #status["cloud_id"] = cloud_id
    status["running"] = factory_running
    status["HBW"] = hbw_flag
    status["VGR"] = vgr_flag
    status["MPO"] = mpo_flag
    status["SSC"] = ssc_flag
    status["SLD"] = sld_flag

#*********************************************
#* * * * * * * * ON MESSAGE * * * * * * * * *
#*********************************************
def on_message(client, userdata, message):
    global message_received_flag, order_canceled, cancel_flag

    #recieved_message = str(message.payload.decode("utf-8"))
    print("***************************************")
    recieved_message = json.loads(message.payload.decode("utf-8"))
    msg_type_received = recieved_message["msg_type"]
    cloud_id_received = recieved_message["cloud_id"]
    print(recieved_message)
    print(msg_type_received)
    print(cloud_id_received)
    #print("***************************************")

    # Order sent from cloud
    if msg_type_received == "order":
        print(recieved_message["location"])
        print("***************************************")
        if message_received_flag == True:
            print("!*!*!*!*! ORDER UNABLE !*!*!*!*!*!")
            unable_status["cloud_id"] = cloud_id_received
            print(unable_status["cloud_id"])
            client.publish("UofICapstone_Sim", payload=json.dumps(unable_status))

        else:
            status["cloud_id"] = cloud_id_received
            print("Received message: ", recieved_message)
            message_received_flag = True

    # Request Status from cloud
    elif msg_type_received == "request status":
        print("***************************************")
        # Give the Cloud the status and keep running the system
        print("Request Status")
        client.publish("UofICapstone_Sim", payload=json.dumps(status))
        print(status)

    # Perform Inventory from cloud
    elif msg_type_received == "perform inventory":
        print("***************************************")
        # Unable to perform inventory while factory is running
        if message_received_flag == True:
            print("!*!*!*!*! INVENTORY UNABLE !*!*!*!*!*!")
            #unable_status["cloud_id"] = recieved_message[49:56]
            print(unable_status["cloud_id"])
            client.publish("UofICapstone_Sim", payload=json.dumps(unable_status))
        # Start Perform Inventory
        else:
            print("Perform Inventory")
            client.publish("UofICapstone_Sim", payload=json.dumps(inventory))
    
    # Cancel Order from cloud
    elif msg_type_received == "cancel order":
        print("***************************************")
        # if factory is before MPO then you can cancel, stop the thread
        #status["MPO"] == True or status["SLD"] == True or 
        if cancel_flag == True:
            print("!*!*!*!*! CANCEL UNABLE !*!*!*!*!*!")
            #unable_status["cloud_id"] = recieved_message[49:56]
            print(unable_status["cloud_id"])
            client.publish("UofICapstone_Sim", payload=json.dumps(unable_status))
        elif message_received_flag == False:
            print("Nothing to cancel")
            client.publish("UofICapstone_Sim", payload=json.dumps(unable_status))
        else:
            print("Cancel Order")
            order_canceled = True
            #####
            ###
            ##
            #
    # WC is Webcam from cloud
    elif msg_type_received == "webcam":
        print(recieved_message["power"])
        print("***************************************")
        # power on/off webcam and keep factory running.
        print("Webcam")
    # CW is Control Webcam from cloud
    elif msg_type_received == "control webcam":
        print(recieved_message["y_turntable"])
        print(recieved_message["x_turntable"])
        print("***************************************")
        # move camera and keep factory running.
        print("Control Webcam")

#*********************************************
#* * * * * * * * * HANDSHAKE * * * * * * * * *
#*********************************************
def handshake(client, hand_shake):
    client.publish("UofICapstone_Sim", payload=json.dumps(hand_shake))
    print("....SENT HANDSHAKE...")

#********************************************
#* * * * * * * * * MAIN * * * * * * * * * * *
#********************************************
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    time_now = datetime.now() + timedelta(seconds=2)
    scheduler.add_job(factory_master, 'date', run_date=time_now, id='factory_job')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

'''
### MQTT Set up ###
print("CREATING CLIENT")
client = mqtt.Client("Factory Sim")
client.connect(mqttBroker)
hand_shake["msg_confirmation_id"] = "FC" + str(fc_number)
client.loop_start()
client.subscribe("UofICapstone_User")
client.on_message = on_message
'''
'''try:
    #### Connect to an existing database ####
    connection = psycopg2.connect(user="postgres",
                                  password="qwerty",
                                  host="localhost",
                                  database="factorydb")

    #### Create a cursor to perform database operations ####
    cursor = connection.cursor()

### MQTT Set up ###
print("CREATING CLIENT")
client = mqtt.Client("Factory Sim")
client.connect(mqttBroker)
hand_shake["msg_confirmation_id"] = "FC" + str(fc_number)

while True:
    client.loop_start()
    client.subscribe("UofICapstone_User")
    client.on_message = on_message

    if message_received_flag == True:
        message_received_flag = False
        handshake(hand_shake)
'''
        #scheduler.resume(factory_start)
        #time.sleep(3)
        #client.publish("UofICapstone_Sim", payload=json.dumps(order_status))
        #print("....SENT ORDERSTATUS...")

    #print("-----Loop-----")
    #time.sleep(5)
    #client.loop_end()


    #while not client.message_received_flag:
        #time.sleep(1) #wait for message
    #client.message_received_flag=False
    #if len(messages)==0:
        #print("test failed")
    #else:
        #print("not failed")

#client.disconnect()


'''except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
 '''   
