import logging
from monitorcontrol import get_monitors, VCPError

from monitor_controller.dataclass import Channel

class EventController:
    
    def __init__(self, event_queue: list, settings: dict) -> None:
        self.event_queue = event_queue
        self.settings = settings
        self.logger = logging.getLogger()

    def handle_event(self):
        current_event = self.event_queue.pop(0)
        self.required_settings = self.settings[current_event]

        self.logger.info("Checking out the current monitor settings...")
        for monitor in get_monitors():
            iteration = 0
            monitor_name = self.settings.keys()[iteration]
            with monitor:
                try:
                    self.current_channel = monitor.get_input_source()
                    required_channel = self.required_settings[monitor_name]

                    if self.is_wrong_channel(monitor_name):
                        self.logger.info("Current input channel for monitor {} is not active.".format(monitor_name))
                        self.logger.info("We need to switch input channel, adding action to queue..")
                        self.logger.info("Triggering action to change input channel, switching to {} for {}".format(self.determine_required_input_source(required_channel), monitor_name))
                        monitor.set_input_source(self.determine_required_input_source(required_channel))
                    else:
                        self.logger.info("Current input channel for monitor {} is active, no switching required.".format(monitor_name))
                        continue

                except VCPError:
                    self.logger.warning("Obtaining monitor information has gone wrong")

    def is_wrong_channel(self, monitor_name) -> bool:
        return self.determine_required_input_source(self.required_settings[monitor_name]) != self.current_channel

    def determine_required_input_source(self, required_channel: str):
            return Channel.channels[required_channel]
    