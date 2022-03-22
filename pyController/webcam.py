
"""
Factory webcam control class
"""

import logging
import time
import threading
import base64
import json
import cv2 as cv

class Webcam():
    """ Factory webcam control class """

    def __init__(self, rate=10, mqtt=None, source=None):
        self.logger = logging.getLogger("Webcam")
        self.logger.setLevel(logging.WARN) # sets default logging level for this module

        self.mqtt = mqtt
        self.rate = rate
        self.worker_thread = None
        self.worker_thread_stop = False
        self.source = source

        # Object to capture the frames
        self.cap = cv.VideoCapture(0)

        self.logger.info("Initialized webcam")


    def start(self):
        """ Start webcam thread """
        self.logger.info("Starting webcam thread")
        self.worker_thread = threading.Thread(target=self.worker, args=(self.rate,))
        self.worker_thread.start()


    def stop(self):
        """ Stops web cam thread """
        self.logger.info("Stopping webcam thread")
        self.worker_thread_stop = True  # Set flag for thread to stop
        if self.worker_thread is not None:
            self.worker_thread.join()   # Wait for thread to stop

        self.cap.release()              # Release capture


    def update(self):
        """ Checks status and makes sure thread and capture source is still good """
        if not self.worker_thread.is_alive():
            self.logger.info("Webcam thread stopped.. restarting")
            self.worker_thread.start()



    def worker(self, rate):
        """ Takes a picture, encodes, then sends the image to mqtt """
        wait_period = float(1 / rate)
        while not self.worker_thread_stop:
            start = time.time()
            jpg_as_text = self.get_image()

            # self.convert_text_to_image(jpg_as_text)

            if len(jpg_as_text) > 10:
                self.send_image(jpg_as_text)

            end = time.time()
            dt = end - start
            sleep_time = max(0, wait_period - dt)
            self.logger.debug(f"dt: {dt:.4f} | sleep time: {sleep_time:.4f} | wait period: {wait_period:.4f}")
            time.sleep(sleep_time)
        
        self.logger.info("Webcam worker thread exiting")


    def get_image(self):
        # Source: https://stackoverflow.com/a/40930153
        """ Get image from capture source """
        # Read Frame
        retval, image = self.cap.read()
        self.logger.debug("Image shape: %s", image.shape)

        # Encode frame to jpg
        # Params doc: https://docs.opencv.org/3.4/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac
        retval, buffer = cv.imencode('.jpg', image, params=[cv.IMWRITE_JPEG_QUALITY, 50])
        self.logger.debug("Encoded shape: %s",buffer.shape)

        # Endode jpg to base64
        jpg_as_text = base64.b64encode(buffer)
        self.logger.debug("Text len: %s", len(jpg_as_text))

        return jpg_as_text


    def get_fake_image(self):
        # TODO
        # Look at
        # https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv

        """ Get image from capture source """

        import urllib2
        import numpy as np

        req = urllib2.urlopen('http://answers.opencv.org/upfiles/logo_2.png')
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv.imdecode(arr, -1) # 'Load it as it is'

        cv.imshow('lalala', image)
        if cv.waitKey() & 0xff == 27: quit()

        # Encode frame to jpg
        # Params doc: https://docs.opencv.org/3.4/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac
        retval, buffer = cv.imencode('.jpg', image, params=[cv.IMWRITE_JPEG_QUALITY, 50])
        self.logger.debug("Encoded shape: %s",buffer.shape)

        # Endode jpg to base64
        jpg_as_text = base64.b64encode(buffer)
        self.logger.debug("Text len: %s", len(jpg_as_text))

        return jpg_as_text


    def convert_text_to_image(self, jpg_as_text):
        """ Decode base64 and write image to file """
        # Convert back to binary
        jpg_original = base64.b64decode(jpg_as_text)

        # Write to a file to show conversion worked
        with open('image.jpg', 'wb') as f_output:
            f_output.write(jpg_original)


    def send_image(self, data):
        """ Send image data to mqtt broker """
        # This might be handled one layer up
        if self.mqtt is not None:
            msg = { "webcam_status" : "simulated", "image_data" : f"{data}" }
            #msg = { "webcam_status" : "offline", "image_data" : f"Fake Data aabbccddeeffgg" }
            #self.logger.debug(f"Webcam data: \n{data}")
        else:
            msg = { "webcam_status" : "offline", "image_data" : f"{data}" }
            #print(msg)
            #self.logger.info(f"Webcam data: \n{data}")


        # Send to mqtt broker
        if self.mqtt is not None:
            self.mqtt.publish("Factory/Webcam", payload=json.dumps(msg), qos=0)
