import os
import requests

appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
userId = os.environ.get("USERID")
template_id = os.environ.get("MYTV_TID")


def get_access_token():
    global appID, appSecret
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token
    
    
def send(num, pd):
    global template_id,userId
    access_token = get_access_token()
    body = {
        "touser": userId.strip(),
        "template_id": template_id,
        "url": "",
        "data": {
            "num": {
                "value": num
            },
            "pd":{
                "value": pd
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)


fail_list = []
num = 0
res = requests.get("http://tv.yzh999.cn/z/y.txt")
res.encoding = "utf-8"
lines = res.text.split("\n")
for line in lines:
   line = line.replace("\n", "")
   list = line.split(",")
   if list[1] != "#genre#":
       num+=1
       name = list[0]
       link = list[1]
       print(f"正在测试第{num}个: {name}")            
       try:
           response = requests.get(link, timeout=5)
           response.encoding = "utf-8"
           if response.status_code != 200:
               fail_list.append(name)
       except Exception as e:
           fail_list.append(name)
           
           
o = 0
for i in fail_list:
     o+=1
  
# print(o, fail_list)                   
send(o, fail_list.join(","))

