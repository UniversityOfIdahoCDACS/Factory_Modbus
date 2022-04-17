
"""
Factory Job Queue class
Depends on inventory & job_data for some functions
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
        logger.debug("Adding order to queue: %s", order_data.job_info())
        self._data.append(order_data)


    def cancel_job_order(self, order_id=None):
        """
        Search all jobs and delete each job with matching order ID
        """
        logger.info("Scanning queue to delete order_id: %s", order_id)
        canceled_jobs = []
        for index, job in enumerate(self._data):
            logger.debug("Scanning Item: %d\tdata: %s", index, job.job_info())
            if job.order_id == order_id:
                log_msg = f"Deleting Job #: {job.job_id} from order {job.order_id}"
                canceled_jobs.append(job.job_id)
                logger.info(log_msg)
                del self._data[index]

        if len(canceled_jobs) > 0:
            logger.info("Deleted %d jobs", len(canceled_jobs))
        else:
            log_msg = f"Could not find any jobs matching order_id {order_id}"
            logger.warning(log_msg)
            return [] # return with empty list of deleted jobs

        return canceled_jobs # return list of deleted jobs


    def cancel_job_id(self, job_id=None):
        """Search queue for job id and delete"""
        logger.info("Scanning queue to delete job_id: %s", job_id)
        for index, job in enumerate(self._data):
            logger.debug("Scanning Item: %s\tdata: %s", index, job.job_info())
            if job.job_id == job_id:
                log_msg = f"Deleting Job #: {job.job_id} from order {job.order_id}"
                logger.info(log_msg)
                del self._data[index]
                return [job_id] # return list of deleted jobs

        log_msg = f"Could not find any jobs matching job_id {job_id} found"
        logger.warning(log_msg)
        return [] # return with empty list of deleted jobs


    # Returns number of jobs
    def has_jobs(self):
        """Return queue length"""
        return len(self._data)


    def print_jobs(self):
        """Print out job data"""
        if len(self._data) == 0:
            logger.info("No jobs available to print")
        else:
            for job in self._data:
                logger.info("Item: %s", job.job_info())


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
            logger.debug("Looking at possible next job %s", job.job_info())
            job_color = job.color
            logger.debug("> job color: %s", job_color)

            # Check inventory for color
            slot = inventory.pop_color(job_color)
            if slot is False: # no color found in inventory
                continue # look at next jobdf
            else:
                job.add_slot(slot)      # Add slot data to job

            logger.info("Found available job id %s for color %s in slot %s", job.job_id, job_color, slot)
            del self._data[index]   # Delete job in queue
            return job              # Pass back job data

        logger.info("Could not match waiting job with available inventory")
        return False
