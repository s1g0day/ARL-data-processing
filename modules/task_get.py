# 删除ARL计划任务
import json
import time
import math
import random
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 获取任务ID
def get_task_ids(url, token):
    task_params = {
        'size': '10',
        'page': '1',
    }

    task_response = requests.get(url + '/api/task/', params=task_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_data = json.loads(task_response.text)
    task_data_number = task_data["total"]
    if task_data_number == 0:
        print("计划任务为空")
        exit()
    
    #计算页数，可以直接指定total_pages = 10 删除10页内容
    total_pages = math.ceil(task_data_number / 10)
    # total_pages = 1

    # 获取 items 数据
    task_items = []
    for page in range(1, total_pages + 1):
        task_params['page'] = str(page)
        task_response = requests.get(url + '/api/task/', params=task_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_page_data = json.loads(task_response.text)

        for i in range(len(task_page_data["items"])):
            task = task_page_data["items"][i]
            print(f"id: {task['_id']}, status: {task['status']}, name: {task['name']}, targets: {task['target']}")
            
    return task_items, task_data_number

def task_get_main(url, token):
    print("开始获取所有任务数据")
    task_items, datas = get_task_ids(url, token)
