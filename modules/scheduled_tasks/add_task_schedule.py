import math
import json
import time
import random
import urllib3
import requests
from datetime import datetime, timedelta
from common.arl_headers import arl_headers_main
from common.convert_to_ascii import convert_to_ascii,is_chinese_domain
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 定时任务
def Timed_tasks(url, token, policy_id, domain, at_regular_time):
    # 资产发现任务
    task_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'future_scan',
        'policy_id': policy_id,
        'start_date': at_regular_time,
        'task_tag': 'task',
    }
    # 风险巡航任务
    risk_cruising_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'future_scan',
        'policy_id': policy_id,
        'start_date': at_regular_time,
        'task_tag': 'risk_cruising',
    }
    task_response = requests.post(url + '/api/task_schedule/', json=task_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    risk_cruising_response = requests.post(url + '/api/task_schedule/', json=risk_cruising_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_data = json.loads(task_response.text)
    risk_cruising_data = json.loads(risk_cruising_response.text)
    print(f"Domain:{domain}, Asset_Discovery_Add_status:{task_data['message']}")
    print(f"Domain:{domain}, Risk_cruising_Add_status:{risk_cruising_data['message']}")

# 周期任务
def Periodic_tasks(url, token, policy_id, domain, execution_day):
    # 资产发现任务
    task_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'recurrent_scan',
        'policy_id': policy_id,
        'cron': execution_day,
        'task_tag': 'task',
    }
    # 风险巡航任务
    risk_cruising_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'recurrent_scan',
        'policy_id': policy_id,
        'cron': execution_day,
        'task_tag': 'risk_cruising',
    }
    task_response = requests.post(url + '/api/task_schedule/', json=task_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    risk_cruising_response = requests.post(url + '/api/task_schedule/', json=risk_cruising_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_data = json.loads(task_response.text)
    risk_cruising_data = json.loads(risk_cruising_response.text)
    print(f"Domain:{domain}, Asset_Discovery_Add_status:{task_data['message']}")
    print(f"Domain:{domain}, Risk_cruising_Add_status:{risk_cruising_data['message']}")

# 获取随机 时分秒
def random_time(execution_time):
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    # 合并随机生成的小时、分钟和秒
    execution_time = execution_time.replace(hour=random_hour, minute=random_minute, second=random_second)
    
    return execution_time

# 获取随机cron, 每个月随即天数随机日期
def generate_random_all_cron():
    # 获取当前日期和时间
    now = datetime.now()
    
    # 确定月份和日期的范围，允许包括当前月、下个月和下下个月
    current_month = now.month
    next_month = (current_month + 1) % 12
    next_next_month = (current_month + 2) % 12
    current_day = now.day
    
    # 获取本月的最大天数
    max_day_current_month = (now.replace(day=1, month=next_month) - timedelta(days=1)).day
    
    # 生成随机的日期，确保在今天之后
    month = random.choice([current_month, next_month, next_next_month])
    day = random.randint(current_day + 1, max_day_current_month)
    
    # 生成随机的分钟和小时
    minute = random.randint(0, 59)
    hour = random.randint(0, 23)
    
    # 组合 cron 表达式
    cron_expression = f"{minute} {hour} {day} {month} *"
    
    return cron_expression

# 获取随机cron
def generate_random_cron(execution_time):
    
    # 确定月份和日期
    current_month = execution_time.month
    current_day = execution_time.day

    # 生成随机的分钟和小时
    current_hour = random.randint(0, 23)
    current_minute = random.randint(0, 59)

    # 组合 cron 表达式
    cron_expression = f"{current_minute} {current_hour} {current_day} {current_month} *"

    return cron_expression

def task_schedule_add_main(url, token, policy_id, domains, Task_Type, start_index):
    print("添加计划任务")
    # 每组最多包含的域名数
    MAX_DOMAINS_PER_GROUP = 200    
    
    domain_count = len(domains)
    # 计算页数 groups
    groups = math.ceil(domain_count / MAX_DOMAINS_PER_GROUP)
    execution_time = datetime.now()  # 初始时间

    for i in range(groups):
        group_domains = domains[i*MAX_DOMAINS_PER_GROUP:(i+1)*MAX_DOMAINS_PER_GROUP]
        execution_time += timedelta(days=1)

        for j, domain in enumerate(group_domains, start=1):
            domain = domain.strip()    

            if is_chinese_domain(domain):
                # 转换为 ASCII 格式
                ascii_domain = convert_to_ascii(domain)
                if ascii_domain:
                    print("转换后的 ASCII 域名:", ascii_domain)
                    domain = ascii_domain
            else:
                domain = domain
            
            if (i * MAX_DOMAINS_PER_GROUP + j) >= start_index:  # 检查是否达到指定的起始索引
                if Task_Type == "cycle":
                    # 周期任务
                    # cron_format = generate_random_cron(execution_time)   # 生成一个随机的 cron 
                    cron_format = generate_random_all_cron()   # 生成一个随机的 cron 表达式
                    print(f"\nProcessing domain {i * MAX_DOMAINS_PER_GROUP + j}/{domain_count}, Domain: {domain}, Execution Time: {cron_format}")
                    # Periodic_tasks(url, token, policy_id, domain, cron_format)   

                elif Task_Type == "calm":
                    # 定时任务
                    formatted_time = random_time(execution_time).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"\nProcessing domain {i * MAX_DOMAINS_PER_GROUP + j}/{domain_count}, Domain: {domain}, Execution Time: {formatted_time}")
                    Timed_tasks(url, token, policy_id, domain, formatted_time)
                    time.sleep(random.random()*10)

