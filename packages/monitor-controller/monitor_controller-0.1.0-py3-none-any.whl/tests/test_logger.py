import unittest
from monitor_controller.logger import setup_logger

class TestLogger(unittest.TestCase):
    def test_setup_logger(self):
        logger = setup_logger()
        self.assertIsNotNone(logger)

if __name__ == "__main__":
    unittest.main()