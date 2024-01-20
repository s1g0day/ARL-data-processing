# 删除ARL计划任务
import json
import math
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 停止计划任务
def task_schedule_stop(url, json_data, token):

    task_schedule_stop_response = requests.post(url + '/api/task_schedule/stop/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_schedule_stop_data = json.loads(task_schedule_stop_response.text)
    print("停止状态: " + task_schedule_stop_data['message'])

# 删除计划任务
def task_schedule_delete(url, json_data, token):

    task_schedule_delete_response = requests.post(url + '/api/task_schedule/delete/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_schedule_delete_data = json.loads(task_schedule_delete_response.text)
    print("删除状态: " + task_schedule_delete_data['message'])

# 获取任务ID
def get_task_schedule_id(url, token):
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

    task_schedule_ids = []
    for page in range(1, total_pages + 1):
        task_schedule_params['page'] = str(page)
        task_schedule_response = requests.get(url + '/api/task_schedule/', params=task_schedule_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_schedule_page_data = json.loads(task_schedule_response.text)

        for item in task_schedule_page_data["items"]:
            task_schedule_ids.append(item)

    return task_schedule_ids, task_schedule_data_number

# 主函数
def task_schedule_delete_main(url, token):
    task_schedule_ids, datas = get_task_schedule_id(url, token)
    json_data = {
        '_id': [
        ],
    }

    for index, task_schedule in enumerate(task_schedule_ids):
        # time.sleep(random.random()*3)
       
        task_schedule_id = task_schedule["_id"]
        print(f"第{index + 1}/{datas}个任务调度 id: {task_schedule_id}")
        # 追加字符到'_id'键对应的列表中
        json_data['_id'].append(task_schedule_id)

    task_schedule_stop(url, json_data, token)
    task_schedule_delete(url, json_data, token)

