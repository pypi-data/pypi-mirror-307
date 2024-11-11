import unittest
from unittest.mock import patch, MagicMock
from monitorcontrol import InputSource
from monitor_controller.config import ConfigGenerator

class TestConfigGenerator(unittest.TestCase):
    def setUp(self):
        self.config_generator = ConfigGenerator()

    @patch('monitor_controller.config.DeviceListener.scan')
    @patch('monitor_controller.config.inquirer.prompt')
    def test_determine_trigger_device(self, mock_prompt, mock_scan):
        mock_scan.return_value = ["Device1", "Device2"]
        mock_prompt.return_value = {'trigger_device': 'Device1'}
        
        selected_device = self.config_generator.determine_trigger_device()
        
        self.assertEqual(selected_device, 'Device1')
        mock_prompt.assert_called_once()
        mock_scan.assert_called_once()

    @patch('monitor_controller.config.DeviceListener.get_monitors')
    @patch('monitor_controller.config.print')
    def test_determine_active_monitor_settings(self, mock_print, mock_get_monitors):
        mock_monitor = MagicMock()
        mock_monitor.get_vcp_capabilities.return_value = {"model": "Monitor1"}
        mock_monitor.get_input_source.return_value = InputSource.HDMI1
        mock_get_monitors.return_value = [mock_monitor]
        
        monitor_settings = self.config_generator.determine_active_monitor_settings()
        print(monitor_settings)
        
        self.assertIn("Monitor1", monitor_settings["main"])
        self.assertEqual(monitor_settings["main"]["Monitor1"], "HDMI1")
        mock_get_monitors.assert_called_once()
        mock_print.assert_called()

    @patch('monitor_controller.config.inquirer.prompt')
    @patch('monitor_controller.config.print')
    def test_alternate_monitor_settings(self, mock_print, mock_prompt):
        mock_prompt.side_effect = [
            {"channel": "DP1"},
            {"channel": "HDMI2"}
        ]
        
        monitor_config = {
            "main": {
                "Monitor1": "HDMI1",
                "Monitor2": "DP2"
            }
        }
        
        updated_config = self.config_generator.alternate_monitor_settings(monitor_config)
        
        self.assertIn("alternate", updated_config)
        self.assertEqual(updated_config["alternate"]["Monitor1"], "DP1")
        self.assertEqual(updated_config["alternate"]["Monitor2"], "HDMI2")
        mock_prompt.assert_called()
        mock_print.assert_called()

if __name__ == "__main__":
    unittest.main()