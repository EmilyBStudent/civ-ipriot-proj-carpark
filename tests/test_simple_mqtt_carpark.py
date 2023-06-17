import unittest
from smartpark.simple_mqtt_carpark import CarPark

class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.carpark = CarPark('../config/tiny_carpark.toml', test_mode=True)

    def test_cars_entering(self):
        self.carpark.on_car_entry()
        self.carpark.on_car_entry()
        self.assertEqual(2, self.carpark.total_cars)

    def test_cars_exiting(self):
        self.carpark.on_car_entry()
        self.carpark.on_car_entry()
        self.carpark.on_car_entry()
        self.carpark.on_car_exit()
        self.carpark.on_car_exit()
        self.assertEqual(1, self.carpark.total_cars)

    def test_available_spaces(self):
        self.carpark.on_car_entry()
        self.assertEqual(1, self.carpark.available_spaces)

    def test_available_spaces_not_negative(self):
        self.carpark.on_car_entry()
        self.carpark.on_car_exit()
        self.carpark.on_car_exit()
        self.assertEqual(self.carpark.total_spaces,
                         self.carpark.available_spaces)