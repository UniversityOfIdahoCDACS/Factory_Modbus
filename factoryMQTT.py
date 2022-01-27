#from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import factoryModbus as fm
import time,logging,sys
import json
import os
import socket    # Used for exception handling
from dotenv import load_dotenv


#*********************************************
#* * * * * * * * * Load .env * * * * * * * * *
#*********************************************
# Find script directory
envLoc = os.path.dirname(os.path.realpath(__file__)) + "/.env"
# Test if exist then import .env
if not os.path.exists(envLoc):
    logging.error(".env file not found")
    logging.debug("envLoc value: %r" % envLoc)
    sys.exit(1)
try:
    config = dotenv_values(envLoc) # loads .env file in current directoy
except:
    logging.error("Error loading .env file")
    sys.exit(1)

# Environment debug
for item in config:
    logging.debug(item, config[item], type(config[item]))


#*********************************************
#* * * * * * * * * HANDSHAKE * * * * * * * * *
#*********************************************
def handshake(client, hand_shake):
    client.publish(config['MQTT_PUBLISH'], payload=json.dumps(hand_shake))
    print("....SENT HANDSHAKE...")

#*********************************************
#* * * * * * * * ON MESSAGE * * * * * * * * *
#*********************************************
def on_message(client, userdata, message):
    print("GOT THE MESSAGE!")
    factory = fm.FACTORY(config['FACTORY_IP'], config['FACTORY_PORT'])
    x_value = 2
    y_value = 3
    factory.order(x_value, y_value)
    got_Once = False


got_Once = True
#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
     ### MQTT Set up ###
    print("CREATING CLIENT")
    client = mqtt.Client(config['MQTT_CLIENT_ID'])

    try:
        client.connect(config['MQTT_BROKER_URL'], keepalive=60)
    except socket.timeout:
        print("MQTT connection attempt timed out")
        sys.exit(1)
        #raise Exception ("MQTT connection attempt timed out") from socket.timeout
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
        sys.exit(1)

    client.loop_start()
    client.subscribe(config['MQTT_SUBSCRIBE'])
    while got_Once:
        client.on_message = on_message
