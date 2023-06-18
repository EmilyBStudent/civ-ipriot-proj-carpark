"""Simplify creation of MQTT clients from configuration file data."""
import paho.mqtt.client as paho
class MqttDevice:
    """
    Helper class to simplify creation of MQTT clients from configuration file
    data.
    """
    def __init__(self, config):
        """
        Initialise with information from the configuration data provided and
        create a paho client to use.

        :param config: dictionary of configuration data including paho settings
        """
        self.name = config['name']
        self.location = config['location']

        # Define topic components:
        self.topic_root = config['topic-root']
        self.topic_qualifier = config['topic-qualifier']
        self.topic = self._create_topic_string()

        # Configure broker
        self.broker = config['broker']
        self.port = config['port']

        # initialise a paho client and bind it to the object (has-a)
        self.client = paho.Client()
        self.client.connect(self.broker,
                            self.port)

    def _create_topic_string(self):
        """
        Generate the MQTT topic string using the saved configuration data.

        :returns: string formatted as an MQTT topic
        """
        return (f"{self.topic_root}/{self.location}/" +
                f"{self.name}/{self.topic_qualifier}")