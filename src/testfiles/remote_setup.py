#!/usr/bin/env python

import usb.core
import usb.util
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

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

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

      if BTN_UP in control:
          print("UP Button Pressed")

      if BTN_LEFT in control:
          print("Left Button Pressed")

      if BTN_RIGHT in control:
          print("Right Button Pressed")

      if BTN_STOP in control:
          print("Stop Button Pressed")

      if BTN_EXIT in control:
          print("Exit Button Pressed")
          exit()

    time.sleep(0.5) # Let CTRL+C actually exit
