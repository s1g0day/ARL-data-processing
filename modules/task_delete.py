# 删除ARL计划任务
import json
import time
import math
import random
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 重启任务
def task_restart(url, json_data, token):

    task_restart_response = requests.post(url + '/api/task/restart/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_restart_data = json.loads(task_restart_response.text)
    print("重启状态: " + task_restart_data['message'])

# 停止任务
def task_stop(url, json_data, token):

    task_stop_response = requests.post(url + '/api/task/batch_stop/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_stop_data = json.loads(task_stop_response.text)
    print("停止状态: " + task_stop_data['message'])

# 删除任务
def task_delete(url, json_data, token):
    # 追加 "del_task_data" 到 "json_data" 字典中
    json_data.update({'del_task_data': True})

    task_delete_response = requests.post(url + '/api/task/delete/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_delete_data = json.loads(task_delete_response.text)
    print("删除状态: " + task_delete_data['message'])

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
    # total_pages = 3
    # 获取ID
    task_ids = []
    for page in range(1, total_pages + 1):
        task_params['page'] = str(page)
        task_response = requests.get(url + '/api/task/', params=task_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_page_data = json.loads(task_response.text)

        for item in task_page_data["items"]:
            task_ids.append(item)

    return task_ids, task_data_number

# 获取需要重启的任务ID
def task_restart_id(task_ids, datas):

    json_data = {
        'task_id': [
        ],
    }
    for index, task in enumerate(task_ids):
        # if task['status'] != "done" and task['status'] != "stop":
        if task['status'] == "stop":
            task_id = task["_id"]
            print(f"第{index + 1}/{datas}个任务调度 id: {task_id}, 状态为{task['status']}")
            json_data['task_id'].append(task_id)    # 追加字符到'_id'键对应的列表中
    return json_data
            
# 获取需要删除的任务ID
def task_delete_id(task_ids, datas):
    
    json_data = {
        'task_id': [
        ],
    }
    for index, task in enumerate(task_ids):
        # if task['status'] == "waiting" and "周期任务" in task["name"]:
        if task['status'] == "waiting":
            task_id = task["_id"]
            print(f"第{index + 1}/{datas}个任务调度 id: {task_id}")
            json_data['task_id'].append(task_id)    # 追加字符到'_id'键对应的列表中
    return json_data


# 主函数
def task_delete_main(url, token):
    task_ids, datas = get_task_ids(url, token)

    # json_delete_data = task_delete_id(task_ids, datas)
    json_restart_data = task_restart_id(task_ids, datas)
    
    '''
    停止任务时需要调用停止函数，修改需要状态status
    删除任务时需要先停止，在删除
    重启任务时会创建新任务，因此需要先重启，然后删除原任务
    '''
    # 停止
    # task_stop(url, json_restart_data, token)
    # 重启
    # task_restart(url, json_restart_data, token)
    # 删除
    # task_delete(url, json_restart_data, token)