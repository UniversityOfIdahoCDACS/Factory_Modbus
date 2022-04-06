
import os
import sys
import logging
from time import sleep
from dotenv import dotenv_values
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

def main():
    config = load_env()
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
