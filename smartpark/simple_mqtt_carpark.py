from datetime import datetime

import mqtt_device
from config_parser import parse_config
from paho.mqtt.client import MQTTMessage


class CarPark:
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config_file: str, test_mode: bool=False):
        config = parse_config(config_file)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self._temperature = None

        self.mqtt_device = mqtt_device.MqttDevice(config)
        self.mqtt_device.client.on_message = self.on_message
        self.mqtt_device.client.subscribe('sensor')
        if not test_mode:
           self.mqtt_device.client.loop_forever()

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        
    def _publish_event(self):
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
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        if self.total_cars > 0:
            self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        # TODO: Extract temperature from payload
        # self.temperature = ... # Extracted value
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    car_park = CarPark('../config/city_square_parking.toml', test_mode=True)
    print("Carpark initialized")