"""This module tests the runability of factory_inventory.py"""

import logging
import factory_inventory

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

# Create formatter
#formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] [%(threadName)s] - %(message)s')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] [%(name)s] - %(message)s')

# Logger: create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)     # set logging level for console
ch.setFormatter(formatter)
logger.addHandler(ch)

# reduce logging level of specific libraries
logging.getLogger("inventoryHandler").setLevel(logging.DEBUG)

if __name__ == "__main__":
    i = factory_inventory.FACTORY_INVENTORY()
    i.preset_inventory()

    logger.info("Inventory: %s", i.get_inventory())
    logger.info("x1,y2: %s", i.get_slot(1, 2))
    logger.info("Qty red %s", i.get_quantity('red'))
    logger.info("Qty blue %s", i.get_quantity('blue'))
    logger.info("Qty white %s", i.get_quantity('white'))
    logger.info("Qty empty %s", i.get_quantity('empty'))
    logger.info("---------------")
    logger.info("Changing slot 1,2")
    i.set_slot(1, 2, 'empty')
    logger.info("x1,y2: %s", i.get_slot(1, 2))
    logger.info("Qty red %s", i.get_quantity('red'))
    logger.info("Qty blue %s", i.get_quantity('blue'))
    logger.info("Qty white %s", i.get_quantity('white'))
    logger.info("Qty empty %s", i.get_quantity('empty'))
    logger.info("---------------")
    logger.info("Qty blue %s", i.get_quantity('blue'))

    logger.info("poping a blue")
    slot = i.find_color('red')
    logger.info('blue in slot %s', slot)
    logger.info("Qty blue %s", i.get_quantity('blue'))

    logger.info("poping a blue")
    slot = i.pop_color('blue')
    logger.info('blue in slot %s', slot)
    logger.info("Qty blue %s", i.get_quantity('blue'))
    logger.info("poping a blue")

    logger.info("Inventory: %s", i.get_inventory())

    slot = i.pop_color('blue')
    logger.info('blue in slot %s', slot)
    logger.info("Qty blue %s", i.get_quantity('blue'))
    logger.info("poping a blue")

    slot = i.pop_color('blue')
    logger.info('blue in slot %s', slot)
    logger.info("Qty blue %s", i.get_quantity('blue'))

    logger.info("Inventory: %s", i.get_inventory())
