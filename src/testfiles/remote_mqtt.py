#!/usr/bin/env python

import usb.core
import usb.util
import paho.mqtt.client as mqtt
import time

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

BTN_LEFT  = 79
BTN_RIGHT = 80
BTN_DOWN  = 81
BTN_UP    = 82
BTN_STOP  = 40 # Center Button
BTN_EXIT  = 41 # Back Button

USB_VENDOR  = 0x1915 # Andoer
USB_PRODUCT = 0x1047 # Universal Remote

BUTTON_COUNT = 0

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/button")
  
def publishMessage(payload):
    global BUTTON_COUNT
    
    mqttClient.publish("rpi/led", payload=payload)
    
    BUTTON_COUNT+=1
    mqttClient.publish("rpi/button", payload=BUTTON_COUNT)
		

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

clientName = "RPI Button"
serverAddress = "hoverrunrpi"

mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus

mqttClient.connect(serverAddress)

while True:
    control = None

    try:
      control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
      print control
    except:
      pass
      
    if control != None:
      if BTN_DOWN in control:
          print("Down Button Pressed")
          publishMessage("red/off")

      if BTN_UP in control:
          print("UP Button Pressed")
          publishMessage("red/on")

      if BTN_LEFT in control:
          print("Left Button Pressed")
          publishMessage("green/on")

      if BTN_RIGHT in control:
          print("Right Button Pressed")
          publishMessage("green/off")

      if BTN_STOP in control:
          print("Stop Button Pressed")

      if BTN_EXIT in control:
          print("Exit Button Pressed")
          exit()

    time.sleep(0.5) # Let CTRL+C actually exit
