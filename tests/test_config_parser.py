import unittest
from smartpark.config_parser import parse_config

class TestConfigParsing(unittest.TestCase):
    def setUp(self):
        self.config_file = '../config/city_square_parking.toml'
    def test_config_parser_has_correct_name_and_spaces(self):
        config = parse_config(self.config_file)
        self.assertEqual(config['name'], "Moondalup City Square Parking")
        self.assertEqual(config['total-spaces'], 192)

    def test_config_parser_raises_error_if_file_not_found(self):
        config = parse_config(self.config_file)
        self.assertRaises(SystemExit, parse_config, 'zzzzz.toml')