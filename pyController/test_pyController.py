
"""This module tests the runability of pyController.py"""

import logging
import factoryJobQueue
import factory_inventory
import pyController


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

def main():
    """Main Function"""
    logger.info("test pyController started")

    logger.debug("Creating Job and orchastrator")

    # Setup Job Queue and Inventory objects
    job_queue = factoryJobQueue.JobQueue()
    inventory = factory_inventory.FACTORY_INVENTORY()
    inventory.preset_inventory()

    # Setup factory object
    if False: # Use real factory
        #import factoryModbus
        factory = None
    else:
        import FactorySim2
        factory = FactorySim2.FactorySim2()

    # Setup orchastrator object
    orchastrator = pyController.ORCHASTRATOR(mqtt=None, queue=job_queue, inventory=inventory, factory=factory)

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
