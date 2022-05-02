
""" Python Controller Orchastrator module """

import json
import logging

# factory modules import
from job_queue import JobQueue
from job_data import JobData
from inventory import Inventory

class Orchastrator():
    """ Python Controller Orchastrator
    This class orchastrates data between various sub objects
    """
    def __init__(self, mqtt=None, factory=None):
        # Logging
        self._logger = logging.getLogger('Orchastrator')
        self._logger.setLevel(logging.DEBUG) # sets default logging level for this module
        self._logger.info("Orchastrator initializing")

        # Setup Job Queue and Inventory objects
        self._job_queue = JobQueue()
        self._inventory = Inventory()
        self._inventory.preset_inventory()

        if factory is None:
            raise Exception("factory not specified")

        self._factory = factory
        self.mqtt = mqtt  # mqtt is optional

        self._current_job = None
        self._last_factory_state = None


    def add_job_callback(self, job_data):
        """ Add job data to Job queue """
        # Verify
        if not isinstance(job_data, JobData):
            log_msg = "Invalid new job data. Not job_data object"
            self._logger.error("%s", log_msg)

        # Add to queue
        self._job_queue.add_job(job_data)
        log_msg = f"Added job {job_data.job_id} for order {job_data.order_id} | color: {job_data.color},  cook time: {job_data.cook_time}, sliced: {job_data.sliced}"
        self._logger.info(log_msg)
        notice_msg = {'msg_type': 'job_status', 'job_id': job_data.job_id, 'message': 'Added to queue'}
        self.send_job_notice(notice_msg)


    def cancel_job_id_callback(self, job_id):
        """ Search job queue and delete matching job id """
        # Verify
        if not (isinstance(job_id, int) and job_id >= 0):
            log_msg = f"Error: Invalid cancel job id: {job_id}"
            self._logger.error(log_msg)
            notice_msg = {'msg_type': 'error', 'message': "Invalid id"}
            self.send_job_notice(notice_msg)
            return

        # Cancel Job
        canceled_list = self._job_queue.cancel_job_id(job_id)

        # Report
        if len(canceled_list) > 0:
            log_msg = f"Deleting Job #: {job_id}"
            notice_msg = {'msg_type': 'job_status', 'job_id': job_id, 'message': "Canceled"}
        else:
            log_msg = f"Could not find any jobs matching job_id {job_id} found"
            notice_msg = {'msg_type': 'error', 'message': f"Job id {job_id} not found"}
        self._logger.debug(log_msg)
        self.send_job_notice(notice_msg)


    def cancel_job_order_callback(self, order_id):
        """ Search job queue and delete all jobs matching order id """
        # Verify
        if not (isinstance(order_id, int) and order_id >= 0):
            log_msg = f"Error: Invalid cancel order id: {order_id}"
            self._logger.error(log_msg)
            notice_msg = {'msg_type': 'error', 'message': "Invalid id"}
            self.send_job_notice(notice_msg)
            return

        # Cancel order
        canceled_list = self._job_queue.cancel_job_order(order_id)

        # Report
        if len(canceled_list) > 0:             # If jobs were deleted
            for deleted_job_id in canceled_list:
                log_msg = f"Deleting Job #: {deleted_job_id} from order {order_id}"
                notice_msg = {'msg_type': 'job_status', 'job_id': deleted_job_id, 'message': "Canceled"}
                self._logger.debug(log_msg)
                self.send_job_notice(notice_msg)
        else:                                  # if no Jobs were canceled
            log_msg = f"Could not find any jobs matching order_id {order_id}"
            notice_msg = {'msg_type': 'error', 'message': f"Order id {order_id} not found"}
            self._logger.debug(log_msg)
            self.send_job_notice(notice_msg)


    def factory_command_callback(self, command, **args):
        """ Calls factory.command with supplied args """
        self._logger.debug("Factory command: %s, args: %r", command, args)
        if command == 'reset_inventory':
            self._inventory.preset_inventory()

    def send_inventory(self):
        """ Get current inventory and send to mqtt """
        if self.mqtt is not None:
            inv = {}
            inv['Inventory'] = self._inventory.get_inventory()
            self._logger.info("Inventory: %s", inv['Inventory'])

            self.mqtt.publish('Factory/Inventory', payload=json.dumps(inv), qos=0)
        return


    def send_status(self):
        """ Get status and send to mqtt """
        if self.mqtt is not None:
            status = {}
            status['factory_status'] = self._factory.status()

            if self._current_job is None:
                status['current_job'] = "None"
            else:
                status['current_job'] = str(self._current_job.job_id)

            status['job_queue_len'] = str(self._job_queue.has_jobs())
            self.mqtt.publish("Factory/Status", payload=json.dumps(status), qos=0)
        return


    def send_job_notice(self, msg):
        """ Sents attached message to Job_notice mqtt topic """
        if self.mqtt is not None:
            self.mqtt.publish("Factory/Job_notice", payload=json.dumps(msg), qos=2)
        return


    def factory_update(self):
        """Run the factory's update function.
           This should be called every 1-5 seconds"""
        factory_state = self._factory.update()
        self._logger.debug("Factory state: %s", factory_state)

        # If factory just finished processing
        if factory_state == 'ready' and self._last_factory_state == 'processing':
            # Job finished
            message = f"Job {self._current_job.job_id} has been completed"
            self._logger.info(message)

            notice_msg = {'msg_type': 'job_status', 'job_id': self._current_job.job_id, 'message': 'Completed'}
            self.send_job_notice(notice_msg)
            self._current_job = None
            self.send_status()

        # If factory ready, start a job if available
        elif factory_state == 'ready' and self._job_queue.has_jobs():
            self._logger.info("Starting job")
            self.factory_start_job()

        elif factory_state == 'processing':
            self._logger.debug("Factory processing...")

        self._last_factory_state = factory_state


    def factory_start_job(self):
        '''Start factory operation'''
        if self._job_queue.has_jobs():
            # Pop next job
            current_job = self._job_queue.next_available_job(self._inventory) # returns job or False

            if current_job is False: # No job ready
                self._logger.debug("Could not match waiting job with available inventory")
                return
            else:
                self._current_job = current_job

            # Send to factory
            self._factory.order(current_job)

            message = f"Started job {current_job.job_id}"
            self._logger.info(message)

            # Send updated information
            notice_msg = {'msg_type': 'job_status', 'job_id': current_job.job_id, 'message': 'Started'}
            self.send_job_notice(notice_msg)
            self.send_status()
            self.send_inventory()
        return
