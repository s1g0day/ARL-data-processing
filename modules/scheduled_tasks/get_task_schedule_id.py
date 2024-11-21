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

def get_schedule_data(url, token, params):
    """统一的API请求处理函数"""
    response = requests.get(
        url + '/api/task_schedule/',
        params=params,
        headers=arl_headers_main(url, token),
        verify=False,
        timeout=(4, 20)
    )
    return json.loads(response.text)

def get_schedule_count(url, token, status):
    """获取计划任务的总数和页数"""
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
            params['schedule_status'] = current_status
            schedule_data = get_schedule_data(url, token, params)
            total_number += schedule_data["total"]
            
        if total_number == 0:
            print("计划任务为空")
            exit()
            
        total_pages = math.ceil(total_number / 10)
        base_params['schedule_status'] = available_status
        return total_pages, total_number, base_params
    
    base_params['schedule_status'] = status
    schedule_data = get_schedule_data(url, token, base_params)
    schedule_data_number = schedule_data["total"]
    
    if schedule_data_number == 0:
        print("计划任务为空")
        exit()
    
    total_pages = math.ceil(schedule_data_number / 10)
    return total_pages, schedule_data_number, base_params

def get_page_schedules(url, token, params, status_list):
    """获取单页的所有计划任务"""
    schedule_items = []
    for current_status in status_list:
        current_params = params.copy()
        current_params['schedule_status'] = current_status
        schedule_data = get_schedule_data(url, token, current_params)
        schedule_items.extend(schedule_data["items"])
    return schedule_items

def get_task_schedule_id_main(url, token, status):
    """获取计划任务ID列表的主函数"""
    total_pages, schedule_data_number, schedule_params = get_schedule_count(url, token, status)
    schedule_items = []

    for page in range(1, total_pages + 1):
        schedule_params['page'] = str(page)
        
        if status.startswith("no_"):
            status_list = schedule_params['schedule_status']
            items = get_page_schedules(url, token, schedule_params, status_list)
        else:
            status_list = [schedule_params['schedule_status']]
            items = get_page_schedules(url, token, schedule_params, status_list)
        
        schedule_items.extend(items)

    return schedule_items, schedule_data_number