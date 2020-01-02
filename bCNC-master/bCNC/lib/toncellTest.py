'''
进入页面先亮蓝色(空闲)，显示0
轮询并显示订单数，大于0则亮绿灯(就绪)
绿灯(就绪)状态下点击开关变为红色(工作中)，通过接口获取待打印订单的gcode并下载到本地，开始打印
打印结束后通过文件名获得orderId并告知后端打印完成
'''
# import RPi.GPIO as GPIO
import requests
import threading
import time
import datetime
import logging


colorDict = {
    'Red': 36,
    'Blue': 37,
    'Green': 38,
    'Anode': 40
}
colorTuple = tuple(map(lambda item: colorDict[item], colorDict))

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




def changeColor(color):
    print(color)


def polling():
    res = requests.get(
        r'https://o.api.troncell.com/api/services/app/OrderExtension/GetPrintOrderCount', headers={"tenantId": "5056"})
    print(res)
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

def getColor():
    return "Green"


print("troncellTest start")