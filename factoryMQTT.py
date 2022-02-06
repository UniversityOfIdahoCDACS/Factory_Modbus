
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
import time,logging,sys
import json
import os
import socket       # Used for exception handling
import ssl          # Used for MQTT TLS connection

#*********************************************
#* * * * * * * * * Logger Setup * * * * * * * *
#*********************************************
FORMAT = '[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='factoryMQTT.log')

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
    logging.debug("Item: {}\tValue: {}".format(item, config[item]))


class FACTORY_MQTT():
    # Doc: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

    def __init__(self, URL=None, PORT=None, CLIENT_ID="Unknown Client", TOPIC_SUB=None, TOPIC_PUB=None):
        # Logger
        self.logger = logging.getLogger('FACTORY_MQTT')
        self.logger.debug("Initializing MQTT Client")

        # MQTT variables
        self.mqtt_url = URL
        self.mqtt_port = PORT
        self.client_id = CLIENT_ID  # This client identifier
        self.topic_sub = TOPIC_SUB  # Primary subscriber topic
        self.topic_pub = TOPIC_PUB  # Primary publisher topic

        # MQTT Client config
        self.client = mqtt.Client(self.client_id, transport="websockets")
        self.client.ws_set_options(path="/ws", headers=None)
        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
             tls_version=ssl.PROTOCOL_TLS, ciphers=None)
        #self.client.enable_logger(logger=self.logger)   # paho will use CLASS's logger & settings
        self.client.enable_logger()                      # paho loger will be paho.mqtt.client

    def test(self):
        self.logger.info("Hello from class")
    
    def connect(self):
        try:
            self.client.connect(self.mqtt_url, port=self.mqtt_port, keepalive=60)
        except socket.timeout:
            self.logger.error("MQTT connection attempt timed out")
            sys.exit(1)
            #raise Exception ("MQTT connection attempt timed out") from socket.timeout
        except Exception as e:
            self.logger.error("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
            sys.exit(1)
    
    # Called when the broker responds to our connection request
    # client.connect callback
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("connected OK Returned code=",rc)
        else:
            print("Bad connection Returned code=",rc)
        
    
    def message_callback(self, userdata, message):
        self.logger.debug("MQTT userdata: {}\tMsg: {}".format(userdata, message))


    # Publish to broker
    def publish(self, topic, payload=None, qos=0, retain=False):
        self.logger.info("Sending topic {} this payload: {}".format(topic, payload))
        try:
            self.client.publish(topic, payload=payload, qos=qos, retain=retain)
        except ValueError:
            self.logger.error("Invalid topic set, qos invalid, or payload too long")
        except Exception as e:
            self.logger.error("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    

    # connect if needed and start subscription with broker
    def start(self):
        self.logger.debug("Subscribing to {}".format(self.topic_sub))
        self.client.subscribe(self.topic_sub)

        self.logger.info("Starting MQTT loop")
        self.client.loop_start()

        # Send online message
        self.publish(self.topic_pub, payload="%s initialized".format(self.client_id))
    

    # Stop and disconnect from broker
    def stop(self):
        self.logger.info("Stopping MQTT loop")
        self.client.loop_stop()
        self.client.disconnect()
    

    # Health check and any periodic jobs
    def update(self):
        self.logger.debug("MQTT update")
        # check connection?
    
    # TODO
    # Check if connected
    # Reconnect
    # looping

    ## Callbacks
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            self.logger.info("connected OK Returned code=",rc)
        else:
            self.logger.warning("Bad connection Returned code=",rc)

    def on_message(self, userdata, message):
        pass

    def on_disconnect(self):
        pass



if __name__ == '__main__':
    m = FACTORY_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']), CLIENT_ID=config['MQTT_CLIENT_ID'],
            TOPIC_SUB=config['MQTT_SUBSCRIBE'], TOPIC_PUB=config['MQTT_PUBLISH'])

    m.test()
    m.connect()

    time.sleep(2)
    m.start()
    
    while True:
        time.sleep(10)
        m.update()

    m.stop()
    exit()







#******************************************************************************************
#******************************************************************************************
#* Code graveyard
#******************************************************************************************
#******************************************************************************************
os.exit()



#*********************************************
#* * * * * * * * * HANDSHAKE * * * * * * * * *
#*********************************************
def handshake(client, hand_shake):
    client.publish(config['MQTT_PUBLISH'], payload=json.dumps(hand_shake))

#*********************************************
#* * * * * * * * ON MESSAGE * * * * * * * * *
#*********************************************
def on_message(client, userdata, message):
    logging.debug("GOT THE MESSAGE!")
    logging.debug("Received message: '" + str(message.payload) + "' on topic: '"
        + message.topic + "' with QoS: " + str(message.qos))
    data = json.loads(message.payload)
    for item in data:
        logging.debug(">Key: {}\tValue: {}".format(item, data[item]))

   # Factory stuff here

    got_Once = False


got_Once = True
#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
     ### MQTT Set up ###
    logging.info("CREATING CLIENT")
    client = mqtt.Client(config['MQTT_CLIENT_ID'], transport="websockets")
    client.ws_set_options(path="/ws", headers=None)
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
             tls_version=ssl.PROTOCOL_TLS, ciphers=None)

    client.connect(config['MQTT_BROKER_URL'], port=int(config['MQTT_PORT']), keepalive=60)

    client.loop_start()
    client.subscribe(config['MQTT_SUBSCRIBE'])

    #client.on_message = on_message
    #client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=True)
    logging.info("Post client loop")
    while got_Once:
        client.on_message = on_message



