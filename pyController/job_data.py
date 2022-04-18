""" Job data class """

class JobData():
    """ This class holds and validataes job specific data """
    def __init__(self, job_id=None, order_id=None, color=None, cook_time=None, sliced=None):
        if self._validate_int(job_id):
            self.job_id = job_id

        if self._validate_int(order_id):
            self.order_id = order_id

        if isinstance(color, str):
            self.color = color
        else:
            raise AttributeError("Color is not a string")

        if self._validate_int(cook_time):
            self.cook_time = cook_time

        if isinstance(sliced, bool):
            self.sliced = sliced

        # X, Y slot can be added later
        self.slot = None

    def _validate_int(self, data):
        """ Validate input
        Test if Int and int > 0
        """
        if not isinstance(data, int):
            print("Not happy 1")
            raise AttributeError("Not an integer")
        elif data < 0:
            print("not happy 2")
            raise AttributeError("Negative number not accepted")
        else:
            return True

    def job_info(self):
        """ Return string of job attributes
        Mainly used for logging outputs
        """
        return f"job_id: {self.job_id}, order_id: {self.order_id}, color: {self.color}, cook time: {self.cook_time}, slice time {self.sliced}"

    def add_slot(self, slot):
        """ Adds slot information (x, y) to job_data """
        self.slot = slot
