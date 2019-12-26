#!/usr/bin/env python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
pointList=[12,13,15,16,7,18,22,29,31,11,36,37,38,40]
GPIO.setup(pointList, GPIO.OUT)


GPIO.cleanup()
print ("GPIO ClEAN")