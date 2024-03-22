import hashlib
import json
import random
import time
import os
import requests
from bs4 import BeautifulSoup

appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
userId = os.environ.get("USERID")
template_id = os.environ.get("HLX_TID")
key = os.environ.get("HLX_KEY")
hlx_user_id = os.environ.get("HLX_USERID")
cat_ids = [57,63,43,119,81,16,44,45,96,70,111,71,4,29,107,110,122,90,120,121,115,21,102,3,76,57,92,98,58,82,77,63,22,2,108,1,6]
# cat_ids = [119, 43, 45]


def md5_encode(now, cat_id):
    hash_ob = hashlib.md5()
    content = "cat_id" + str(cat_id) + "time" + str(now) + "fa1c28a5b62e79c3e63d9030b6142e4b"
    hash_ob.update(content.encode('utf-8'))
    return hash_ob.hexdigest()


def get_info(hlx_user_id, key):
    u = "https://floor.huluxia.com/view/level?viewUserID=" + hlx_user_id + "&_key=" + key + "&theme=0"
    head = {
        "Host": "floor.huluxia.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; 21091116AC Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046278 Mobile Safari/537.36"
    }
    r = requests.get(u, headers=head)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    spans = soup.find("li", class_="lev_li_second")
    e = spans.findAll("span")
    s = 0
    for i in e:
        if s == 0:
            name = i.text
        else:
            level = i.text
        s += 1
        spans = soup.find("li", class_="lev_li_forth")
        e = spans.findAll("span")
        s = 0
        for i in e:
            if s == 0:
                now_exp = i.text
            if s == 2:
                next_exp = i.text
            s += 1
    return name, level, now_exp, next_exp


def get_access_token():
    global appID, appSecret
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


def send(access_token, name, level, nowexp, nextexp):
    global template_id, userId, hlx_user_id, key
    body = {
        "touser": userId.strip(),
        "template_id": template_id,
        "url": "https://floor.huluxia.com/view/level?viewUserID=" + hlx_user_id + "&_key=" + key + "&theme=0",
        "data": {
            "name": {
                "value": name
            },
            "level": {
                "value": level
            },
            "nowexp": {
                "value": nowexp
            },
            "nextexp": {
                "value": nextexp
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)


# get_info(hlx_user_id, key)

n_time = int(time.time() * 1000)
headers = {
    "User-Agent": "okhttp/3.8.1",
    "Host": "floor.huluxia.com"
}

for cat_id in cat_ids:
    cat_id = str(cat_id)
    url = "http://floor.huluxia.com/user/signin/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.2.1.9.2&versioncode=385&market_id=tool_web&_key="
    url = url + key + "&device_code=6f77ffab-f206-4ac1-aea2-2651ebd123c8&phone_brand_type=MI&hlx_imei=&hlx_android_id=57262aa2edceb4d0&hlx_oaid=36280b480ea3a9f0&cat_id="
    url = url + cat_id
    data = {
        "sign": md5_encode(n_time, cat_id),
        "platform": "2",
        "gkey": "000000",
        "app_version": "4.2.1.9.2",
        "versioncode": "385",
        "market_id": "tool_web",
        "device_code": "[d]6f77ffab-f206-4ac1-aea2-2651ebd123c8",
        "phone_brand_type": "MI",
        "hlx_imei": "",
        "hlx_android_id": "57262aa2edceb4d0",
        "hlx_oaid": "36280b480ea3a9f0",
        "cat_id": str(cat_id),
        "time": str(n_time)
    }
    response = requests.post(url=url, data=data, headers=headers)
    response.encoding = "utf-8"
    print(response.text)
    time.sleep(random.randint(5, 20))

name, level, nowexp, nextexp = get_info(hlx_user_id, key)
send(get_access_token(), name, level, nowexp, nextexp)
