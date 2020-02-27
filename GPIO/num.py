import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

hz = 250
positiveDict = {
    "ones": 5,
    "tens": 10
}

# key:led point num value:GPIO
pointDict = {
    1: 12,
    2: 13,
    3: 15,
    4: 16,
    5: 7,
    6: 18,
    7: 22,
    8: 29,
    9: 31,
    10: 11
}
pointTuple = tuple(map(lambda item: pointDict[item], pointDict))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pointTuple, GPIO.OUT)

# key:num value:led point num
transferDict = {
    0: (7, 6, 4, 1, 3, 8),
    1: (6, 4),
    2: (7, 6, 1, 3, 9),
    3: (7, 6, 4, 1, 9),
    4: (6, 4, 8, 9),
    5: (7, 4, 1, 8, 9),
    6: (7, 4, 1, 3, 8, 9),
    7: (7, 6, 4),
    8: (7, 6, 4, 1, 3, 8, 9),
    9: (7, 6, 4, 1, 8, 9)
}


def closeAll():
    GPIO.output(pointTuple, GPIO.LOW)
    GPIO.output(pointDict[positiveDict["ones"]], GPIO.HIGH)
    GPIO.output(pointDict[positiveDict["tens"]], GPIO.HIGH)


def showNum(targetNum):
    showSingleNum(targetNum, "ones")
    showSingleNum(targetNum, "tens")


def showSingleNum(targetNum, positive):
    closeAll()
    if(positive == "tens"):
        num = targetNum//10
    elif (positive == "ones"):
        num = targetNum % 10

    GPIO.output(pointDict[positiveDict[positive]], GPIO.LOW)
    for item in transferDict[num]:
        GPIO.output(pointDict[item], GPIO.HIGH)
    time.sleep(1/hz/2)


while True:
    for item in range(100):
        for times in range(hz):
            showNum(item)

# while True:
#    showNum(32)
