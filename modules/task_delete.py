# 删除ARL计划任务
import ast
import json
import time
import math
import random
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 先处理json_data数据,然后再删除
def split_json(url, json_data, token):
    
    chunk_size = 500
    # 将字典对象转换回 JSON 字符串
    result_json_str = json.dumps(json_data)

    # 将字符串解析为字典对象
    data = json.loads(result_json_str)

    # 如果 result_json_str 的长度小于等于 chunk_size，则不进行拆分
    if len(data['task_id']) <= chunk_size:
        # 创建一个新的字典对象，只包含 "task_id" 键和原始值
        chunk_data = {"task_id": data['task_id']}
        # # 将字典对象转换为 JSON 字符串并打印
        # chunk_json_str = json.dumps(chunk_data)
        # print(chunk_json_str)
        # 调用任务删除函数
        task_delete(url, chunk_data, token)
    else:
        # 拆分 JSON 数据
        chunks = [list(data['task_id'][i:i+chunk_size]) for i in range(0, len(data['task_id']), chunk_size)]

        # 处理每个部分
        for chunk in chunks:
            # 创建一个新的字典对象，只包含 "task_id" 键和当前部分的值
            chunk_data = {"task_id": chunk}
            # # 将字典对象转换为 JSON 字符串并打印
            # chunk_json_str = json.dumps(chunk_data)
            # print(chunk_json_str)
            # 调用任务删除函数
            task_delete(url, chunk_data, token)
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
    # total_pages = 10

    # 获取 items 数据
    task_items = []
    for page in range(1, total_pages + 1):
        # time.sleep(random.random()*3)
        task_params['page'] = str(page)
        task_response = requests.get(url + '/api/task/', params=task_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_page_data = json.loads(task_response.text)

        for item in task_page_data["items"]:
            task_items.append(item)
    return task_items, task_data_number


# 这种是先获取所有需要删除的id，然后统一删除。

def task_delete_main(url, token):
    print("开始获取所有任务数据")
    task_items, datas = get_task_ids(url, token)
    json_data = {
        "task_id": [
        ],
    }
    print("开始筛选出 status 为 waiting 的任务ID")
    for index, task in enumerate(task_items):
        # if task['status'] == "waiting" and "周期任务" in task["name"]:
        if task['status'] == "stop":
            task_id = task["_id"]
            # print(f"第{index + 1}/{datas}个任务调度 id: {task_id}")
            json_data["task_id"].append(task_id)    # 追加字符到'_id'键对应的列表中
    '''
    删除任务时需要先停止，在删除
    '''
    # 停止
    task_stop(url, json_data, token)
    # 删除
    split_json(url, json_data, token)

# 自定义删除
def task_custom_delete_main(url, delete_id_file, token):

    with open(delete_id_file, "r", encoding="utf-8") as files:
        files = files.readlines()
        for i in files:
            json_data = {
                'task_id': [
                ],
            }
            aaa = i.strip()
            json_data['task_id'].append(aaa) 
            print(json_data)
            # 停止
            # task_stop(url, json_data, token)
            # 删除
            # task_delete(url, json_data, token)
