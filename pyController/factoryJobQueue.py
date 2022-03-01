
"""
Factory Job Queue class
Depends on factory_inventory
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # sets default logging level for this module

class JobQueue():
    """
    Factory Job Queue class
    Depends on factory_inventory
    """
    def __init__(self):
        """Initialize"""
        self._data = []
        logger.debug("Job Queue initialized")


    def add_job(self, order_data):
        """Add job to Queue"""
        logger.debug("Adding order to queue: %s", order_data)
        self._data.append(order_data)


    def cancel_job_order(self, order_id=None):
        """
        Search all jobs and delete each job with matching order ID
        """
        logger.info("Scanning queue to delete order_id: %s", order_id)
        items_deleted = 0
        return_msg = []
        for index, job in enumerate(self._data):
            logger.debug("Scanning Item: %d\tdata: %s", index, job)
            if job['order_id'] == order_id:
                return_msg.append(f"Deleting Job #: {job['job_id']} from order {job['order_id']}")
                logger.info(return_msg)
                del self._data[index]
                items_deleted += 1

        if items_deleted > 0:
            logger.info("Deleted %s jobs", items_deleted)
        else:
            return_msg = f"Could not find any jobs matching order_id {order_id}"
            logger.warning(return_msg)
            return (1, return_msg)

        return  (0, return_msg)


    def cancel_job_id(self, job_id=None):
        """Search queue for job id and delete"""
        logger.info("Scanning queue to delete job_id: %s", job_id)
        return_msg = ""
        for index, job in enumerate(self._data):
            logger.debug("Scanning Item: %s\tdata: %s", index, job)
            if job['job_id'] == job_id:
                return_msg = f"Deleting Job #: {job['job_id']} from order {job['order_id']}"
                logger.info(return_msg)
                del self._data[index]
                return (0, return_msg)

        return_msg = f"Could not find any jobs matching job_id {job_id} found"
        logger.warning(return_msg)
        return (1, return_msg)


    # Returns number of jobs
    def has_jobs(self):
        """Return queue length"""
        return len(self._data)


    def print_jobs(self):
        """Print out job data"""
        if len(self._data) == 0:
            logger.info("No jobs available to print")
        else:
            for item in self._data:
                logger.info("Item: %s", item)


    def next_job(self):
        """
        Pops next job if available & return job info
        """
        if len(self._data) == 0:
            logger.warning("No items in queue!")
            return 0

        return self._data.pop()

    # pop next job with available inventory
    def next_available_job(self, inventory):
        '''
        Look at first job
        Get it's color
        Try to pop an inventory slot with color
            if yes, pop job
            if no, pass to next job
        '''
        for index, job in enumerate(self._data):
            logger.debug("Looking at possible next job %s", job)
            job_color = job['color']
            logger.debug("> job color: %s", job_color)

            # Check inventory for color
            slot = inventory.pop_color(job_color)
            if slot is False: # no color found in inventory
                continue # look at next jobdf

            logger.info("Found available job %s for color %s in slot %s", job, job_color, slot)
            del self._data[index]   # Delete job in queue
            return (job, slot)           # Pass back job data

        logger.info("Could not match waiting job with available inventory")
        return False
