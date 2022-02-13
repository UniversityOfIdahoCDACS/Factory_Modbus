
import enum
from dotenv import dotenv_values
import logging
from logging.handlers import RotatingFileHandler
import time
import json
import sys
import os

# factory modules import
#import factoryModbus
import jobQueue
import factory_inventory
import factoryMQTT


#*********************************************
#* * * * * * * * * Logger Setup * * * * * * * *
#*********************************************

# Logger: logging config   https://docs.python.org/3/howto/logging-cookbook.html
# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for all modules
#logger.
 
# Create formatter
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

# Logger: create rotating file handler
rfh = RotatingFileHandler('app_rot.log')
rfh.maxBytes=1024*1024          # maximum size of a log before being rotated
rfh.backupCount=2               # how many rotated files to keep
rfh.setFormatter(formatter)     # set format
rfh.setLevel(logging.DEBUG)     # set level for file logging
logger.addHandler(rfh)          # add filehandle to logger
 
# Logger: create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)     # set logging level for console
ch.setFormatter(formatter)
logger.addHandler(ch)
 
# reduce logging level of specificlibraries
logging.getLogger("jobQueue").setLevel(logging.DEBUG)
logging.getLogger("paho.mqtt.client").setLevel(logging.DEBUG)


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
    def __init__(self, mqtt=None, queue=None, inventory=None):
        self.mqtt = mqtt  # mqtt is optional
        self.inventory = inventory
        if queue is None:
            raise Exception("queue not specified")
        else:
            self.queue=queue
        

    def add_job_callback(self, job_data):
        # Verify
        if not ('job_id' and 'order_id' and 'color' and 'cook_time' and 'slice' in job_data):
            logging.error("Error: Invalid new_job data. dir: {}".format(dir(job_data)))
            self.send_job_notice("Error: Invalid new_job data: {}".format(job_data))
            raise Exception ("Bad job_data")
        
        # Add to queue
        self.queue.add_job(job_data)
        log_msg = "Added job {} for order {} | color: {},  cook time: {}, sliced: {}".format(job_data['job_id'], job_data['order_id'], job_data['color'], job_data['cook_time'], job_data['slice'])
        self.send_job_notice(log_msg)


    def cancel_job_id_callback(self, job_id):
        # Verify
        if not (isinstance(job_id, int) and job_id >= 0):
            log_msg = "Error: Invalid cancel job id: {}".format(job_id)
            logging.error(log_msg)
            self.send_job_notice(log_msg)
            raise Exception (log_msg)
        
        # Cancel Job
        cancel_msg = self.queue.cancel_job_id(job_id)

        # Report
        logging.debug(cancel_msg[1])
        self.send_job_notice(cancel_msg[1])


    def cancel_job_order_callback(self, order_id):
        # Verify
        if not (isinstance(order_id, int) and order_id >= 0):
            log_msg = "Error: Invalid cancel order id: {}".format(order_id)
            logging.error(log_msg)
            self.send_job_notice(log_msg)
            raise Exception (log_msg)
        
        # Cancel order
        cancel_msg = self.queue.cancel_job_order(order_id)
        
        # Report
        if cancel_msg[0] == 0:
            for item in cancel_msg[1]:
                logging.debug(item)
                self.send_job_notice(item)
        else:
            self.send_job_notice(cancel_msg[1])
    

    def send_inventory(self):
        # Get inventory
        if self.mqtt is not None:
            inv = {}
            inv['Inventory'] = self.inventory.get_inventory()
            logging.debug("Got inventory: {}".format(inv))

            self.mqtt.publish('Factory/Inventory', payload=json.dumps(inv), qos=0)
        return


    def send_status(self):
        if self.mqtt is not None:
            status = {}
            status['factory_status'] = 'Offline'
            status['current_job'] = 'None'
            status['job_queue_len'] = str(self.queue.has_jobs())
            self.mqtt.publish("Factory/Status", payload=json.dumps(status), qos=0)


    def send_job_notice(self, msg):
        if self.mqtt is not None:
            self.mqtt.publish("Factory/Job_notice", payload=msg, qos=2)
        return


    def factory_update(self):
        pass


def main():
    logging.info("Starting factory python controller")

    config = load_env()

    logging.info("Starting factory MQTT")
    mqtt = factoryMQTT.FACTORY_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']), CLIENT_ID=config['MQTT_CLIENT_ID'],
            TOPIC_SUB=config['MQTT_SUBSCRIBE'])
    mqtt.connect()
    time.sleep(1)
    mqtt.start()
    
    logging.info("hello")
    logging.debug("Creating Job and orchastrator")
    job_queue = jobQueue.JOB_QUEUE()
    inventory = factory_inventory.FACTORY_INVENTORY()
    inventory.preset_inventory()
    orchastrator = ORCHASTRATOR(mqtt=mqtt, queue=job_queue, inventory=inventory)

    
    logging.debug("Going into main loop")
    while True:
        time.sleep(7)
        mqtt.update()
        orchastrator.send_inventory()
        orchastrator.send_status()


if __name__ == '__main__':
    main()