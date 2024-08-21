import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 停止计划任务
def stop_task_schedule_main(url, json_data, token):

    task_schedule_stop_response = requests.post(url + '/api/task_schedule/stop/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_schedule_stop_data = json.loads(task_schedule_stop_response.text)
    print(f"Stop_status:{task_schedule_stop_data['message']}")