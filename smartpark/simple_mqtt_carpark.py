from datetime import datetime

import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


class CarPark:
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self._temperature = None

        self.mqtt_device = mqtt_device.MqttDevice(config)
        self.mqtt_device.client.on_message = self.on_message
        self.mqtt_device.client.subscribe('sensor')
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
    config = {'name': "raf-park",
              'total-spaces': 130,
              'total-cars': 0,
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'entry',
              'is_stuff': False
              }
    # TODO: Read config from file
    car_park = CarPark(config)
    print("Carpark initialized")