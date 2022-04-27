""" Test file for webadmin.py """

from time import sleep
import logging
import webapp.webadmin as webadmin

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for this module

# Create formatter
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

# Logger: create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)     # set logging level for console
ch.setFormatter(formatter)
logger.addHandler(ch)

def main():
    """ Main program """
    print("Starting Webapp")

    webadmin.start_webapp()
    print("Webapp continuted")

    while True:
        # print("tick")
        try:
            sleep(5)
        except KeyboardInterrupt:
            print("main exiting from keyboard interrupt")
            exit()


if __name__ == "__main__":
    main()
