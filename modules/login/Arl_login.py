import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 判断是否为JSON格式
def is_json(response_text):
    try:
        json_object = json.loads(response_text)
        return True
    except ValueError as e:
        return False
    
# 验证账密, 获取token
def arl_login_main(login_url, login_name, login_password):

    json_data = {
        'username': login_name,
        'password': login_password,
    }
    try:
        response = requests.post(login_url + '/api/user/login', json=json_data, verify=False)
        if is_json(response.text):
            # 判断是否登陆成功
            if "200" in response.text:
                print("[+] Login Success!")
                return json.loads(response.text)['data']['token']
            elif "401" in response.text:
                print("[-] Wrong username or password!")
        else:
            # 请求异常,
            print("[-] Request Error!")
    except:
        return

# 验证token
def token_verification_main(url, token):
    try:
        response = requests.get(url + '/api/console/info', headers=arl_headers_main(url, token), verify=False, timeout=(4,20))
        if is_json(response.text):
            # 判断是否登陆成功
            if "200" in response.text:
                print("[+] Token is valid")
                return True
            elif "401" in response.text:
                print("[-] Invalid token")
        else:
            # 请求异常,
            print("[-] Request Error!")
    except:
        return