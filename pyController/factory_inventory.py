"""Factory inventory class"""

import logging

logger = logging.getLogger('Factory_Inventory')
logger.setLevel(logging.DEBUG) # sets default logging level for all modules

class FACTORY_INVENTORY():
    '''
    x : row
    y : column
    '''

    def __init__(self):
        self.inventory = []
        logger.debug("Factory Inventory Initialized")

    # Presets inventory to a known configuration
    def preset_inventory(self):
        """Presets inventory to a known configuration """
        self.inventory = [['red', 'empty', 'red'],
                        ['empty', 'white', 'white'],
                        ['blue', 'blue', 'blue']]
        logger.debug("Factory Inventory using preset configuration")

    # Returns entire inventory
    def get_inventory(self):
        """Returns entire inventory"""
        logger.debug("Factory Inventory: %s", self.inventory)
        return self.inventory

    # Return number of items matching color in inventory
    def get_quantity(self, color):
        """Return number of items matching color in inventory"""
        count = 0
        for row in self.inventory:
            count += row.count(color)
        logger.debug("Count of %s: %d", color, count)
        return count

    # Set value of slot
    def set_slot(self, slot_x, slot_y, color):
        """Set value of slot"""
        self.inventory[slot_x][slot_y] = color
        logger.debug("Slot %d,%d set to %s", slot_x, slot_y, color)

    # Return value of slot
    def get_slot(self, slot_x, slot_y):
        """Return value of slot"""
        slot = self.inventory[slot_x][slot_y]
        logger.debug("Slot %d,%d is %s", slot_x, slot_y, slot)
        return slot

    # Return x, y of a matching slot. Return False if not found
    def find_color(self, color):
        """
        Return x, y of a matching slot.
        Return False if not found
        """
        for row_index, row in enumerate(self.inventory):
            for column_index, item in enumerate(row):
                if item == color:
                    logger.debug("Found{} in slot {},{}".format(color, row_index, column_index))
                    return (row_index, column_index)
        logger.warning("Did not find {} in inventory".format(color))
        return False

    # Return x, y of a matching slot and mark slot as empty. Return False if not found
    def pop_color(self, color):
        """
        Return x, y of a matching slot and mark slot as empty.
        Return False if not found
        """
        for row_index, row in enumerate(self.inventory):
            for column_index, item in enumerate(row):
                #logger.debug(">> item is {}".format(item))
                if item == color:
                    logger.debug("Found{} in slot {},{}".format(color, row_index, column_index))
                    self.set_slot(row_index, column_index, 'empty')
                    return (row_index, column_index)
        logger.warning("Did not find {} in inventory".format(color))
        return False
