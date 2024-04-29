'''
new Env('爽歪歪短剧');
注册入口:https://admin.yunhuikunpeng.com/appDownload/
authorization&clientid多号@隔开
算是一个分虹平台，每天协议刷取贡献币获取会员参与平台分红(脚本未在青龙测试有bug勿喷)
'''

import requests
import random
import time
import os

appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
userId = os.environ.get("USERID")
template_id = os.environ.get("SWW_TID")
sww = os.environ.get('SWW')


def get_access_token():
    global appID, appSecret
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token
    
    
def send(access_token, num):
    global template_id,userId
    body = {
        "touser": userId.strip(),
        "template_id": template_id,
        "url": "",
        "data": {
            "num": {
                "value": num
            }            
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)


def taskCompleted(authorization, clientid):
    url = "https://admin.yunhuikunpeng.com/prod-api/appUser/taskCompleted"
    headers = {
        "Host": "admin.yunhuikunpeng.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; RMX3562 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.98 Mobile Safari/537.36",
        "authorization": authorization,
        "clientid": clientid,
        "content-type": "application/x-www-form-urlencoded",
        "content-length": "0",
        "accept-encoding": "gzip"
    }
    completed = 0
    while completed < 10:
        response = requests.post(url, headers=headers)
        response_data = response.json()
        msg = response_data['msg']
        completed = response_data["data"]["completed"]
        print(f"广告观看结果:{msg}----->>当前已观看广告{completed}个广告")
        delay = random.randint(60, 65)
        time.sleep(delay)
if __name__ == "__main__":
    sww_list = sww.split('@')
    n = 0
    for num, sww_item in enumerate(sww_list, start=1):
        authorization, clientid = sww_item.split('&')
        print(f"=====开始执行第{num}个账号任务=====")
        print("---------开始执行十个广告任务---------")
        taskCompleted(authorization, clientid)
        n +=1
    acc = get_access_token()
    send(acc,n)
