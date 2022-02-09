
from distutils.log import error
from dotenv import dotenv_values
import logging
import time
# import json
import sys
import os

# factory modules import
import factoryModbus
import jobQueue
import factoryMQTT


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
    except Exception as e:
        logging.error("Error loading .env file")
        logging.error("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
        sys.exit(1)

    # Environment debug
    for item in config:
        logging.debug("Item: {}\tValue: {}".format(item, config[item]))
    
    return config


class ORCHASTRATOR():
    def __init__(self, mqtt=None, queue=None):
        self.mqtt = mqtt  # mqtt is optional
        if queue is None:
            raise Exception("queue not specified")
        else:
            self.queue=queue

    def add_job_callback(self, job_data):
        # Verify
        if not ('job_id' and 'order_id' and 'color' and 'cook_time' and 'slice' in job_data):
            print("Bad job_data")
            self.send_job_notice("Error: Invalid new_job data: %r" % job_data)
            raise Exception ("Bad job_data")
        
        # Add to queue
        self.queue.add_job(job_data)

        self.send_job_notice("Added job %d for order %d | color: %s,  cook time: %d, sliced: %b"% (job_data['job_id'], job_data['order_id'], job_data['color'], job_data['cook_time'], job_data['slice']))
        pass


    def cancel_job_id_callback(self, job_id):
        self.send_job_notice("Canceled job")
        pass


    def cancel_job_order_callback(self, order_id):
        self.send_job_notice("Canceled order")
        pass


    def send_inventory(self):
        # Get inventory
        pass


    def send_status(self):
        pass


    def send_job_notice(self, msg):
        if self.mqtt is not None:
            pass
        return


    def factory_update(self):
        pass


def main():
    logging.info("Starting factory python controller")

    config = load_env()

    logging.info("Starting factory MQTT")
    mqtt = factoryMQTT.FACTORY_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']), CLIENT_ID=config['MQTT_CLIENT_ID'],
            TOPIC_SUB=config['MQTT_SUBSCRIBE'], TOPIC_PUB=config['MQTT_PUBLISH'])
    mqtt.connect()
    time.sleep(1)
    # mqtt.start()
    
    logging.info("hello")
    logging.debug("Creating Job and orchastrator")
    job_queue = jobQueue.JOB_QUEUE()
    orchastrator = ORCHASTRATOR(mqtt=mqtt, queue=job_queue)


    
    logging.debug("Going into main loop")
    while True:
        time.sleep(7)
        mqtt.update()


if __name__ == '__main__':
    main()