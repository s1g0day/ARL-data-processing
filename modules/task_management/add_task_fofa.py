import json
import time
import random
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# fofa 任务下发
def task_fofa_add_main(url, token, policy_id, domain, index):

    json_data = {
        'name': domain + "_task_fofa_" + str(index),
        'query': domain,
        'policy_id': policy_id,
    }
    time.sleep(random.random()*3)
    response = requests.post(url + '/api/task_fofa/submit', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    data = json.loads(response.text)
    print(f"Domain:{domain}, Add_task_fofa_status:{data['message']}")