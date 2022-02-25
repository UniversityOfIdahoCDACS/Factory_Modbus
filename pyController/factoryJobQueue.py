
# Depends on factory_inventory

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

class JOB_QUEUE():
    def __init__(self):
        self._data = []
        logger.debug("Job Queue initialized")


    def add_job(self, order_data):
        logger.debug("Adding order to queue: {}".format(order_data))
        self._data.append(order_data)


    def cancel_job_order(self, order_id=None):
        logger.info("Scanning queue to delete order_id: {}".format(order_id))
        items_deleted = 0
        return_msg = []
        for index, job in enumerate(self._data):
            logger.debug("Scanning Item: {}\tdata: {}".format(index, job))
            if job['order_id'] == order_id:
                return_msg.append("Deleting Job #: {} from order {}".format(job['job_id'], job['order_id']))
                logger.info(return_msg)
                del self._data[index]
                items_deleted += 1
        
        if items_deleted > 0:
            logger.info("Deleted {} jobs".format(items_deleted))
        else:
            logger.warning("Could not find any jobs matching order_id {}".format(order_id))
            return_msg = "Could not find any jobs matching order_id {}".format(order_id)
            return (1, return_msg)
        
        return  (0, return_msg)


    def cancel_job_id(self, job_id=None):
        logger.info("Scanning queue to delete job_id: {}".format(job_id))
        return_msg = ""
        for index, job in enumerate(self._data):
            logger.debug("Scanning Item: {}\tdata: {}".format(index, job))
            if job['job_id'] == job_id:
                return_msg = "Deleting Job #: {} from order {}".format(job['job_id'], job['order_id'])
                logger.info(return_msg)
                del self._data[index]
                return (0, return_msg)
        
        logger.warning("Could not find any jobs matching job_id {} found".format(job_id))

        return (1, "Could not find any jobs matching job_id {} found".format(job_id))


    # Returns number of jobs
    def has_jobs(self):
        return len(self._data)
    

    def print_jobs(self):
        if len(self._data) == 0:
            logger.info("No jobs available to print")
        else:
            for item in self._data:
                logger.info("Item: {}".format(item))
    
    
    def next_job(self):
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
            logger.debug("Looking at possible next job {}".format(job))
            job_color = job['color']
            logger.debug("> job color: {}".format(job_color))

            # Check inventory for color
            slot = inventory.pop_color(job_color)
            if slot is False: # no color found in inventory
                continue # look at next job
            else:
                logger.info("Found available job {} for color {} in slot {}".format(job, job_color, slot))
                del self._data[index]   # Delete job in queue
                return (job, slot)           # Pass back job data

        logger.info("Could not match waiting job with available inventory")
        return False
