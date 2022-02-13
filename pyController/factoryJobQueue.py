

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

logger.info("job queue imported")
logger.debug("job queue imported - debug")


class JOB_QUEUE():
    def __init__(self):
        self.data = []


    def add_job(self, order_data):
        logger.debug("Adding order to queue: {}".format(order_data))
        self.data.append(order_data)


    def cancel_job_order(self, order_id=None):
        logger.info("Scanning queue to delete order_id: {}".format(order_id))
        items_deleted = 0
        return_msg = []
        for item in enumerate(self.data):
            logger.debug("Scanning Item: {}\tdata: {}".format(item[0], item[1]))
            if item[1]['order_id'] == order_id:
                return_msg.append("Deleting Job #: {} from order {}".format(item[1]['job_id'], item[1]['order_id']))
                logger.info(return_msg)
                del self.data[item[0]]
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
        for item in enumerate(self.data):
            logger.debug("Scanning Item: {}\tdata: {}".format(item[0], item[1]))
            if item[1]['job_id'] == job_id:
                return_msg = "Deleting Job #: {} from order {}".format(item[1]['job_id'], item[1]['order_id'])
                logger.info(return_msg)
                del self.data[item[0]]
                return (0, return_msg)
        
        logger.warning("Could not find any jobs matching job_id {} found".format(job_id))

        return (1, "Could not find any jobs matching job_id {} found".format(job_id))


    # Returns number of jobs
    def has_jobs(self):
        return len(self.data)
    

    def print_jobs(self):
        if len(self.data) == 0:
            logger.info("No jobs available to print")
        else:
            for item in self.data:
                logger.info("Item: {}".format(item))
    
    
    def next_job(self):
        if len(self.data) == 0:
            logger.warning("No items in queue!")
            return 0
        
        return self.data.pop()


