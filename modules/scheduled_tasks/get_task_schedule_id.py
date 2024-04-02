import json
import math
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 获取任务ID
def get_task_schedule_id_main(url, token):
    task_schedule_params = {
        'size': '10',
        'page': '1',
    }

    task_schedule_response = requests.get(url + '/api/task_schedule/', params=task_schedule_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_schedule_data = json.loads(task_schedule_response.text)
    task_schedule_data_number = task_schedule_data["total"]
    if task_schedule_data_number == 0:
        print("计划任务为空")
        exit()

    # 计算页数，可以直接指定total_pages = 10 删除10页内容
    total_pages = math.ceil(task_schedule_data_number / 10)
    # total_pages = 20
    task_schedule_ids = []
    for page in range(1, total_pages + 1):
        task_schedule_params['page'] = str(page)
        task_schedule_response = requests.get(url + '/api/task_schedule/', params=task_schedule_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_schedule_page_data = json.loads(task_schedule_response.text)

        for item in task_schedule_page_data["items"]:
            task_schedule_ids.append(item)

    return task_schedule_ids, task_schedule_data_number
