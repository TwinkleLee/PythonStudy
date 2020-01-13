'''
进入页面先亮蓝色(空闲)，显示0
轮询并显示订单数，大于0则亮绿灯(就绪)
绿灯(就绪)状态下点击开关变为红色(工作中)，通过接口获取待打印订单的gcode并下载到本地，开始打印
打印结束后通过文件名获得orderId并告知后端打印完成
'''
import RPi.GPIO as GPIO
import requests
import threading
import time
import datetime
import logging

app = None

colorDict = {
    'Red': 36,
    'Blue': 37,
    'Green': 38,
    'Anode': 40
}
colorTuple = tuple(map(lambda item: colorDict[item], colorDict))

hz = 100
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
    # 5: 7,#3代
    5: 32,#4代
    6: 18,
    7: 22,
    8: 29,
    9: 31,
    10: 11
}
pointTuple = tuple(map(lambda item: pointDict[item], pointDict))
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
BtnPin = 33
orderCount = 0
nowOrderId = None

fh = logging.FileHandler(encoding='utf-8', mode='a', filename='logger.log')
sh = logging.StreamHandler()
logging.basicConfig(handlers=[
    sh, fh], format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.DEBUG)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


def initColor():
    GPIO.setup(colorTuple, GPIO.OUT)
    changeColor('Blue')


def changeColor(color):
    if color:
        GPIO.output(
            list(filter(lambda item: item != colorDict[color], colorTuple)), GPIO.HIGH)
        GPIO.output(colorDict[color], GPIO.LOW)
    else:
        GPIO.output(colorTuple, GPIO.HIGH)


def polling():
    res = requests.get(
        r'https://o.api.troncell.com/api/services/app/OrderExtension/GetPrintOrderCount', headers={"tenantId": "5056",'type':'4'})
    try:
        res.raise_for_status()
    except BaseException as e:
        logging.error(e)
        if res.status_code == 500:
            logging.error(res.json()["error"])
    else:
        resDict = res.json()
        global orderCount
        orderCount = resDict["result"]
        if (orderCount == 0 and getColor() == 'Green'):
            changeColor('Blue')
        elif (orderCount > 0 and getColor() == 'Blue'):
            changeColor('Green')
    finally:
        timer = threading.Timer(5, polling)
        timer.start()


def showNum():
    # timerTens = threading.Timer(1/hz/2, showSingleNum, [orderCount, "tens"])
    # timer = threading.Timer(1/hz, showNum)
    # timerTens.start()
    # timer.start()
    # time.sleep(1/hz/2)
    while True:
        showSingleNum(orderCount, "ones")
        time.sleep(1/hz)
        showSingleNum(orderCount, "tens")
        time.sleep(1/hz)
    # showNum()

def showSingleNum(targetNum, positive):
    GPIO.output(pointTuple, GPIO.LOW)
    GPIO.output(pointDict[positiveDict["ones"]], GPIO.HIGH)
    GPIO.output(pointDict[positiveDict["tens"]], GPIO.HIGH)

    if positive == "tens":
        num = targetNum//10
    elif positive == "ones":
        num = targetNum % 10

    GPIO.output(pointDict[positiveDict[positive]], GPIO.LOW)
    for item in transferDict[num]:
        GPIO.output(pointDict[item], GPIO.HIGH)


def initNum():
    GPIO.setup(pointTuple, GPIO.OUT)
    # showNum()
    t = threading.Thread(target=showNum)
    t.start()


def getColor():
    for color in colorDict:
        if GPIO.input(colorDict[color]) == 0:
            return color
    return None


def initBtn():
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BtnPin, GPIO.RISING,
                          callback=detectClick, bouncetime=1000)


def detectClick(chn):
    if getColor() == "Green":
        changeColor("Red")
        # startLaser("gcode50.nc")
        res = requests.get(
            r'https://o.api.troncell.com/api/services/app/OrderExtension/GetNextOrderGcodeFile', headers={"tenantId": "5056","type":"4   fvdddddddddddddddddd"})
        try:
            res.raise_for_status()
        except BaseException as e:
            logging.error(e)
            if res.status_code == 500:
                logging.error(res.json()["error"])
            changeColor('Green')
        else:
            resDict = res.json()
            res = requests.get(resDict["result"])
            fileName = resDict["result"].split("/")[-1]
            global nowOrderId
            nowOrderId = int(fileName.split(".")[-2])
            with open(fileName, 'wb') as activeFile:
                for chunk in res.iter_content(len(res.content)):
                    activeFile.write(chunk)
            startLaser(fileName)


def startLaser(fileName):
    print("startLaser", fileName)
    app.loadAndRun(fileName)
    # app.loadDialog()

def callback():
    res = requests.get(r'https://o.api.troncell.com/api/services/app/OrderExtension/ConfirmPrintOrder',
                       headers={"tenantId": "5056"}, params={"orderId": nowOrderId})
    try:
        res.raise_for_status()
    except BaseException as e:
        logging.error(e)
        if res.status_code == 500:
            logging.error(res.json()["error"])
    finally:
        if orderCount == 0:
            changeColor('Blue')
        else:
            changeColor('Green')


# initNum()
# initColor()
# polling()
# initBtn()
