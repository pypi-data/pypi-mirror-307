import hid
import logging
from monitorcontrol import get_monitors

class DeviceListener():

    def __init__(self, trigger_device: str, event_queue: list):

        self.trigger_device = trigger_device
        self.event_queue = event_queue

        self.logger = logging.getLogger()
        self.running = True

    @staticmethod
    def scan(logger):
        all_hids = hid.enumerate()
        unique_devices = set()
        logger.info("Detected the following devices connected to your PC..")
        for device in all_hids:
            product_name = device["product_string"]
            unique_devices.add(product_name)
        
        for product_name in unique_devices:
            logger.info(product_name)

        return list(unique_devices)
    
    @staticmethod
    def get_monitors():
        return get_monitors()
 
    def listen(self):
        
        all_hids = hid.enumerate()

        if self.trigger_device in [device["product_string"] for device in all_hids]:
            self.logger.info("Your trigger device {} is connected to your main setup".format(self.trigger_device))
            self.logger.info("Add main event to queue")
            self.event_queue.append("main")

        else:
            self.logger.info("Your trigger device is not connected to your main setup")
            self.logger.info("Add alternate event to queue")
            self.event_queue.append("alternate")

    def stop(self):
        self._running = False
