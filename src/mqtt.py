import json
import paho.mqtt.client as mqtt


class MQTTServer:
    def __init__(self, serial):
        clientName = "RPI Button"
        serverAddress = "hoverrunrpi"

        self.mqttClient = mqtt.Client(clientName)

        self.mqttClient.on_connect = self.connection_config
        self.mqttClient.on_message = self.message_decoder

        self.mqttClient.connect(serverAddress)
        self.mqttClient.loop_start()

        self.serial = serial

        self.trainingDetails = {
            "Type": "Manual",
            "Level": 1.0,
            "Limit": None,
            "Status": False,
        }

        self.pid_settings = {"Kp": 10, "Ki": 0.0, "Kd": 0}

    def connection_config(self, client, userdata, flags, rc):
        self.mqttClient.subscribe("hvrrun/training")
        self.mqttClient.subscribe("hvrrun/pidsettings")

    def message_decoder(self, client, userdata, msg):
        message = str(msg.payload.decode("UTF-8", "ignore"))

        if msg.topic == "hvrrun/training":
            self.trainingDetails = json.loads(message)
            self.send_ack(1)
        elif msg.topic == "hvrrun/pidsettings":
            self.pid_settings = json.loads(message)
            self.send_pid_params()
            self.send_ack(1)
        else:
            self.send_ack(0)

    def send_ack(self, ack):
        self.mqttClient.publish("hvrrun/ack", payload=ack)

    def send_pid_params(self):
        msg = "pid %d %.2f %d " % (
            self.pid_settings["Kp"],
            self.pid_settings["Ki"],
            self.pid_settings["Kd"],
        )
        self.serial.write(msg)

    def disconnect(self):
        self.mqttClient.loop_stop()
