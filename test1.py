# import requests
# import threading

# myNumber = 0


# def showNum():
#     showSingleNum("A")
#     timerTens = threading.Timer(1/50/2, showSingleNum, ["B"])
#     timer = threading.Timer(1/50, showNum)
#     timerTens.start()
#     timer.start()


# def showSingleNum(lamp):
#     print(lamp)


# def polling():
#     res = requests.get(
#         r'https://o.api.troncell.com/api/services/app/OrderExtension/GetPrintOrderCount', headers={"tenantId": "5056"})
#     global myNumber
#     myNumber = res.json().result
#     timer = threading.Timer(5, polling)
#     timer.start()


# showNum()
# polling()


# print(__name__)


# import threading
# import time


# def td():

#     time.sleep(1)
#     print('当前线程名字是：' + threading.current_thread().name)
#     time.sleep(1)


# if __name__ == '__main__':
#     td()
#     s_time = time.time()
#     print(s_time)

#     print('这是主线程：' + threading.current_thread().name)
#     tdg_list = []

#     for i in range(5):
#         t = threading.Thread(target=td)
#         tdg_list.append(t)

#     for t in tdg_list:
#         # t.setDaemon(True)#设置当前线程(主线程)为守护线程 当前线程(主线程)结束时t线程也结束
#         t.start()
#         t.join()#在t完成前阻塞当前线程(主线程)

#     print('主线程结束了！', threading.current_thread().name)
#     print('一共用时：', time.time()-s_time)


import threading

def fn(num=50):
    print(threading.current_thread().name, num)
t = threading.Thread(target=fn, args=[100], name='LoopThread')
t.start()
fn()
