from datetime import datetime

import mqtt_device
from config_parser import parse_config
from paho.mqtt.client import MQTTMessage


class CarPark:
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config_file: str, test_mode: bool=False):
        """
        Initialise the carpark with data from the given config file.
        Create a new MQTT device to listen for updates from the carpark
        sensor and publish updates to the display.
        """
        config = parse_config(config_file)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self._temperature = None

        self.mqtt_device = mqtt_device.MqttDevice(config)
        self.mqtt_device.client.on_message = self.on_message
        self.mqtt_device.client.subscribe('sensor')
        self._publish_event()
        if not test_mode:
           self.mqtt_device.client.loop_forever()

    @property
    def available_spaces(self):
        """
        Calculate available parking spaces based on total spaces and current
        number of cars in the carpark.
        """
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        
    def _publish_event(self):
        """ Publish the current carpark statistics to the MQTT device. """
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                f"TIME: {readable_time}, "
                + f"SPACES: {self.available_spaces}, "
                + "TEMPC: 42"
            )
        )
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + "TEMPC: 42"
        )
        self.mqtt_device.client.publish('display', message)

    def on_car_entry(self):
        """Handle a car entering the carpark."""
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        """Handle a car exiting the carpark."""
        if self.total_cars > 0:
            self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        """Handle messages received from the sensor."""
        payload = msg.payload.decode()
        # TODO: Extract temperature from payload
        # self.temperature = ... # Extracted value
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    car_park = CarPark('../config/city_square_parking.toml')
    print("Carpark initialized")