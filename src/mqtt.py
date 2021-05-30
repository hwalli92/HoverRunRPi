import json
import paho.mqtt.client as mqtt

class MQTTServer:
    def __init__(self):
        clientName = "RPI Button"
        serverAddress = "hoverrunrpi"

        self.mqttClient = mqtt.Client(clientName)

        self.mqttClient.on_connect = self.connection_config
        self.mqttClient.on_message = self.message_decoder

        self.mqttClient.connect(serverAddress)

        self.trainingDetails = {"Type": "Manual", "Level": 1.0, "Limit": None, "Status": False}
    
	def connection_config(self, client, userdata, flags, rc):
		self.mqttClient.subscribe("hvrrun/training")
        self.mqttClient.subscribe("hvrrun/status")

    def message_decoder(self, client, userdata, msg):
        message = str(msg.payload.decode("UTF-8", "ignore"))

        self.trainingDetails = json.loads(message)

        self.send_ack()

    def send_ack(self):
        self.mqttClient.publish("hvrrun/ack", payload=1)
