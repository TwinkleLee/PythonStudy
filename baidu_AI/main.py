# coding=utf-8

import ssl
import sys
import json
import base64
import os

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus


# 防止https证书校验不正确
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = '6m61522xnks1g90FiY7NhaMk'

SECRET_KEY = 'Zujjx7cTROhW1UgarplBXQj4aegNoe5j'


IMAGE_RECOGNIZE_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish"


"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    读取文件
"""


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""


def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except URLError as err:
        print(err)


"""
    调用菜品识别接口并打印结果
"""


def print_result(filename, url):
    # 获取图片
    file_content = read_file(filename)

    response = request(url, urlencode(
        {
            'image': base64.b64encode(file_content),
        }))
    result_json = json.loads(response)

    # 打印图片结果
    print(os.path.split(filename)[1])
    for data in result_json["result"]:
        print(data)


if __name__ == '__main__':

    # 获取access token
    token = fetch_token()

    # 拼接图像识别url
    url = IMAGE_RECOGNIZE_URL + "?access_token=" + token


    nowDir = os.path.dirname(__file__)
    # print_result(os.path.join(nowDir, "./food1.jpg"), url)
    # print_result(os.path.join(nowDir, "./food2.jpg"), url)
    # print_result(os.path.join(nowDir, "./food3.jpg"), url)
    # print_result(os.path.join(nowDir, "./food_test.jpg"), url)
    print_result(os.path.join(nowDir, "./food_test2.jpg"), url)

