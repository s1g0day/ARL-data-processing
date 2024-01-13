import json
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def arl_login_main(login_url, login_name, login_password):

    json_data = {
        'username': login_name,
        'password': login_password,
    }
    login_res = requests.post(login_url + '/api/user/login', json=json_data, verify=False)
    
    # 判断是否登陆成功：
    if "401" not in login_res.text:
        token = json.loads(login_res.text)['data']['token']
        print("[+] Login Success!!")
        return token
    else:
        print("[-] login Failure! ")