# import requests
# try:
#     res = requests.get(r'https://o.api.troncell.com/api/serv1ices/app/OrderExtension/GetPrintOrderCount',
#                        headers={"tenantId": "5056"}, timeout=0.1)
#     res.raise_for_status()
# except BaseException as e:
#     print("BaseException", type(e), e)
#     try:
#         if res.json()["error"]:
#             print(res.json()["error"])
#     except BaseException:
#         pass
# else:
#     print(res.json()["result"])
# finally:
#     print('request over')

import logging
fh = logging.FileHandler(encoding='utf-8', mode='a', filename='logger.log')
sh = logging.StreamHandler()
logging.basicConfig(handlers=[
    sh, fh], format='%(asctime)s - %(pathname)s - %(module)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.DEBUG)


def a():
    logging.info("hello world")


def b():
    a()


b()
