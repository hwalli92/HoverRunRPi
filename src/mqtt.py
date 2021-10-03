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

        self.pid_settings = {"kp": 0.0, "ki": 0.0, "kd": 0.0}

    def connection_config(self, client, userdata, flags, rc):
        self.mqttClient.subscribe("hvrrun/speedup")
        self.mqttClient.subscribe("hvrrun/speeddown")
        self.mqttClient.subscribe("hvrrun/pidsettings")

    def message_decoder(self, client, userdata, msg):
        print("New msg on topic: {}".format(msg.topic))
        
        if msg.topic == "hvrrun/speedup":
            self.serial.write("speed up")
            self.send_ack(1)
        elif msg.topic == "hvrrun/speeddown":
            self.serial.write("speed down")
            self.send_ack(1)
        elif msg.topic == "hvrrun/pidsettings":
            message = str(msg.payload.decode("UTF-8", "ignore"))
            self.pid_settings = json.loads(message)
            self.send_pid_params()
            self.send_ack(1)
        else:
            self.send_ack(0)

    def send_ack(self, ack):
        self.mqttClient.publish("hvrrun/ack", payload=ack)

    def send_pid_params(self):
        msg = "pid %f %f %f " % (
            self.pid_settings["kp"],
            self.pid_settings["ki"],
            self.pid_settings["kd"],
        )
        self.serial.write(msg)

    def disconnect(self):
        self.mqttClient.loop_stop()
