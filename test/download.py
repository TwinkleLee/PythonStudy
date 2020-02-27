# import threading

# def polling():
#     payload = {'Subkey': '48cea11fd6ee4e0987b6ab00785e87c01'}
#     res = requests.get(
#         r'https://s1.api.troncell.com/api/services/app/SensingDevice/GetAds', params=payload)
#     resDict = res.json()
#     print(resDict)
#     if(resDict["error"]):
#         print("出错", resDict["error"]["message"])
#     else:
#         print(resDict["result"])

#     timer = threading.Timer(3, polling)
#     timer.start()

# polling()

import requests
res = requests.get('http://139.196.240.230:288/3.txt')
# res.encoding='utf-16'
# res.encoding='ISO-8859-1'
# print(res.text)
res.raise_for_status()
# print(str(res.content,'utf-16'))

readFile = open('download.txt', 'r', encoding='utf-16', errors='replace')

print(readFile.read())
# playFile = open('download.txt', 'wb')
# for chunk in res.iter_content(len(res.content)):
# playFile.write(chunk)
