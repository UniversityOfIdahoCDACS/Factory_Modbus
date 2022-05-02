
"""This module tests the runability of pyController.py"""

import logging
from job_data import JobData
from factory.factory_sim2 import FactorySim2    # Simulated factory
from orchastrator import Orchastrator
from webapp import webadmin

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG) # sets default logging level for this module

def main():
    """Main Function"""
    logger.info("test pyController started")

    logger.debug("Creating Job and orchastrator")

    # Setup factory sim object
    factory = FactorySim2()

    # Setup orchastrator object
    orchastrator = Orchastrator(mqtt=None, factory=factory)

    # Setup webadmin object
    # webadmin.webapp_storage.set_orchastrator(orchastrator)
    # webadmin.start_webapp()

    # Add jobs
    logger.info("Running Tests")
    add_job = JobData(job_id=123, order_id=100, color='red', cook_time=12, sliced=True)
    orchastrator.add_job_callback(add_job)
    add_job = JobData(job_id=124, order_id=100, color='red', cook_time=12, sliced=True)
    orchastrator.add_job_callback(add_job)
    add_job = JobData(job_id=125, order_id=201, color='red', cook_time=12, sliced=True)
    orchastrator.add_job_callback(add_job)
    add_job = JobData(job_id=126, order_id=201, color='red', cook_time=12, sliced=True)
    orchastrator.add_job_callback(add_job)
    add_job = JobData(job_id=127, order_id=201, color='red', cook_time=12, sliced=True)
    orchastrator.add_job_callback(add_job)

    # Cancel some orders and jobs
    orchastrator.cancel_job_id_callback(124)
    orchastrator.cancel_job_id_callback(1256)
    orchastrator.cancel_job_order_callback(201)
    orchastrator.cancel_job_order_callback(201201)


if __name__ == '__main__':
    main()
