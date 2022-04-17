
""" Test program for Factory_Sim2 """

import logging
from time import sleep
from job_data import JobData
from factory.factory_sim2 import FactorySim2

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for module

def main():
    """ Main test function """
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
    #formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

    # Logger: create console handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)     # set logging level for console
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.getLogger('Factory_Sim2').setLevel(logging.DEBUG)

    fs = FactorySim2(processing_time=4)
    logger.info("Factory Status: %s", fs.status())

    order = JobData(job_id=123, order_id=1, color='blue', cook_time=16, sliced=True)
    order.add_slot((1,2))
    fs.order(order)

    fs.update()
    sleep(0.01)

    while fs.status() != 'ready':
        logger.info("Factory Status: %s", fs.status())
        fs.update()
        try:
            sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping")
            fs.stop()

    logger.info("Factory job completed. Status: %s", fs.status())
    logger.info("End test")


if __name__ == '__main__':
    main()
