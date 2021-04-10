#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time

BUTTON_COUNT=0

def gpioSetup():
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	gpio.setup(22, gpio.IN, pull_up_down=gpio.PUD_DOWN)

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/button")
	
def buttonCallback(channel):
	global BUTTON_COUNT
	
	print("Button was pushed!")
	
	if BUTTON_COUNT % 2 == 0:
		mqttClient.publish("rpi/led", payload="red/on")
		time.sleep(2)
		mqttClient.publish("rpi/led", payload="red/off")
	else:
		mqttClient.publish("rpi/led", payload="green/on")
		time.sleep(2)
		mqttClient.publish("rpi/led", payload="green/off")
	
	BUTTON_COUNT+=1
	mqttClient.publish("rpi/button", payload=BUTTON_COUNT)
		

gpioSetup()
	
clientName = "RPI Button"
serverAddress = "hoverrunrpi"

mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus

mqttClient.connect(serverAddress)

gpio.add_event_detect(22, gpio.RISING, callback=buttonCallback)

mqttClient.loop_forever()
