import requests
import json
from requests.exceptions import ReadTimeout

headers = {
    'content-type': 'application/json;charset=utf8'
}
payload = {
    "perception": {
        "inputText": {
            "text": "附近的酒店"
        },
        "selfInfo": {
            "location": {
                "city": "无锡",
                "province": "江苏",
                "street": "惠钱路"
            }
        }
    },
    "userInfo": {
        "apiKey": "25867d758bf840f18c801a669bc70b3c",
        "userId": "2"
    }
}
try:
    res = requests.post('http://openapi.tuling123.com/openapi/api/v2',
                        data=json.dumps(payload), headers=headers)
    res.raise_for_status()
except BaseException as e:
    print("BaseException", type(e), e)
    try:
        if res.json()["error"]:
            print(res.json()["error"])
    except BaseException:
        pass
else:
    print(res.json())
    print(res.text)
finally:
    print('request over')
