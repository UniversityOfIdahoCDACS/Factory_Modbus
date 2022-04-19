

import logging
import time
import json
import sys
import socket       # Used for exception handling
import ssl          # Used for MQTT TLS connection
import paho.mqtt.client as mqtt
import utilities
from job_data import JobData


class Factory_MQTT():
    # Doc: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

    def __init__(self, URL=None, PORT=None, CLIENT_ID="Unknown Client", TOPIC_SUB=None):
        # Logger
        self.logger = logging.getLogger('Factory_MQTT')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Initializing MQTT Client")

        # MQTT variables
        self.mqtt_url = URL
        self.mqtt_port = PORT
        self.client_id = CLIENT_ID  # This client identifier
        self.topic_sub = TOPIC_SUB  # Primary subscriber topic
        print(f"sel topic_sub {self.topic_sub}")

        # MQTT Client config
        self.client = mqtt.Client(self.client_id, transport="websockets")
        self.client.ws_set_options(path="/ws", headers=None)
        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
             tls_version=ssl.PROTOCOL_TLS, ciphers=None)
        self.client.message_callback_add(self.topic_sub, self.on_message)  # Link callback
        #self.client.enable_logger(logger=self.logger)  # paho will use CLASS's logger & settings
        self.client.enable_logger()                     # paho loger will be paho.mqtt.client

        # Callbacks
        self.add_job_callback = None
        self.cancel_job_callback = None
        self.cancel_order_callback = None


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


    # Publish to broker
    def publish(self, topic, payload=None, qos=0, retain=False):
        #self.logger.debug("Sending topic %s this payload: %s", topic, payload)
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

        self.logger.debug("Subscribing to %s", self.topic_sub)
        self.client.subscribe(self.topic_sub)

        # Send online message
        self.publish("Factory/Echo", payload=f"{self.client_id} initialized")


    # Stop and disconnect from broker
    def stop(self):
        self.logger.info("Stopping MQTT loop")
        self.client.loop_stop()
        self.client.disconnect()


    # Health check and any periodic jobs
    def update(self):
        # Check Connection
        if not self.client.is_connected():
            self.logger.warn("MQTT Not connected!")


    ## Callbacks
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info("connected OK Returned code=%s", rc)
        else:
            self.logger.warning("Bad connection Returned code=%s", rc)


    def on_message(self, client, userdata, message):
        """ Activates on message recieved
        Parses payload based on msg_type
        """
        # We don't care about client. Returned client object
        # We don't care about userdata. Empty

        self.logger.info("Message received! \tMsg: %s", message.payload)

        self.logger.debug(">> Message topic: %s", message.topic)
        self.logger.debug(">> Message payload: %s", message.payload)
        self.logger.debug(">> Message timestamp: %s", message.timestamp)

        mypayload = json.loads(message.payload.decode("utf-8"))
        for item in mypayload:
            self.logger.debug(">> Payload item %s\t value: %s", item, mypayload[item])

        echo_msg = f"Factory recieved message type {mypayload['msg_type']}"
        self.publish('Factory/Echo', payload=echo_msg)

        # Parse message
        self.logger.debug("> Parsing message")
        if 'msg_type' in mypayload:
            if mypayload['msg_type'] == 'new_job':
                job_payload = mypayload['payload']
                self.logger.info("Recieved new job")

                if self.add_job_callback is not None:
                    try:
                        # Create job data object. This also validates inputes
                        job_data = JobData(job_id=job_payload['job_id'], order_id=job_payload['order_id'],
                                           color=job_payload['color'], cook_time=job_payload['cook_time'],
                                           sliced=job_payload['slice'])
                    except AttributeError as error:
                        log_msg = f"Error creating job object with data {job_payload}.\n{error}"
                        self.logger.error(log_msg)
                    except Exception as error:
                        self.logger.error("Unknown error %s" % error)
                    else: # No error
                        self.add_job_callback(job_data)


            elif mypayload['msg_type'] == 'cancel_job_id':
                self.cancel_job_callback(mypayload['job_id'])

            elif mypayload['msg_type'] == 'cancel_order_id':
                self.cancel_job_callback(mypayload['order_id'])

            else:
                self.publish("Factory/Job_notice", f"Invalid message type {mypayload['msg_type']}")
                self.logger.error("Message received with invalid message type %s", mypayload['msg_type'])


    def set_add_job_callback(self, func):
        self.add_job_callback = func

    def set_cancel_job_callback(self, func):
        self.cancel_job_callback = func

    def set_cancel_order_callback(self, func):
        self.cancel_order_callback = func


    def on_disconnect(self):
        pass



if __name__ == '__main__':
    # Create logger
    logger = logging.getLogger("factoryMQTT_test")
    logger.setLevel(logging.DEBUG) # sets default logging level for this module

    logger.info("Starting factory MQTT")
    config = utilities.load_env()

    m = Factory_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']), CLIENT_ID=config['MQTT_CLIENT_ID'],
                     TOPIC_SUB=config['MQTT_SUBSCRIBE'])

    m.connect()

    time.sleep(2)
    m.start()

    logger.debug("Going into main loop")
    while True:
        time.sleep(7)
        m.update()

    m.stop()
