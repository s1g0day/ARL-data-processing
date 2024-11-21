import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def github_task(url, domain, token):
    json_data = {
    'name': '1',
    'keyword': '1',
    }

    response = requests.post(url + '/api/github_task/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))    
    data = json.loads(response.text)
    print(domain + "_添加fofa任务状态: " + data['message'])

def github_task_add_main(url, token, url_file):
    with open(url_file, 'r', encoding='utf-8') as domains:
        domain_list = domains.readlines()

    total_domains = len(domain_list)
    for index, domain in enumerate(domain_list):
        domain = domain.strip()
        print(f"\nProcessing domain {index+1}/{total_domains}: {domain}")
        # time.sleep(random.random()*6)
        github_task(url, domain, token)

if __name__ == '__main__':


    url = "https://192.168.88.21:5003"
    token = "aa5622fb3e4ad91b65365e31571881d9"
    url_file = "1.txt"
    
    github_task_add_main(url, token, url_file)

