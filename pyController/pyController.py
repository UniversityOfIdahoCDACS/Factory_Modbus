
""" Python Factory 4.0 Controller """

import time
import os
import logging
from logging.handlers import RotatingFileHandler

# factory modules import
import utilities
from orchastrator import Orchastrator
# from job_data import JobData                  # Used when manually adding a job at startup
from mqtt import Factory_MQTT
import webcam
from factory.factory import FACTORY             # Real factory
from factory.factory_sim2 import FactorySim2    # Simulated factory
from webapp import webadmin


#*********************************************
#* * * * * * * * * Logger Setup * * * * * * * *
#*********************************************

# Logger: logging config   https://docs.python.org/3/howto/logging-cookbook.html
# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for this module

# Create formatter
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

# Logger: create rotating file handler
script_dir = os.path.dirname(os.path.realpath(__file__))    # Directory this script is running from
utilities.create_log_dir(script_dir + "/logs")                    # creates /logs directory if missing
rfh = RotatingFileHandler(script_dir + "/logs/app.log")
rfh.maxBytes = 1024*1024          # maximum size of a log before being rotated
rfh.backupCount = 2               # how many rotated files to keep
rfh.setFormatter(formatter)     # set format
rfh.setLevel(logging.DEBUG)     # set level for file logging
logger.addHandler(rfh)          # add filehandle to logger

# Logger: create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)     # set logging level for console
ch.setFormatter(formatter)
logger.addHandler(ch)

# reduce logging level of specific libraries
logging.getLogger("jobQueue").setLevel(logging.DEBUG)
logging.getLogger("paho.mqtt.client").setLevel(logging.INFO)
logging.getLogger("Factory_MQTT").setLevel(logging.INFO)
logging.getLogger("Factory").setLevel(logging.DEBUG)
logging.getLogger("pymodbus").setLevel(logging.INFO)


def main():
    '''pyController main program'''

    logging.info("Starting factory python controller")

    # Signal handler
    killer = utilities.GracefulKiller()

    # Get environment configs
    config = utilities.load_env()

    logging.info("Starting factory MQTT")
    mqtt = Factory_MQTT(URL=config['MQTT_BROKER_URL'], PORT=int(config['MQTT_PORT']),
                                    CLIENT_ID=config['MQTT_CLIENT_ID'], TOPIC_SUB=config['MQTT_SUBSCRIBE'])
    mqtt.connect()
    time.sleep(1)
    mqtt.start()


    # Setup factory object
    logging.debug("Creating factory object")
    if config['FACTORY_SIM'] == 'True': # Use FactorySim2
        logging.info("Using Factory sim")
        factory = FactorySim2(processing_time=30)
    else:
        logging.info("Using Factory Modbus")
        factory = FACTORY(config['FACTORY_IP'], config['FACTORY_PORT'])

    # Setup webcam
    if config['FAKE_WEBCAM'] == 'True':
        logging.debug("Using fake image source")
        my_webcam = webcam.Webcam(rate=10, mqtt=mqtt)
        my_webcam.start()

    else:
        logging.debug("Using real camera")
        my_webcam = webcam.Webcam(rate=10, mqtt=mqtt, source=0)
        my_webcam.start()


    # Setup orchastrator object
    orchastrator = Orchastrator(mqtt=mqtt, factory=factory)

    # Setup webadmin object
    webadmin.webapp_storage.set_orchastrator(orchastrator)
    webadmin.start_webapp()

    # set mqtt orchastrator callbacks
    mqtt.set_add_job_callback(orchastrator.add_job_callback)
    mqtt.set_cancel_job_callback(orchastrator.cancel_job_id_callback)
    mqtt.set_cancel_order_callback(orchastrator.cancel_job_order_callback)
    mqtt.set_factory_command_callback(orchastrator.factory_command_callback)

    # Manually add job to orchastrator
    # add_job = JobData(job_id=123, order_id=100, color='white', cook_time=12, sliced=True)
    # orchastrator.add_job_callback(add_job)

    logging.info("Starting main loop")
    count = 0
    while not killer.kill_now:
        try:
            count += 1
            time.sleep(1)
        except KeyboardInterrupt:
            break

        if count % 2 == 0:
            orchastrator.factory_update()
            mqtt.update()
            my_webcam.update()

        if count % 15 == 0:
            orchastrator.send_status()

        if count % 60 == 0:
            orchastrator.send_inventory()

        if count > 600:
            if config['FACTORY_SIM'] == 'True':
                # Periodically reset inventory when running factory sim
                logging.info("Resetting Inventory")
                orchastrator.factory_command_callback('reset_inventory')
            count = 0

    # Shutdown
    logging.info("Shutting down gracefully")
    my_webcam.stop()
    factory.stop()
    mqtt.stop()


if __name__ == '__main__':
    main()
