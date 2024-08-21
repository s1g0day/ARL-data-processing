from common.logo import logo
from common.convert_to_ascii import convert_to_ascii, is_chinese_domain
from modules.login.Arl_login import arl_login_main, token_verification_main
from modules.Fingerprint_management.finger_add import finger_add_main
from modules.task_management.add_task import task_add_main
from modules.task_management.get_task_ids import get_task_ids, task_get_main
from modules.task_management.task_main_delete import task_delete_main
from modules.task_management.task_main_restart import task_restart_main
from modules.task_management.add_task_fofa import task_fofa_add_main
from modules.task_management.task_main_delete import task_custom_delete_main
from modules.task_management.task_main_restart import task_custom_restart_main
from modules.scheduled_tasks.add_task_schedule import task_schedule_add_main
from modules.scheduled_tasks.task_schedule_delete import task_schedule_delete_main

def read_url_file(url, url_file, token, start_index):

    with open(url_file, 'r', encoding='utf-8') as domains:
        domain_list = domains.readlines()
        total_domains = len(domain_list)
    if start_index < 1:
        start_index = 1
        print("输入异常, start_index 重置为 1")
    elif start_index > total_domains:
        start_index = total_domains
        print(f"输入异常, start_index 重置为 {total_domains}")

    for index in range(start_index-1, total_domains):
        domain = domain_list[index].strip()
        if domain:
            print(f"\nProcessing Domain {index+1}/{total_domains}: {domain}")
        if is_chinese_domain(domain):
            # 转换为 ASCII 格式
            ascii_domain = convert_to_ascii(domain)
            if ascii_domain:
                print("转换后的 ASCII 域名:", ascii_domain)
                domain = ascii_domain
        else:
            domain = domain
        task_add_main(url, token, domain)                   # 添加任务
        # task_fofa_add_main(url, token, domain)              # 添加fofa任务
    
    # 周期任务： cycle  定时任务： calm
    # Task_Type = "calm"
    # 策略ID
    # policy_id = "65fe317b428288ffefde56e3"    
    # task_schedule_add_main(url, token, policy_id, domain_list, Task_Type, start_index) # 添加计划任务
    

if __name__ == '__main__':

    logo()
    # 登录获取session
    url = "https://192.168.88.21:5003"
    # username = "admin"
    # password = "123456"
    # token = arl_login_main(url, username, password)
    token = "dc56cb8f9167923519953d69c4c3b096"

    if token_verification_main(url, token):
        
        # print("# 添加指纹")
        # json_file = "config/finger_dev.json"
        # finger_add_main(url, json_file, token)
        
        # print("# 添加任务")
        # url_file = "config/1.txt"
        # start = 1   # 初始为 1
        # read_url_file(url, url_file, token, start)

        print("# 获取任务数据")
        task_get_main(url, token)
        # task_items, datas = get_task_ids(url, token)

        # print("# 删除任务")
        # task_delete_main(url, token, task_items, datas)

        # print("# 删除计划任务")
        # task_schedule_delete_main(url, token)

        # print("# 重启任务")
        # task_restart_main(url, token, task_items, datas) 
   
        # id_file = "config/task_id_debug.txt"
        # print("# 自定义删除任务")
        # task_custom_delete_main(url, id_file, token)

        # print("# 自定义重启任务")
        # task_custom_restart_main(url, id_file, token)