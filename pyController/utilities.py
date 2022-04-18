""" Utility functions """

# Standard Lib
import logging
import sys
import os
import signal

# Libraries
from dotenv import dotenv_values

#*********************************************
#* * * * * * * * * Load .env * * * * * * * * *
#*********************************************
def load_env():
    """ Loads environment variables from a .env file """
    # Find script directory
    file_loc = os.path.dirname(os.path.realpath(__file__)) + "/.env"
    # Test if .env exists
    if not os.path.exists(file_loc):
        logging.error(".env file not found")
        logging.debug("file_loc value: %r", file_loc)
        sys.exit(1)

    # Load .env
    try:
        loaded_config = dotenv_values(file_loc) # loads .env file in current directoy
    except Exception as exception:
        logging.error("Error loading .env file %s", exception)
        sys.exit(1)

    # Environment debug
    for item in loaded_config:
        logging.debug("Env Var: %s\tValue: %s", item, loaded_config[item])


    return loaded_config


class GracefulKiller:
    # Source: https://stackoverflow.com/a/31464349
    # Signal doc: https://docs.python.org/3/library/signal.html
    """
    Class to term program upon term signal
    poll kill_now for True and exit
    example: while not killer.kill_now:

    Tip: In threads use:
        main_thread = threading.main_thread()
        while main_thread.is_alive():
    """
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        """ Sets kill flag """
        self.kill_now = True
        if args[0] == signal.SIGINT:
            logging.warning("Keyboard interrupt")
            #print("p Keyboard interrupt")
        else:
            logging.warning("Term signal received")
            #print("p Term signal received")

def create_log_dir(path):
    """
    Tests for logging directory. Creates directory if missing
    path: log directory path
    Example: create_log_dir("/var/log/project")
    Example: create_log_dir("./logs")
    """

    # Test if path exists
    if not os.path.exists(path):
        logging.info("Logging directory not found. Creating at %s", path)
        os.mkdir(path)
