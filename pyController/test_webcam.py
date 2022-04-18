
"""This module tests the runability of webcam.py"""

import logging
import time

import utilities
from mqtt import Factory_MQTT
import webcam


logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for this module

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

    logging.getLogger('Factory_MQTT').setLevel(logging.ERROR)

    logger.info("test webcam started")

    # MQTT
    if True:
        # Get environment configs
        config = utilities.load_env()

        logger.info("Starting factory MQTT")
        mqtt = Factory_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']),
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
