"""
Display car park availability and temperature data for use of drivers in
Moondalup.
"""
import threading
import tkinter as tk
from typing import Iterable

from paho.mqtt.client import MQTTMessage

from config_parser import parse_config
import mqtt_device


class WindowedDisplay:
    """
    Displays values for a given set of fields as a simple GUI window. Use
    .show() to display the window; use .update() to update the values
    displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """
        Creates a Windowed (tkinter) display to replace sense_hat display. To
        show the display (blocking) call .show() on the returned object.

        :param title: String containing the title of the window (usually the
            name of your car park from the config)
        :param display_fields: An Iterable (usually a list) of field names for
            the UI. Updates to values must be presented in a dictionary with
            these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """
        Update the values displayed in the GUI.

        :param updated_values: a dictionary with keys matching the field names
            passed to the constructor.
        """
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()


class CarParkDisplay:
    """
    Provides a simple display of the car park status. The class is designed to
    be customizable without requiring and understanding of tkinter or
    threading.
    """
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self, config_file: str):
        """
        Start an MQTT client to subscribe to car park updates, and create a
        window to display the updates received.

        :param config_file: string containing relative path and filename of
            the car park configuration to use in setting up the MQTT client
        """
        config = parse_config(config_file)
        self.carpark_name = config['name']
        self.mqtt_device = mqtt_device.MqttDevice(config)
        self.mqtt_device.client.subscribe('carpark')
        self.mqtt_device.client.on_message = self.on_message

        self.window = WindowedDisplay(
            self.carpark_name, CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        """Check for updates from the MQTT subscription."""
        self.mqtt_device.client.loop_forever()

    def on_message(self, client, userdata, msg: MQTTMessage):
        """
        On receiving a car park update through MQTT, display the new
        information in the window.

        :param client: The MQTT client which received the message.
        :param userdata: userdata passed with the MQTT message
        :param msg: the message received, in MQTTMessage format
        """
        payload = msg.payload.decode()

        # Rather than assume the data will always be received ordered the same
        # way, we save the keys with the data so we can access exactly the
        # information we want.
        fields = payload.split(',')
        received = dict()
        for field in fields:
            label, data = field.split(':', 1)
            received[label.strip()] = data.strip()

        # NOTE: Dictionary keys *must* be the same as the class fields
        field_values = dict()
        if received['SPACES'] == '0':
            field_values['Available bays'] = 'FULL'
        else:
            field_values['Available bays'] = received['SPACES']
        field_values['Temperature'] = received['TEMPC']
        field_values['At'] = received['TIME']

        self.window.update(field_values)


if __name__ == '__main__':
    CarParkDisplay('../config/city_square_parking.toml')