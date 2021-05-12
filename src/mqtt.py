import paho.mqtt.client as mqtt


class MQTTServer():
	
	def __init__(self):
		clientName = "RPI Button"
		serverAddress = "hoverrunrpi"

		self.mqttClient = mqtt.Client(clientName)

		self.mqttClient.on_connect = self.connection_config
		self.mqttClient.on_message = self.message_decoder

		self.mqttClient.connect(serverAddress)
		
	def connection_config(self, client, userdata, flags, rc):
		self.mqttClient.subscribe("rpi/motorctrl")
		
	def message_decoder(self, client, userdata, msg):
		self.message = msg.payload.decode(encoding='UTF-8')
		
	def publish_message(self, payload):
		self.mqttClient.publish("rpi/led", payload=payload[0])
    
		self.mqttClient.publish("rpi/motorctrl", payload=payload[1])
		
