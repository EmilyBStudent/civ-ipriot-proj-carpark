import unittest
from smartpark.car_detector import CarDetector

class TestCarDetector(unittest.TestCase):
    """Unit tests for CarDetector class."""
    def setUp(self):
        """Create a CarDetector in testing mode."""
        self.car_detector = CarDetector('../config/tiny_carpark.toml',
                                   test_mode=True)

    def test_temperature_remains_between_maximum_and_minimum(self):
        """
        The temperature never falls below or exceeds the given maximum/
        minimum.
        """
        self.car_detector.temperature = 40
        self.assertEqual(self.car_detector.MAX_TEMPERATURE,
                         self.car_detector.temperature)
        self.car_detector.temperature = -10
        self.assertEqual(self.car_detector.MIN_TEMPERATURE,
                         self.car_detector.temperature)

    def test_invalid_temperature_raises_exception(self):
        """
        Setting the car park temperature to something other than an int raises
        a ValueError.
        """
        with (self.assertRaises(ValueError)):
            self.car_detector.temperature = '25'
        with (self.assertRaises(ValueError)):
            self.car_detector.temperature = 25.025