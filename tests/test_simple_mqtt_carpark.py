import unittest
from smartpark.simple_mqtt_carpark import CarPark

class TestCarPark(unittest.TestCase):
    """Unit tests for CarPark class."""
    def setUp(self):
        """Create a CarPark in testing mode."""
        self.carpark = CarPark('../config/tiny_carpark.toml', test_mode=True)

    def test_cars_entering(self):
        """
        Test that total_cars and available_spaces update correctly when cars
        enter the car park.
        """
        self.carpark.on_car_entry()
        self.carpark.on_car_entry()
        self.assertEqual(2, self.carpark.total_cars)
        self.assertEqual(0, self.carpark.available_spaces)

    def test_cars_exiting(self):
        """
        Test that total_cars and available_spaces update correctly when cars
        exit the car park.
        """
        self.carpark.on_car_entry()
        self.carpark.on_car_entry()
        self.carpark.on_car_entry()
        self.carpark.on_car_exit()
        self.carpark.on_car_exit()
        self.assertEqual(1, self.carpark.total_cars)
        self.assertEqual(1, self.carpark.available_spaces)

    def test_available_spaces_calculated_correctly(self):
        """
        Test that car park available spaces are calculated correctly under
        normal circumstances.
        """
        self.carpark.on_car_entry()
        self.assertEqual(1, self.carpark.available_spaces)

    def test_available_spaces_not_negative(self):
        """Available parking spaces are never negative."""
        self.carpark.on_car_entry()
        self.carpark.on_car_exit()
        self.carpark.on_car_exit()
        self.assertEqual(self.carpark.total_spaces,
                         self.carpark.available_spaces)

    def test_temperature_can_be_set(self):
        """
        The car park temperature can be set to an integer and read back
        successfully.
        """
        self.carpark.temperature = 25
        self.assertEqual(25, self.carpark.temperature)

    def test_temperature_can_be_unknown(self):
        """
        The car park temperature can be set to None and is read back as
        'unknown'.
        """
        self.carpark.temperature = None
        self.assertEqual('unknown', self.carpark.temperature)

    def test_invalid_temperature_raises_exception(self):
        """
        Setting the car park temperature to something other than an int or
        None raises a ValueError.
        """
        with (self.assertRaises(ValueError)):
            self.carpark.temperature = '25'
        with (self.assertRaises(ValueError)):
            self.carpark.temperature = 25.025