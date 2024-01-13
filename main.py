from common.logo import logo
from argparse import ArgumentParser
from modules.arl_login import arl_login_main
from modules.task_add import task_add_main
from modules.finger_add import finger_add_main
from modules.task_delete import task_delete_main
from modules.task_fofa_add import task_fofa_add_main
from modules.task_schedule_add import task_schedule_add_main
from modules.task_schedule_delete import task_schedule_delete_main

def read_url_file(url, url_file, token):
    with open(url_file, 'r', encoding='utf-8') as domains:
        domain_list = domains.readlines()
    
    total_domains = len(domain_list)
    for index, domain in enumerate(domain_list):
        domain = domain.strip()
        print(f"\nProcessing domain {index+1}/{total_domains}: {domain}")
        # task_add_main(url, token, domain)     # 添加任务
        # task_fofa_add_main(url, token, domain)    # 添加fofa任务
        # task_schedule_add_main(url, token, domain)    # 添加计划任务

if __name__ == '__main__':
    logo()
    
    url = "https://192.168.88.21:5003"
    url_file = "config/url_debug.txt"
    json_file = "config/finger_debug.json"

    # 登录获取session
    # username = "admin"
    # password = "123456"
    # token = arl_login_main(url, username, password)
    token = "dc56cb8f9167923519953d69c4c3b096"

    # 添加指纹
    # finger_add_main(url, json_file, token)
    
    # 添加任务、计划任务
    # read_url_file(url, url_file, token)

    # 删除任务、计划任务
    # task_delete_main(url, token)
    
    # 删除计划任务
    # task_schedule_delete_main(url, token)