
import time
import logging
import threading

# Import factory modules
from factory.modbus import MODBUS       # Modbus communication client
from factory.module_hbw import HBW      # Mini-Factory module: High Bay Warehouse
from factory.module_vgr import VGR      # Mini-Factory module: Vacume Gripper Robot
from factory.module_mpo import MPO      # Mini-Factory module: mpo??
from factory.module_sld import SLD      # Mini-Factory module: sld
from factory.module_ssc import SSC_LED  # Mini-Factory module: ssc
from factory.module_ssc_webcam import SSC_Webcam      # Mini-Factory module: SSC Webcam



#*****************************
#*         FACTORY           *
#*****************************
class FACTORY():
    def __init__(self, ip, port):
        # Setup Logger
        self.logger = logging.getLogger("Factory")
        self.logger.setLevel(logging.DEBUG) # sets default logging level for module

        self.logger.info("Factory Initializing...")

        # Setup Modules
        self._mb = MODBUS(ip, port)
        self._hbw = HBW(self._mb)
        self._vgr = VGR(self._mb)
        self._mpo = MPO(self._mb)
        self._sld = SLD(self._mb)
        self._ssc = SSC_LED(self._mb)
        self._ssc_webcam = SSC_Webcam(self._mb)

        #check ready status
        self._status_details = None
        self.status()

        # Factory processing variables
        self._factory_state = 'ready'       # Status of the factory
        self._processing_thread = None      # Tread object when active
        self._processing_thread_stop = False # Stop flag for processing thread
        self._job_data = None               # Holds job data such as x, y, cook time and slice info

        # Send Factory reset to all modules
        self.reset_factory()

        self.logger.debug("Factory Modbus Initialized")

    def status(self):
        """ Test each module and return a factory status
        Tests each module's fault and ready flags
        Generate a status_detailed dictionary object
        Return factory status string
        """
        factory_status = 'offline'
        modules = [self._hbw, self._vgr, self._mpo, self._sld]

        # Test if online
        self._mb.connection_check()

        # Test each module
        modules_ready_status = []
        modules_faulted_status = []
        modules_statuses = []
        for module in modules:
            module_faulted = module.IsFault()
            module_ready = module.IsReady()

            # Add to lists
            modules_faulted_status.append(module_faulted)
            modules_ready_status.append(module_ready)

            # Module summary (Module name, module faulted, module ready)
            modules_statuses.append((module.name, module_faulted, module_ready))

        # if any module is faulted, Factory is in Fault state
        # if all modules are ready, Factory is in a ready state
        if any(modules_faulted_status):
            factory_status = 'fault'
        elif all(modules_ready_status):
            factory_status = 'ready'
        else:
            factory_status = 'processing'

        # Detailed status report
        self._status_details = {'factory_status': factory_status,          # Factory status
                                'modules_faulted': modules_faulted_status, # List of bools of faulted modules
                                'modules_ready': modules_ready_status,     # List of bools of ready modules
                                'modules_statuses': modules_statuses }     # List: module_name, faulted, ready
        


        return factory_status

    def status_detailed(self):
        """ Calls Factory.status() and returns detailed information """
        self.status()
        return self._status_details

    def _check_factory_faults(self):
        """ Checks all modules for faults.
        Return true if any faulted
        """
        modules = [self._hbw, self._vgr, self._mpo, self._sld]
        for module in modules:
            if module.IsFault():
                self.logger.warning("Factroy Module %s in fault. Halted factory processing", module.name)
                self._processing_thread_stop = True
                self._factory_state == 'fault'
                return True
        return False

    def reset_factory(self):
        """ Sends reset task to all modules """
        modules = [self._hbw, self._vgr, self._mpo, self._sld, self._ssc, self._ssc_webcam]
        for module in modules:
            module.Reset()

    def stop(self):
        """ Stops factory opperations """
        self._processing_thread_stop = True

    def update(self):
        """
        This function should be called periodically every 1-5 seconds
        This checks the factory state and starts jobs as needed
        """
        if self._factory_state == 'ready':
            if self._job_data is not None:
                # Start job
                self.logger.info("Factory starting processing of a job")
                self._factory_state = 'processing'

                # Start thread
                self.logger.info("Starting processing thread")
                self._processing_thread_stop = False
                self._processing_thread = threading.Thread(target=self._process_order)
                self._processing_thread.start()

        elif self._factory_state == 'processing':
            self.logger.debug("Factory processing an order")
            if not self._processing_thread.is_alive():
                self.logger.info("Job completed")
                if self._check_factory_faults():
                    self._factory_state = 'fault'
                else:
                    self._factory_state = 'ready'

        elif self._factory_state == 'offline':
            self.logger.debug("Factory is offline")

        elif self._factory_state == 'fault':
            self.logger.debug("Factory in fault state")

            # check to see if factory recovered
            if self.status() == 'ready':
                # Reset processing variables. Assuming clean slate
                self._factory_state = 'ready'
                self._processing_thread_stop = True  # Probably redundant in most cases
                self._job_data = None

        else:
            raise Exception("Invalid factory_state set")

        return self._factory_state

    def order(self, job_data):
        """ Load processing job order """
        if self._factory_state == 'ready':
            self.logger.info("Factory importing job data")
            self._job_data = job_data
            return 0
        else:
            self.logger.error("Factory not ready. Not accepting job")
            return 1

    def _process_order(self):
        """ Main order sequence for factory
        Expects self._job_data to be populated
        """
        # Parse Job data
        x_value = self._job_data.slot_x + 1
        y_value = self._job_data.slot_y + 1
        cook_time = self._job_data.cook_time
        do_slice = self._job_data.sliced

        self.logger.info("Factory process started")
        self.logger.debug("X: %d, Y: %d", x_value, y_value)

        def stage_1(x_value, y_value):
            """
            Stage 1
            _hbw -> _vgr -> _mpo also _hbw return pallet
            """
            print("Stage 1 entered")
            hbw_ready_status = self._hbw.IsReady()
            # Run _hbw
            if hbw_ready_status == True:
                print("hbw Is Ready")
                self._hbw.StartTask1(x_value, y_value) #_hbw STARTS
            else:
                print("hbw Is Not Ready")

            # Run _vgr and _hbw return
            while not self._processing_thread_stop:
                hbw_ready_status = self._hbw.IsReady()

                if self._hbw.CurrentProgress() == 80:
                    self._vgr.StartTask1() #_vgr STARTS
                elif hbw_ready_status == True:
                    time.sleep(2)
                    self._hbw.StartTask2(x_value, y_value) # Return Pallet
                    break
                time.sleep(0.1)

                if self._check_factory_faults():
                    return


        def stage_2():
            """
            Stage 2 - Wait for puck to arrive at MPO and start MPO
            """
            print("Stage 2 entered")
            while not self._processing_thread_stop:
                mpo_start_light = self._mpo.StartSensorStatus()
                if mpo_start_light == False:
                    print("Starting mpo task")
                    time.sleep(1)
                    self._mpo.StartTask1() #Add values to change
                    break
                time.sleep(0.1)

                if self._check_factory_faults():
                    return

        def stage_3():
            """
            Stage 3 - Wait for MPO finish & start SLD task
            """
            print("Stage 3 entered")
            while not self._processing_thread_stop:
                mpo_end_light = self._mpo.EndSensorStatus()
                if mpo_end_light == False:
                    self._sld.StartTask1()
                    break
                time.sleep(0.1)

                if self._check_factory_faults():
                    return

        def stage_4():
            """
            Stage 4 - Wait for SLD to finish
            """
            print("Stage 4 entered")
            while not self._processing_thread_stop and not self._sld.IsReady():
                time.sleep(0.1)

                if self._check_factory_faults():
                    return


        if not self._processing_thread_stop:
            stage_1(x_value, y_value)

        if not self._processing_thread_stop:
            stage_2()

        if not self._processing_thread_stop:
            stage_3()

        if not self._processing_thread_stop:
            stage_4()

        self._job_data = None        # Clear job data that just completed
        self._processing_thread_stop # Clear stop flag
        return

    def _restock(self):
        pass


#*****************************
#*           MAIN            *
#*****************************
if __name__ == '__main__':
    #Main is not used
    print("******************************")
    print("* start factory with         *")
    print("* $python3 pyController.py   *")
    print("*            or              *")
    print("* $python3 test_factory.py   *")
    print("******************************")
