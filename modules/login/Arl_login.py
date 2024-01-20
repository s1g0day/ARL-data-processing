import json
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 验证账密, 获取token
def arl_login_main(login_url, login_name, login_password):

    json_data = {
        'username': login_name,
        'password': login_password,
    }
    response = requests.post(login_url + '/api/user/login', json=json_data, verify=False)
    # 判断是否登陆成功
    if "401" in response.text:
        print("[-] login Failure! ")
    else:
        print("[+] Login Success!!")
        return json.loads(response.text)['data']['token']
