import json
import logging
import os
import inquirer

from monitor_controller.dataclass import Channel
from monitor_controller.devicelistener import DeviceListener


class ConfigGenerator:
    def __init__(self):
        self.logger = logging.getLogger()

    def generate(self):
        return self.config
    
    def execute(self):
        if not os.path.exists("config.json"):
            print("config.json not found, starting the config generator..")
            self.logger.info("config.json not found, starting the config generator.")
            self.generate_config()
        else:
            self.logger.info("config.json found, skipping the config generator.")

        with open("config.json") as config_file:
            self.config = json.loads(config_file.read())

        return self.config
    
    def generate_config(self):
        selected_device = self.determine_trigger_device()
        monitor_config = self.determine_active_monitor_settings()
        monitor_config = self.alternate_monitor_settings(monitor_config)
        config = {
            "trigger_device": selected_device,
            "settings": monitor_config
        }

        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        self.logger.info("config.json has been generated and saved.")

    def determine_trigger_device(self):
        self.logger.info("Scanning for connected devices...")
        hids = DeviceListener.scan(self.logger)

        # Create the prompt
        question = [
            inquirer.List(
                "trigger_device",
                message="Choose a trigger device",
                choices=hids
            )
        ]

        # Prompt the user and get the answer
        answer = inquirer.prompt(question)
        selected_device = answer['trigger_device']
        print(f"You selected: {selected_device}")

        return selected_device
    
    def determine_active_monitor_settings(self):
        main_settings = {}

        print("Scanning for connected monitors...\n")
        for monitor in DeviceListener.get_monitors():
            with monitor:
                monitor_info = monitor.get_vcp_capabilities()
                monitor_name = monitor_info["model"]
                current_channel = monitor.get_input_source()
                print(f"Found the following monitor: {monitor_name}")
                print(f"Currently on input source: {current_channel}")

            main_settings[monitor_name] = Channel.inputsource_channels[current_channel]

        # Create the final JSON object
        monitor_config = {
            "main": main_settings
        }

        return monitor_config
    
    def alternate_monitor_settings(self, monitor_config):
        monitor_config["alternate"] = {}
        print("\nNow we will determine the alternate monitor settings with your help..")
        for monitor_name in monitor_config["main"]:
            question = [
                inquirer.List(
                    "channel",
                    message=f"Choose the alternate input source for {monitor_name}",
                    choices=list(Channel.channels.keys())
                )
            ]

            answer = inquirer.prompt(question)
            monitor_config["alternate"][monitor_name] = answer["channel"]

        print("Your monitor settings are now complete.")
        print(json.dumps(monitor_config, indent=4))

        return monitor_config