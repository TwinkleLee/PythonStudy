import RPi.GPIO as GPIO
import time

BtnPin = 33


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(BtnPin, GPIO.IN)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("setup", GPIO.input(BtnPin))
    # GPIO.add_event_detect(BtnPin,GPIO.BOTH,callback=detectChange,bouncetime=1000)
    GPIO.add_event_detect(BtnPin, GPIO.RISING,
                          callback=detectChange, bouncetime=20)


def detectChange(chn):
    print("detectChange", GPIO.input(BtnPin))


def loop():
    while True:
        pass


def destroy():
    print("KeyboardInterrupt")
    GPIO.cleanup()


setup()
try:
    loop()
except KeyboardInterrupt:
    destroy()
