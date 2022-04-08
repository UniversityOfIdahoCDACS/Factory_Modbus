
"""This module tests the runability of factory.py"""

import logging
from time import sleep

import utilities
from factory.factory import SSC_Webcam
from factory.factory import MODBUS

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

# Create formatter
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

# Logger: create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)     # set logging level for console
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    config = utilities.load_env()

    modbus = MODBUS(config['FACTORY_IP'], config['FACTORY_PORT'])
    w = SSC_Webcam(modbus)

    logger.info("Initialized")
    print("P Initialized")

    
    w.StartTask1()
    sleep(5)

    print("End")


if __name__ == "__main__":
    main()
