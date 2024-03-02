import math
import json
import random
import urllib3
import requests
from datetime import datetime, timedelta
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 定时任务
def Timed_tasks(url, token, domain, at_regular_time):
    # 资产发现任务
    task_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'future_scan',
        'policy_id': '65d45e5d18e4a412dc848cce',
        'start_date': at_regular_time,
        'task_tag': 'task',
    }
    # 风险巡航任务
    risk_cruising_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'future_scan',
        'policy_id': '65d45e5d18e4a412dc848cce',
        'start_date': at_regular_time,
        'task_tag': 'risk_cruising',
    }
    task_response = requests.post(url + '/api/task_schedule/', json=task_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    risk_cruising_response = requests.post(url + '/api/task_schedule/', json=risk_cruising_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_data = json.loads(task_response.text)
    risk_cruising_data = json.loads(risk_cruising_response.text)
    print(domain + "_资产发现任务添加任务状态: " + task_data['message'])
    print(domain + "_风险巡航任务添加任务状态: " + risk_cruising_data['message'])

# 周期任务
def Periodic_tasks(url, token, domain, execution_day):
    # 资产发现任务
    task_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'recurrent_scan',
        'policy_id': '65d45e5d18e4a412dc848cce',
        'cron': execution_day,
        'task_tag': 'task',
    }
    # 风险巡航任务
    risk_cruising_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'recurrent_scan',
        'policy_id': '65d45e5d18e4a412dc848cce',
        'cron': execution_day,
        'task_tag': 'risk_cruising',
    }
    task_response = requests.post(url + '/api/task_schedule/', json=task_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    risk_cruising_response = requests.post(url + '/api/task_schedule/', json=risk_cruising_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_data = json.loads(task_response.text)
    risk_cruising_data = json.loads(risk_cruising_response.text)
    print(domain + "_资产发现任务添加任务状态: " + task_data['message'])
    print(domain + "_风险巡航任务添加任务状态: " + risk_cruising_data['message'])

# 获取随机 时分秒
def random_time(execution_time):
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    # 合并随机生成的小时、分钟和秒
    execution_time = execution_time.replace(hour=random_hour, minute=random_minute, second=random_second)
    
    return execution_time

# 时间转为cron格式
def datetime_to_cron(date_time):
    cron_minute = date_time.minute
    cron_hour = date_time.hour
    cron_day = date_time.day
    cron_month = date_time.month
    cron_weekday = date_time.strftime('%w')  # 周日到周六为 0-6
    return f"{cron_minute} {cron_hour} {cron_day} {cron_month} {cron_weekday}"



def task_schedule_add_main(url, token, domains):
    '''
    每组的前 MAX_DOMAINS_PER_GROUP 个 domain 的 随机 cron 为第二天，接着下一个 MAX_DOMAINS_PER_GROUP个 domain 的 随机 cron 为第三天，以此类推
    '''
    print("添加计划任务")
    # 每组最多包含的域名数
    MAX_DOMAINS_PER_GROUP = 200    
    
    domain_count = len(domains)
    groups = math.ceil(domain_count / MAX_DOMAINS_PER_GROUP)
    execution_time = datetime.now()  # 初始时间

    for i in range(groups):
        group_domains = domains[i*MAX_DOMAINS_PER_GROUP:(i+1)*MAX_DOMAINS_PER_GROUP]
        execution_time += timedelta(days=1)

        for j, domain in enumerate(group_domains, start=1):
            domain = domain.strip()    

            # 周期任务
            # cron_format = datetime_to_cron(random_time(execution_time))   # 转换为Cron格式
            # print(f"\nProcessing domain {j+(i*MAX_DOMAINS_PER_GROUP)}/{domain_count}, Domain: {domain}, Execution Time: {cron_format}")
            # Periodic_tasks(url, token, domain, cron_format)   


            # 定时任务
            formatted_time = random_time(execution_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\nProcessing domain {j+(i*MAX_DOMAINS_PER_GROUP)}/{domain_count}, Domain: {domain}, Execution Time: {formatted_time}")
            Timed_tasks(url, token, domain, formatted_time)     