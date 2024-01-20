import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 验证token
def token_verification_main(url, token):

    response = requests.get(url + '/api/console/info', headers=arl_headers_main(url, token), verify=False, timeout=(4,20))

    # 判断是否登陆成功
    if "401" in response.text:
        print("[-] Token no login")
    else:
        print("[+] Token login success")
        return True
       