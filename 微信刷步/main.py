
import requests
import random
import time
import json
import os

user = os.environ.get("STEP_USER")
password = os.environ.get("STEP_PASSWORD")
appID = os.environ.get("APPID")
appSecret = os.environ.get("APPSECRET")
userId = os.environ.get("USERID")
template_id = os.environ.get("STEP_TID")

def get_access_token():
    global appID, appSecret
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


def send(access_token, msg):
    global template_id,userId
    body = {
        "touser": userId.strip(),
        "template_id": template_id,
        "url": "",
        "data": {
            "msg": {
                "value": msg
            },            
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)

time.sleep(random.randint(1,20))

step = random.randint(36589, 62594)

url = "https://api.leafone.cn/api/misport"
params = {
    "user": user,
    "password": password,
    "step": step
}
response = request.get(url, params=params)
if response.statuss_code == 200:
    data = json.loads(response.text)
    if data["code"] == 200:
        msg = f"今日步数提交成功，共提交 {step} 步。"
    else:
        msg = f"今日步数提交失败，错误代码 {data['code']}，错误信息：{data['msg']} "
else:
    msg = "今日步数提交失败，失败原因：接口访问失败！"
    
    
access = get_access_token()
send(access, msg)
    
