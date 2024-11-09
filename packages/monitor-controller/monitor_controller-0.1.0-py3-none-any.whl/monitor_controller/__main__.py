import time
import threading

from monitor_controller.logger import setup_logger
from monitor_controller.devicelistener import DeviceListener
from monitor_controller.eventcontroller import EventController
from monitor_controller.config import ConfigGenerator

def main():
    logger = setup_logger()
    logger.info("Program starting...")

    config = ConfigGenerator().execute()

    event_queue = []

    print("The program will now start listening for events.")

    thread1 = threading.Thread(target=execute, args=(logger, config, event_queue))
    thread1.daemon = True 
    thread1.start()

    try:
        input("Press enter to exit program ...")
    except KeyboardInterrupt:
        pass

def execute(logger, config, event_queue):
    while True:
        listener = DeviceListener(config["trigger_device"], event_queue)
        listener.listen()

        controller = EventController(event_queue, config["settings"])
        controller.handle_event()

        logger.info("4 second time out to prevent too early signal detection.")
        time.sleep(4)
        logger.info("Program is done sleeping, starting from the top...")

if __name__ == "__main__":
    main()