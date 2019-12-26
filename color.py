import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
pointList = (36, 37, 38, 40)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pointList, GPIO.OUT)


def changeColor(lowNum):  # 36~38
    GPIO.output(list(filter(lambda item: item != lowNum, pointList)), GPIO.HIGH)
    GPIO.output(lowNum, GPIO.LOW)


nowNum = 36
while True:
    if(nowNum == 38):
        nowNum = 36
    else:
        nowNum = nowNum+1
    changeColor(nowNum)
    time.sleep(0.5)
