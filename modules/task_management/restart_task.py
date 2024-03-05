import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 重启任务
def restart_task_main(url, json_data, token):

    task_restart_response = requests.post(url + '/api/task/restart/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_restart_data = json.loads(task_restart_response.text)
    print(f"Restart_status:{task_restart_data['message']}")