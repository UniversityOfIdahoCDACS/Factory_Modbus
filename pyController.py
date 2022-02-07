
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



if __name__ == '__main__':
    logging.info("Starting factory python controller")

    config = load_env()

    logging.info("Starting factory MQTT")
    m = factoryMQTT.FACTORY_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']), CLIENT_ID=config['MQTT_CLIENT_ID'],
            TOPIC_SUB=config['MQTT_SUBSCRIBE'], TOPIC_PUB=config['MQTT_PUBLISH'])

    m.connect()

    time.sleep(2)
    m.start()
    
    
    logging.debug("Going into main loop")
    while True:
        time.sleep(7)
        m.update()