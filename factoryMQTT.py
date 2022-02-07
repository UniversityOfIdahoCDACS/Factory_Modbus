
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
import logging
import time
import json
import sys
import os
import socket       # Used for exception handling
import ssl          # Used for MQTT TLS connection

#*********************************************
#* * * * * * * * * Logger Setup * * * * * * * *
#*********************************************
FORMAT = '[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG) #, filename='factoryMQTT.log')

#*********************************************
#* * * * * * * * * Load .env * * * * * * * * *
#*********************************************
def load_env():
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

    return config

class FACTORY_MQTT(mqtt.Client):
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
        self.client.message_callback_add(self.topic_sub, self.on_message)  # Link callback
        #self.client.enable_logger(logger=self.logger)  # paho will use CLASS's logger & settings
        self.client.enable_logger()                     # paho loger will be paho.mqtt.client


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
        self.logger.info("Starting MQTT loop")
        self.client.loop_start()

        self.logger.debug("Subscribing to {}".format(self.topic_sub))
        self.client.subscribe(self.topic_sub)

        # Send online message
        self.publish(self.topic_pub, payload="%s initialized".format(self.client_id))
    

    # Stop and disconnect from broker
    def stop(self):
        self.logger.info("Stopping MQTT loop")
        self.client.loop_stop()
        self.client.disconnect()
    s

    # Health check and any periodic jobs
    def update(self):
        self.logger.debug("MQTT update")
        self.logger.debug(">MQTT State: {}".format(self.client._state))
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


    def on_message(self, client, userdata, message):
        # We don't care about client. Returned client object
        # We don't care about userdata. Empty

        self.logger.info("Message received! \tMsg: {}".format(message.payload))
        
        self.logger.debug(">> Client id: {}".format(client._client_id))
        self.logger.debug(">> Message topic: {}".format(message.topic))
        self.logger.debug(">> Message payload: {}".format(message.payload))
        self.logger.debug(">> Message info: {}".format(message.info))
        self.logger.debug(">> Message timestamp: {}".format(message.timestamp))

        self.logger.debug("> Parsing message")
        mypayload = json.loads(message.payload.decode("utf-8"))
        for item in mypayload:
            self.logger.debug(">> Payload item {}\t value: {}".format(item, mypayload[item]))

        self.logger.debug("Echoing message back to server")
        echo_msg = "Factory recieved message type {}".format(mypayload['msg_type'])
        self.publish(self.topic_pub, payload=echo_msg)



    def on_disconnect(self):
        pass



if __name__ == '__main__':
    logging.info("Starting factory MQTT")
    config = load_env()

    m = FACTORY_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']), CLIENT_ID=config['MQTT_CLIENT_ID'],
            TOPIC_SUB=config['MQTT_SUBSCRIBE'], TOPIC_PUB=config['MQTT_PUBLISH'])

    m.connect()

    time.sleep(2)
    m.start()
    
    
    logging.debug("Going into main loop")
    while True:
        time.sleep(7)
        m.update()

    m.stop()
    exit()
