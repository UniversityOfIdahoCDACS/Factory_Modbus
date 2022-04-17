
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
        self._job_data = None               # Holds job data such as x, y, cook time and slice info

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
                self._processing_thread = threading.Thread(target=self.process_order)
                self._processing_thread.start()

        elif self._factory_state == 'processing':
            self.logger.debug("Factory processing an order")
            if not self._processing_thread.is_alive():
                self.logger.info("Job completed")
                self._factory_state = 'ready'

        elif self._factory_state == 'offline':
            self.logger.debug("Factory is offline")

        elif self._factory_state == 'fault':
            self.logger.debug("Factory in fault state")

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


    def process_order(self):
        """ Main order sequence for factory
        Expects self._job_data to be populated
        """
        # Parse Job data
        x_value = self._job_data.slot[0]
        y_value = self._job_data.slot[1]
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
                print("_hbw Is Ready")
                self._hbw.StartTask1(x_value, y_value) #_hbw STARTS
            else:
                print("_hbw Is Not Ready")

            # Run _vgr and _hbw return
            while True:
                hbw_ready_status = self._hbw.IsReady()

                if self._hbw.CurrentProgress() == 80:
                    self._vgr.StartTask1() #_vgr STARTS
                elif hbw_ready_status == True:
                    time.sleep(2)
                    self._hbw.StartTask2(x_value, y_value)#Return Pallet
                    break
                time.sleep(0.1)

        def stage_2():
            """
            Stage 2
            """
            print("Stage 2 entered")
            while True:
                mpo_start_light = self._mpo.StartSensorStatus()
                if mpo_start_light == False:
                    print("Starting _mpo task")
                    time.sleep(1)
                    self._mpo.StartTask1()#Add values to change
                    break
                time.sleep(0.1)

        def stage_3():
            """
            Stage 3
            """
            print("Stage 3 entered")
            while True:
                mpo_end_light = self._mpo.EndSensorStatus()
                #print("stage 3 end light: "+mpo_end_light)
                if mpo_end_light == False:
                    self._sld.StartTask1()
                    break
                time.sleep(0.1)

        stage_1(x_value, y_value)
        stage_2()
        stage_3()
        self._job_data = None # Clear job data that just completed
        return


    def restock(self):
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
