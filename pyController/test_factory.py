
"""This module tests the runability of factory.py"""

import logging
from time import sleep

import utilities
from factory.factory import FACTORY

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
    f = FACTORY(config['FACTORY_IP'], config['FACTORY_PORT'])
    logger.info("Initialized")
    print("P Initialized")

    f_status = f.status()
    logger.info("Factorystatus %s", f_status)


    if f_status == 'idle':
        # order
        f.order(3, 1, 2, True)
        f.update()
        sleep(2)
    else:
        print("Factory not idle")
    
    while f.status() != 'idle':
        logger.info("Factory Status: %s", f.status())
        f.update()
        sleep(1)


if __name__ == "__main__":
    main()
