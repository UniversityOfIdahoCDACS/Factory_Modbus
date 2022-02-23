
"""This module tests the runability of pyController.py"""

import logging
import factoryJobQueue
import pyController


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

def main():
    """Main Function"""
    logger.info("test pyController started")

    logger.info("hello")
    logger.debug("Creating Job and orchastrator")
    job_queue = factoryJobQueue.JobQueue()
    orchastrator = pyController.ORCHASTRATOR(mqtt=None, queue=job_queue)

    if True:
        logger.info("Running Tests")
        add_job = {'job_id': 123, 'order_id': 100, 'color': "red", 'cook_time': 3, 'slice': True}
        orchastrator.add_job_callback(add_job)
        add_job = {'job_id': 124, 'order_id': 100, 'color': "red", 'cook_time': 3, 'slice': True}
        orchastrator.add_job_callback(add_job)
        add_job = {'job_id': 225, 'order_id': 201, 'color': "red", 'cook_time': 3, 'slice': True}
        orchastrator.add_job_callback(add_job)
        add_job = {'job_id': 226, 'order_id': 201, 'color': "red", 'cook_time': 3, 'slice': True}
        orchastrator.add_job_callback(add_job)
        add_job = {'job_id': 227, 'order_id': 201, 'color': "red", 'cook_time': 3, 'slice': True}
        orchastrator.add_job_callback(add_job)

        orchastrator.cancel_job_id_callback(124)
        orchastrator.cancel_job_id_callback(1256)
        orchastrator.cancel_job_order_callback(201)
        orchastrator.cancel_job_order_callback(201201)



if __name__ == '__main__':
    main()
