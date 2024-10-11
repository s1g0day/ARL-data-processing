import json
import math
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 获取页数
def Get_Page_Count(url, token, status):
    task_params = {
        'size': '10',
        'page': '1',
        'status': status,
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
    return total_pages, task_data_number, task_params

# 获取任务ID
def get_task_ids(url, token, status):

    total_pages, task_data_number, task_params = Get_Page_Count(url, token, status)

    # 获取 items 数据，返回总数据
    task_items = []
    for page in range(1, total_pages + 1):
        # time.sleep(random.random()*3)
        task_params['page'] = str(page)
        task_response = requests.get(url + '/api/task/', params=task_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_page_data = json.loads(task_response.text)

        for item in task_page_data["items"]:
            task_items.append(item)
    return task_items, task_data_number

# 获取任务ID, 逐条打印数据
def task_get_main(url, token, status):
    total_pages, task_data_number, task_params = Get_Page_Count(url, token, status)

    # 获取 items 数据,逐条打印数据
    task_items = []
    for page in range(1, total_pages + 1):
        task_params['page'] = str(page)
        task_response = requests.get(url + '/api/task/', params=task_params, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
        task_page_data = json.loads(task_response.text)

        for i in range(len(task_page_data["items"])):
            task = task_page_data["items"][i]
            print(f"Progress of page:{page}, id:{task['_id']}, status:{task['status']}, name:{task['name']}, targets:{task['target']}")
            task_items.append(task)
            
    return task_items, task_data_number