import unittest
from unittest.mock import patch
from monitor_controller.eventcontroller import EventController

class TestEventController(unittest.TestCase):
    def setUp(self):
        self.event_queue = ["pc"]
        self.settings = {
            "pc": {"Monitor1": "HDMI1"},
            "laptop": {"Monitor1": "DP1"}
        }
        self.controller = EventController(self.event_queue, self.settings)

    @patch('monitor_controller.eventcontroller.get_monitors')
    def test_handle_event(self, mock_get_monitors):
        mock_get_monitors.return_value = [
            {"model": "Monitor1", "input_source": "HDMI1"}
        ]
        self.controller.handle_event()
        self.assertEqual(self.event_queue, [])

if __name__ == "__main__":
    unittest.main()