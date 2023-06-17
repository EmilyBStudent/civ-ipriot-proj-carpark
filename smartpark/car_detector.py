import tkinter as tk
from datetime import datetime
import random

import mqtt_device
from config_parser import parse_config

class CarDetector:
    """
    Provides a couple of simple buttons that can be used to represent a sensor
    detecting a car.
    """

    def __init__(self, config_file, test_mode=False):
        """
        Create an MQTT publisher to provide updates and a Car Detector window
        to simulate cars entering and exiting the carpark.
        """
        config = parse_config(config_file)
        config['topic-qualifier'] = 'sensor'    # TODO: clean up qualifiers
        self.mqtt_device = mqtt_device.MqttDevice(config)

        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50),
            cursor='right_side', command=self.incoming_car
        )
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50),
            cursor='bottom_left_corner', command=self.outgoing_car
        )
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def _publish_event(self, action: str):
        """
        Publish an event via MQTT when a car enters or exits the carpark.
        """
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                f"ACTION: {action}"
                f"TIME: {readable_time}, "
                + "TEMPC: 42"
            )
        )
        message = (
                f"ACTION: {action}"
                f"TIME: {readable_time}, "
                + "TEMPC: 42"
        )
        self.mqtt_device.client.publish('sensor', message)

    def incoming_car(self):
        """Publish an event advising that a car has entered the carpark."""
        self._publish_event('entry')

    def outgoing_car(self):
        """Publish an event advising that a car has exited the carpark."""
        self._publish_event('exit')


if __name__ == '__main__':
    CarDetector('../config/city_square_parking.toml')