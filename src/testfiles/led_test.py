#!/usr/bin/env python


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

while True:
	print "LED on"
	GPIO.output(17,GPIO.HIGH)
	time.sleep(1)
	print "LED off"
	GPIO.output(17,GPIO.LOW)
	time.sleep(2)
