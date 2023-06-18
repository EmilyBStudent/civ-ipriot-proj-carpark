"""
Provides a simple window with buttons to simulate sensor data from the car
park. Simulates cars entering and exiting the car park and the local
temperature being monitored, and publishes this data to MQTT.
"""
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
    MIN_TEMPERATURE = 10
    MAX_TEMPERATURE = 35

    def __init__(self, config_file: str, test_mode: bool=False):
        """
        Create an MQTT publisher to provide updates and a Car Detector window
        to simulate cars entering and exiting the car park.

        :param config_file: string containing relative path and filename of
            the configuration file for the car park
        :param test_mode: bool representing whether the class is running in
            unit test mode (in which case we avoid running any blocking loops)
        """
        config = parse_config(config_file)
        self.mqtt_device = mqtt_device.MqttDevice(config)

        self._temperature = random.randint(self.MIN_TEMPERATURE,
                                           self.MAX_TEMPERATURE)

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

        if not test_mode:
            self.root.mainloop()

    def _publish_event(self, action: str):
        """
        Publish an event via MQTT when a car enters or exits the car park.

        :param action: string naming the kind of event to be published: either
            'entry' or 'exit'
        """
        readable_time = datetime.now().strftime('%H:%M')
        self.update_temperature()
        print(
            (
                f"ACTION: {action}, "
                f"TIME: {readable_time}, "
                + f"TEMPC: {self.temperature}"
            )
        )
        message = (
                f"ACTION: {action}, "
                f"TIME: {readable_time}, "
                + f"TEMPC: {self.temperature}"
        )
        self.mqtt_device.client.publish('sensor', message)

    @property
    def temperature(self):
        """Returns the current temperature."""
        return self._temperature

    @temperature.setter
    def temperature(self, value: int):
        """
        Sets the current temperature, remaining within the maximum and minimum
        temperature range.

        :param value: integer, new temperature to record
        :raises ValueError: if value passed in is not an integer
        """
        if type(value) != int:
            raise ValueError('Temperature must be an integer')

        self._temperature = value
        self._temperature = max(self.temperature, self.MIN_TEMPERATURE)
        self._temperature = min(self.temperature, self.MAX_TEMPERATURE)

    def update_temperature(self):
        """Updates the temperature within a range of +/- 2 degrees."""
        change = random.randint(-2, 2)
        self.temperature = self.temperature + change

    def incoming_car(self):
        """Publish an event advising that a car has entered the car park."""
        self._publish_event('entry')

    def outgoing_car(self):
        """Publish an event advising that a car has exited the car park."""
        self._publish_event('exit')


if __name__ == '__main__':
    CarDetector('../config/city_square_parking.toml')