
"""This simulates the input and output of the real factory module"""

import logging
import threading

logger = logging.getLogger("Factory_Sim2")
logger.setLevel(logging.DEBUG) # sets default logging level for module

class Factory_Sim2():

    def __init__(self):
        """ Initialize class instance"""
        self.factory_ready = True
        self.factory_fault = False
        self.factory_state = "ready" # [ready, processing, fault, offline]
        self.job_data = None

    def status(self):
        """ Returns the state of the factory """
        status_val = {'status': self.factory_ready,
                    'fault': self.factory_fault,
                    'has_job': self.has_job
                    }
        return self.factory_state
    
    def order(self, x, y, cook_time, slice):
        """ Load processing job order """
        if self.factory_ready:
            logger.info("Factory importing job data")
            self.job_data = {'x':slot_x, 'y': slot_y, 'cook_time': cook_time, 'slice': slice}
            return 0
        else:
            logger.warning("Factory not ready. Not accepting job")
            return 1


    def update(self):
        """
        This function should be called periodically every 1-5 seconds
        This checks the factory state and starts jobs as needed
        """

        if self.factory_state == 'ready':
            if job_data is not None:
                # Start job
                logger.info("Factory starting processing of a job")
                self.factory_ready = False
                # Start thread
                logger.info("Starting processing thread")
                self.processing_thread = threading.Thread(target=self.process)
                self.processing_thread.start()

        elif self.factory_state == 'processing'
            logger.debug("Factory processing an order")
            if not self.processing_thread.is_alive():
                logger.info("Job completed")
                self.factory_ready = True

        elif self.factory_state == 'offline'
            logger.debug("Factory is offline")

        elif self.factory_state == 'fault'
            logger.debug("Factory in fault state")

        else:
            raise Exemption ("Invalid factory_state set")


    def process(self):
        """ Simulate processing """
        logger.info("Processing Started")
        sleep(15)
        logger.info("Processing Finished")
        self.job = None
        return
