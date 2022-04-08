""" Utility functions """

import logging
import sys
import os
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
