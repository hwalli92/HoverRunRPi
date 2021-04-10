#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

def gpioSetup():
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	gpio.setup(17, gpio.OUT)
	gpio.setup(27, gpio.OUT)
	gpio.setup(22, gpio.IN, pull_up_down=gpio.PUD_DOWN)

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/led")
	

def messageDecoder(client, userdata, msg):
	message = msg.payload.decode(encoding='UTF-8')
	
	if message == "red/on":
		gpio.output(17, gpio.HIGH)
		print("Red LED is ON!")
	elif message == "red/off":
		gpio.output(17, gpio.LOW)
		print("Red LED is OFF!")
	elif message == "green/on":
		gpio.output(27, gpio.HIGH)
		print("Green LED is ON!")
	elif message == "green/off":
		gpio.output(27, gpio.LOW)
		print("Green LED is OFF!")
	else:
		print("Unknown message!")

gpioSetup()
	
clientName = "RPI LED"
serverAddress = "hoverrunrpi"

mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

mqttClient.connect(serverAddress)

mqttClient.loop_forever()
