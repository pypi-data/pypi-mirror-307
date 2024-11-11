from dataclasses import dataclass
from monitorcontrol import InputSource

@dataclass
class MonitorSettings:
    name: str
    channel: InputSource   

@dataclass
class EventQueue:
    queue: list

class Channel:
    channels = { 
        "HDMI1": InputSource.HDMI1,
        "HDMI2": InputSource.HDMI2,
        "DP1": InputSource.DP1,
        "DP2": InputSource.DP2,
    }

    inputsource_channels = { 
        InputSource.HDMI1: "HDMI1",
        InputSource.HDMI2: "HDMI2",
        InputSource.DP1: "DP1",
        InputSource.DP2: "DP2"
    }

@dataclass
class Monitor:
    name: str
    channel: InputSource

@dataclass
class Setup:
    name: str
    monitors: dict

@dataclass
class TriggerDevices:
    devices: list

class Settings:
    settings = dict

    @staticmethod
    def put(name, setup):
        Settings.settings[name] = setup