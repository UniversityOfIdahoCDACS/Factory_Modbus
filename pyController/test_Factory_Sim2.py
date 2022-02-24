
""" Test program for Factory_Sim2 """

import logging
from time import sleep
import Factory_Sim2

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG) # sets default logging level for module

def main():
    """ Main test function """
    fs = Factory_Sim2.Factory_Sim2()
    print("Factory ready: {}".format(fs.status))

    while fs.status == False:
        logger.info("Factory processing. Ready: %s", fs.status)
        sleep(1)

    logger.info("Factory job completed. Ready: %s", fs.status)
    print("End test")


if __name__ == '__main__':
    main()
