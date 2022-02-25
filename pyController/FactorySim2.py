
"""This simulates the input and output of the real factory module
   Used as a drop in replacement for factoryModbus when the PLC is unavailable"""

import logging
import threading
from time import sleep

logger = logging.getLogger("FactorySim2")
logger.setLevel(logging.DEBUG) # sets default logging level for module

class FactorySim2():

    def __init__(self):
        """ Initialize class instance"""
        self.factory_ready = True
        self.factory_fault = False
        self.factory_state = "ready" # [ready, processing, fault, offline]
        self.job_data = None

        self.processing_thread = None

    def status(self):
        """ Returns the state of the factory """
        status_val = {'status': self.factory_ready,
                    'fault': self.factory_fault
                    }
        return self.factory_state

    def order(self, slot_x, slot_y, cook_time, do_slice):
        """ Load processing job order """
        if self.factory_ready:
            logger.info("Factory importing job data")
            self.job_data = {'x': slot_x, 'y': slot_y, 'cook_time': cook_time, 'do_slice': do_slice}
            return 0
        else:
            logger.error("Factory not ready. Not accepting job")
            return 1


    def update(self):
        """
        This function should be called periodically every 1-5 seconds
        This checks the factory state and starts jobs as needed
        """
        if self.factory_state == 'ready':
            if self.job_data is not None:
                # Start job
                logger.info("Factory starting processing of a job")
                self.factory_ready = False
                self.factory_state = 'processing'
                # Start thread
                logger.info("Starting processing thread")
                self.processing_thread = threading.Thread(target=self.process)
                self.processing_thread.start()

        elif self.factory_state == 'processing':
            logger.debug("Factory processing an order")
            if not self.processing_thread.is_alive():
                logger.info("Job completed")
                self.factory_ready = True
                self.factory_state = 'ready'

        elif self.factory_state == 'offline':
            logger.debug("Factory is offline")

        elif self.factory_state == 'fault':
            logger.debug("Factory in fault state")

        else:
            raise Exception("Invalid factory_state set")
        
        return self.factory_state


    def process(self):
        """ Simulate processing """
        logger.info("Processing Started")
        sleep(3)
        logger.info("Processing ...")
        sleep(3)
        logger.info("Processing ...")
        sleep(3)
        logger.info("Processing ...")
        sleep(3)
        logger.info("Processing Finished")
        self.job_data = None
        return
