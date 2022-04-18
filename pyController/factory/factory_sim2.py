
"""This simulates the input and output of the real factory module
   Used as a drop in replacement for the Factory module when the PLC is unavailable"""

import logging
import threading
import sys
from time import sleep

logger = logging.getLogger("FactorySim2")
logger.setLevel(logging.DEBUG) # sets default logging level for module

class FactorySim2():
    """This class simulates the input and output of the real factory class
       Used as a drop in replacement for Factory class when the PLC is unavailable"""

    def __init__(self, processing_time=40):
        """ Initialize class instance"""
        self.factory_state = "ready" # [ready, processing, fault, offline]
        self.job_data = None

        self.processing_time = processing_time # The total work time proccess will take
        self.processing_thread = None
        self.processing_thread_stop = False

    def status(self):
        """ Returns the state of the factory """
        return self.factory_state

    def order(self, job_data):
        """ Load processing job order """
        if self.factory_state == 'ready':
            logger.info("Factory importing job data")
            self.job_data = job_data
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
                self.factory_state = 'processing'
                # Start thread
                logger.info("Starting processing thread")
                self.processing_thread = threading.Thread(target=self.process)
                self.processing_thread.start()

        elif self.factory_state == 'processing':
            logger.debug("Factory processing an order")
            if not self.processing_thread.is_alive():
                logger.info("Job completed")
                self.factory_state = 'ready'

        elif self.factory_state == 'offline':
            logger.debug("Factory is offline")

        elif self.factory_state == 'fault':
            logger.debug("Factory in fault state")

        else:
            raise Exception("Invalid factory_state set")

        return self.factory_state

    def stop(self):
        """ Set stop flag for simulation thread"""
        self.processing_thread_stop = True
        if self.processing_thread is not None:
            self.processing_thread.join()


    def process(self):
        """ Simulate processing """
        wait_time = self.processing_time / 4

        def wait(self, sleep_time):
            """ Wait function that monitors a thread stop condition """
            main_thread = threading.main_thread()

            for _ in range(int(sleep_time)):
                if not main_thread.is_alive() or self.processing_thread_stop:
                    logger.info("FactorySim thread exiting")
                    sys.exit(0)
                else:
                    sleep(1)

        logger.info("Processing Started. Processing time %d seconds", self.processing_time)
        # sleep(3)
        wait(self, wait_time)
        logger.info("Processing ...")
        # sleep(3)
        wait(self, wait_time)
        logger.info("Processing ...")
        # sleep(3)
        wait(self, wait_time)
        logger.info("Processing ...")
        # sleep(3)
        wait(self, wait_time)
        logger.info("Processing Finished")
        self.job_data = None
        return
