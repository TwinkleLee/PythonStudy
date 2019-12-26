import requests
import threading

def polling():
    payload = {'Subkey': '48cea11fd6ee4e0987b6ab00785e87c01'}
    res = requests.get(
        r'https://s1.api.troncell.com/api/services/app/SensingDevice/GetAds', params=payload)
    resDict = res.json()
    print(resDict)
    if(resDict["error"]):
        print("出错", resDict["error"]["message"])
    else:
        print(resDict["result"])

    timer = threading.Timer(3, polling)
    timer.start()

polling()