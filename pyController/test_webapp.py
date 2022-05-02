""" Test file for webadmin.py """

from time import sleep
import logging
from factory.factory_sim2 import FactorySim2    # Simulated factory
from orchastrator import Orchastrator
import webapp.webadmin as webadmin

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for this module

# Create formatter
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

def main():
    """ Main program """

    # Setup factory sim object
    factory = FactorySim2()

    # Setup orchastrator object
    orchastrator = Orchastrator(mqtt=None, factory=factory)

    logger.info("Starting Webapp")
    webadmin.webapp_storage.set_orchastrator(orchastrator)
    webadmin.start_webapp()
    logger.info("Webapp continuted")

    while True:
        # print("tick")
        try:
            sleep(5)
        except KeyboardInterrupt:
            logger.info("main exiting from keyboard interrupt")
            exit()


if __name__ == "__main__":
    main()
