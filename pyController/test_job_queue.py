
"""This module tests the runability of jobQueue.py"""

import logging
from job_queue import JobQueue
from job_data import JobData
from inventory import Inventory

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for this module

logger.info("job queue imported")


# Testing
if __name__ == '__main__':
    # Create formatter
    #formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

    # Logger: create console handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)     # set logging level for console
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.getLogger('Factory-Inventory').setLevel(logging.DEBUG)


    logger.info("Starting")
    logger.debug("Debug level")

    q = JobQueue()


    order = JobData(job_id=123, order_id=1, color='red', cook_time=12, sliced=True)
    q.add_job(order)
    order = JobData(job_id=123, order_id=1, color='white', cook_time=14, sliced=True)
    q.add_job(order)
    order = JobData(job_id=123, order_id=1, color='blue', cook_time=16, sliced=True)
    q.add_job(order)

    logger.info(q.has_jobs())
    q.print_jobs()

    q.cancel_job_order(order_id=32)
    q.print_jobs()

    q.cancel_job_id(job_id=1324)
    q.print_jobs()

    logger.info(q.has_jobs())

    logger.info(q.next_job())


    logger.info("Testing find next available job\n")

    # Queue pop inventory testing
    logging.getLogger("Factory_Inventory").setLevel(logging.INFO)

    inv = Inventory()
    inv.preset_inventory()

    job = q.next_available_job(inv)
    logger.info("Job return: %s", job)

    job = q.next_available_job(inv)
    logger.info("Job return: %s", job)

    job = q.next_available_job(inv)
    logger.info("Job return: %s", job)
    logger.info("End program")
