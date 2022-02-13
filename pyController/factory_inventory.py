
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
        self.preset_inventory()
        logger.debug("Factory Inventory Initialized")

    # Presets inventory to a known configuration
    def preset_inventory(self):
        self.inventory = [['red', 'empty', 'red'],
                        ['empty', 'white', 'white'],
                        ['blue', 'blue', 'blue']]
        logger.debug("Factory Inventory using preset configuration")

    # Returns entire inventory
    def get_inventory(self):
        logger.debug("Factory Inventory: {}".format(self.inventory))
        return self.inventory

    # Return number of items matching color in inventory
    def get_quantity(self, color):
        count = 0
        for row in self.inventory:
            count += row.count(color)
        logger.debug("Count of {}: {}".format(color, count))
        return count

    # Set value of slot
    def set_slot(self, x, y, color):
        self.inventory[x][y] = color
        logger.debug("Slot {},{} set to {}".format(x, y, color))

    # Return value of slot
    def get_slot(self, x, y):
        slot = self.inventory[x][y]
        logger.debug("Slot {},{} is {}".format(x, y, slot))
        return slot
    
    # Return x, y of a matching slot. Return False if not found
    def find_color(self, color):
        for row in enumerate(self.inventory):
            for column in enumerate(row):
                if column[1] == color:
                    logger.debug("Found{} in slot {},{}".format(color, row[0], column[0]))
                    return (row[0], column[0])
        logger.warning("Did not find {} in inventory".format(color))
        return False

    # Return x, y of a matching slot and mark slot as empty. Return False if not found
    def pop_color(self, color):
        for row in enumerate(self.inventory):
            for column in enumerate(row[1]):
                #logger.debug(">> item is {}".format(column))
                if column[1] == color:
                    logger.debug("Found{} in slot {},{}".format(color, row[0], column[0]))
                    self.set_slot(row[0], column[0], 'empty')
                    return (row[0], column[0])
        logger.warning("Did not find {} in inventory".format(color))
        return False