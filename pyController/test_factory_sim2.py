
""" Test program for Factory_Sim2 """

import logging
from time import sleep
from factory.factory_sim2 import FactorySim2

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for module

def main():
    """ Main test function """
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
    #formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

    # Logger: create console handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)     # set logging level for console
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.getLogger('Factory_Sim2').setLevel(logging.DEBUG)

    fs = FactorySim2()
    logger.info("Factory Status: %s", fs.status())

    fs.order(1, 2, 3, 4)
    fs.update()
    sleep(0.01)

    while fs.status() != 'ready':
        logger.info("Factory Status: %s", fs.status())
        fs.update()
        try:
            sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping")
            fs.stop()

    logger.info("Factory job completed. Status: %s", fs.status())
    logger.info("End test")


if __name__ == '__main__':
    main()
