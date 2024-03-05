import idna
from common.logo import logo
from modules.login.Arl_login import arl_login_main
from modules.login.Token_verification import token_verification_main
from modules.Fingerprint_management.finger_add import finger_add_main
from modules.task_management.add_task import task_add_main
from modules.task_management.get_task_ids import task_get_main
from modules.task_management.get_task_ids import get_task_ids
from modules.task_management.task_main_delete import task_delete_main
from modules.task_management.task_main_restart import task_restart_main
from modules.task_management.add_task_fofa import task_fofa_add_main
from modules.task_management.task_main_delete import task_custom_delete_main
from modules.task_management.task_main_restart import task_custom_restart_main
from modules.scheduled_tasks.add_task_schedule import task_schedule_add_main
from modules.scheduled_tasks.task_schedule_delete import task_schedule_delete_main

# 中文域名转ASCII
def convert_to_ascii(domain):
    try:
        ascii_domain = idna.encode(domain).decode('ascii')
        return ascii_domain
    except Exception as e:
        print("转换失败:", e)
        return None

def is_chinese_domain(domain):
    for char in domain:
        if ord(char) > 127:  # 如果字符的 ASCII 编码大于 127，则说明是非 ASCII 字符，可能是中文字符
            return True
    return False

def read_url_file(url, url_file, token):
    with open(url_file, 'r', encoding='utf-8') as domains:
        domain_list = domains.readlines()
        total_domains = len(domain_list)
    
    for index, domain in enumerate(domain_list):
        domain = domain.strip()
        # print(f"\nProcessing Domain {index+1}/{total_domains}: {domain}")

        if is_chinese_domain(domain):
            # 转换为 ASCII 格式
            ascii_domain = convert_to_ascii(domain)
            if ascii_domain:
                print("转换后的 ASCII 域名:", ascii_domain)
                domain = ascii_domain
        else:
            domain = domain
        # task_add_main(url, token, domain)                   # 添加任务
        # task_fofa_add_main(url, token, domain)              # 添加fofa任务
    
    # task_schedule_add_main(url, token, domain_list) # 添加计划任务
    

if __name__ == '__main__':

    logo()
    print("version: v0.2.3")
    # 登录获取session
    # url = "https://192.168.88.21:5003"
    # username = "admin"
    # password = "123456"
    # token = arl_login_main(url, username, password)
    token = "a464d45fd5240a1f6d9818b0b009df18"

    if token_verification_main(url, token):
        
        # print("# 添加指纹")
        # json_file = "config/finger_dev.json"
        # finger_add_main(url, json_file, token)
        
        # print("# 添加任务")
        url_file = "config/url_debug.txt"
        # url_file = "config/url_dev.txt"
        # url_file = "config/url_schedule.txt"
        # read_url_file(url, url_file, token)

        # print("# 获取任务数据")
        # task_get_main(url, token)

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