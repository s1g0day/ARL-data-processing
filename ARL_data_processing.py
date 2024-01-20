from common.logo import logo
from argparse import ArgumentParser
from modules.login.Arl_login import arl_login_main
from modules.login.Token_verification import token_verification_main
from modules.Fingerprint_management.finger_add import finger_add_main
from modules.task_management.add_task import task_add_main
from modules.task_management.task_get import task_get_main
from modules.task_management.task_main_delete import task_delete_main
from modules.task_management.task_main_restart import task_restart_main
from modules.task_management.add_task_fofa import task_fofa_add_main
from modules.task_management.task_main_delete import task_custom_delete_main
from modules.task_management.task_main_restart import task_custom_restart_main
from modules.scheduled_tasks.task_schedule_add import task_schedule_add_main
from modules.scheduled_tasks.task_schedule_delete import task_schedule_delete_main

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

    # 登录获取session
    url = "https://192.168.88.21:5003"
    # username = "admin"
    # password = "123456"
    # token = arl_login_main(url, username, password)
    token = "4cecadff75a525dc965612f729fbca3c"

    if token_verification_main(url, token):

        # print("# 获取任务数据")
        # task_get_main(url, token)

        # print("# 添加指纹")
        # json_file = "config/finger_debug.json"
        # finger_add_main(url, json_file, token)
        
        # print("# 添加任务、计划任务")
        # url_file = "config/url_debug.txt"
        # read_url_file(url, url_file, token)

        # print("# 删除任务")
        # task_delete_main(url, token)

        # print("# 删除计划任务")
        # task_schedule_delete_main(url, token)

        # print("# 重启任务")
        # task_restart_main(url, token) 
        
        # print("# 停止任务")
        # task_delete_main(url, token)

        # id_file = "config/task_id_debug.txt"
        # print("# 自定义删除任务")
        # task_custom_delete_main(url, id_file, token)

        # print("# 自定义重启任务")
        # task_custom_restart_main(url, id_file, token)
        