
"""This module tests the runability of webcam.py"""

import logging
import time
import os
import sys

from dotenv import dotenv_values
import webcam


#*********************************************
#* * * * * * * * * Load .env * * * * * * * * *
#*********************************************
def load_env():
    # Find script directory
    envLoc = os.path.dirname(os.path.realpath(__file__)) + "/.env"
    # Test if exist then import .env
    if not os.path.exists(envLoc):
        logging.error(".env file not found")
        logging.debug("envLoc value: %r", envLoc)
        sys.exit(1)
    try:
        loaded_config = dotenv_values(envLoc) # loads .env file in current directoy
    except Exception as e:
        logging.error("Error loading .env file %s", e)
        sys.exit(1)

    # Environment debug
    for item in loaded_config:
        logging.debug("Item: %s\tValue: %s", item, loaded_config[item])

    return loaded_config


logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

def main():
    """Main Function"""

    # Create formatter
    formatter = logging.Formatter('kk[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
    #formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

    # Logger: create console handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)     # set logging level for console
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.getLogger('FACTORY_MQTT').setLevel(logging.ERROR)

    logger.info("test webcam started")

    # MQTT
    if True:
        config = load_env()
        import factoryMQTT

        logger.info("Starting factory MQTT")
        mqtt = factoryMQTT.FACTORY_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']),
                                        CLIENT_ID=config['MQTT_CLIENT_ID'], TOPIC_SUB=config['MQTT_SUBSCRIBE'])
        mqtt.connect()
        time.sleep(1)
        mqtt.start()

        my_webcam = webcam.Webcam(mqtt=mqtt, source=0)
        # my_webcam = webcam.Webcam(mqtt=mqtt) # Source from default test file
    else:
        my_webcam = webcam.Webcam(source=0)

    my_webcam.worker(-1)
    time.sleep(3)

    # my_webcam.start()
    # try:
    #     while True:
    #         time.sleep(10)
    # except KeyboardInterrupt:
    #     my_webcam.stop()
    #     mqtt.stop()
    # my_webcam.worker(5)

    mqtt.stop()

if __name__ == '__main__':
    main()
