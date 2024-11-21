import json
import math
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 定义所有可能的状态
ALL_STATUS = [
    "waiting", "done", "error", "stop",
    "domain_brute", "dns_query_plugin", "arl_search", "alt_dns",
    "search_engines", "port_scan", "ssl_cert", "find_site",
    "fetch_site", "site_identify", "site_capture", "site_spider",
    "file_leak", "nuclei_scan", "web_info_hunter", "findvhost"
]

def get_task_data(url, token, params):
    """统一的API请求处理函数"""
    response = requests.get(
        url + '/api/task/',
        params=params,
        headers=arl_headers_main(url, token),
        verify=False,
        timeout=(4, 20)
    )
    return json.loads(response.text)

def Get_Page_Count(url, token, status):
    base_params = {
        'size': '10',
        'page': '1'
    }
    
    if status.startswith("no_"):
        excluded_status = status[3:]
        available_status = [s for s in ALL_STATUS if s != excluded_status]
        
        total_number = 0
        for current_status in available_status:
            params = base_params.copy()
            params['status'] = current_status
            task_data = get_task_data(url, token, params)
            total_number += task_data["total"]
            
        if total_number == 0:
            print("计划任务为空")
            exit()
            
        total_pages = math.ceil(total_number / 10)
        base_params['status'] = available_status
        return total_pages, total_number, base_params
    
    base_params['status'] = status
    task_data = get_task_data(url, token, base_params)
    task_data_number = task_data["total"]
    
    if task_data_number == 0:
        print("计划任务为空")
        exit()
    
    total_pages = math.ceil(task_data_number / 10)
    return total_pages, task_data_number, base_params

def get_page_items(url, token, params, status_list):
    """获取单页的所有任务项"""
    task_items = []
    for current_status in status_list:
        current_params = params.copy()
        current_params['status'] = current_status
        task_data = get_task_data(url, token, current_params)
        task_items.extend(task_data["items"])
    return task_items

def process_tasks(url, token, status, print_progress=False):
    """统一的任务处理函数"""
    total_pages, task_data_number, task_params = Get_Page_Count(url, token, status)
    task_items = []

    for page in range(1, total_pages + 1):
        task_params['page'] = str(page)
        
        if status.startswith("no_"):
            status_list = task_params['status']
            items = get_page_items(url, token, task_params, status_list)
        else:
            status_list = [task_params['status']]
            items = get_page_items(url, token, task_params, status_list)

        if print_progress:
            for task in items:
                print(f"Progress of page:{page}, id:{task['_id']}, status:{task['status']}, name:{task['name']}, targets:{task['target']}")
        
        task_items.extend(items)

    return task_items, task_data_number

def get_task_ids(url, token, status):
    """获取任务ID列表"""
    return process_tasks(url, token, status, print_progress=False)

def task_get_main(url, token, status):
    """获取任务ID列表并打印进度"""
    return process_tasks(url, token, status, print_progress=True)