import unittest
from unittest.mock import patch, MagicMock
from monitor_controller.devicelistener import DeviceListener

class TestDeviceListener(unittest.TestCase):
    @patch('monitor_controller.devicelistener.hid.enumerate')
    def test_scan(self, mock_enumerate):
        mock_enumerate.return_value = [
            {"product_string": "Device1"},
            {"product_string": "Device2"}
        ]
        mock_logger = MagicMock()
        devices = DeviceListener.scan(mock_logger)
        self.assertIn("Device1", devices)
        self.assertIn("Device2", devices)

    @patch('monitor_controller.devicelistener.hid.enumerate')
    def test_listen(self, mock_enumerate):
        mock_enumerate.return_value = [
            {"product_string": "Device1"},
            {"product_string": "Device2"}
        ]
        event_queue = []
        listener = DeviceListener("Device1", event_queue)
        listener.listen()
        self.assertIn("main", listener.event_queue)

if __name__ == "__main__":
    unittest.main()