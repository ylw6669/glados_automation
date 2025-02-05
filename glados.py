import requests
import json
import os

# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # 企业微信机器人Webhook Key 申请地址：企业微信群添加机器人后获取
    webhook_key = os.environ.get("PUSHPLUS_TOKEN", "")
    # 推送内容
    sendContent = ''
    # glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("GLADOS_COOKIE", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量') 
        cookies = []
        exit(0)
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload = {
        'token': 'glados.one'
    }
    for cookie in cookies:
        checkin = requests.post(url, headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent, 'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
        state = requests.get(url2, headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})
        #--------------------------------------------------------------------------------------------------------#  
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        email = state.json()['data']['email']
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            print("签到成功")  # 日志输出
            sendContent += f'{email}----{mess}----剩余({time})天\n'
        else:
            # 发送Cookie失效通知
            if webhook_key:
                webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}'
                data = {
                    "msgtype": "text",
                    "text": {
                        "content": f"⚠️{email}的Cookie已失效，请及时更新！",
                        "mentioned_list": ["@all"]
                    }
                }
                requests.post(webhook_url, json=data)
            print('cookie已失效')  # 日志输出
        #--------------------------------------------------------------------------------------------------------#   
    # 发送签到汇总信息
    if webhook_key and sendContent:
        webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}'
        content = "🎉Glados签到结果：\n" + sendContent.strip()
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        requests.post(webhook_url, json=data)
