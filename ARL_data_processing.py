import yaml
import argparse
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

def read_config(config_file):
    """
    读取配置文件，并返回配置字典。

    :param config_file: 配置文件路径
    :return: 配置字典
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"配置文件 '{config_file}' 未找到。")
    except yaml.YAMLError as e:
        print(f"配置文件 '{config_file}' 加载错误: {e}")
    except Exception as e:
        print(f"加载配置文件时发生错误: {e}")

def read_url_file(url_file):
    """
    读取URL文件，并返回域名列表。

    :param url_file: URL 文件路径
    :: 域名列表
    """
    with open(url_file, 'r', encoding='utf-8') as domains:
        domain_list = domains.readlines()
    return domain_list

def process_tasks(url, token, task_add, policy_id, domain_list, start_index):
    """
    处理普通任务和fofa任务

    :param url: API URL
    :param token: API 令牌
    :param policy_id: 策略ID
    :param domain_list: 域名列表
    :param start_index: 任务开始索引
    """
    total_domains = len(domain_list)
    if start_index < 1:
        start_index = 1
        print("输入异常, start_index 重置为 1")
    elif start_index > total_domains:
        start_index = total_domains
        print(f"输入异常, start_index 重置为 {total_domains}")

    for index in range(start_index - 1, total_domains):
        domain = domain_list[index].strip()
        if domain:
            print(f"\nProcessing Domain {index + 1}/{total_domains}: {domain}")
        if is_chinese_domain(domain):
            ascii_domain = convert_to_ascii(domain)
            if ascii_domain:
                print("转换后的 ASCII 域名:", ascii_domain)
                domain = ascii_domain

        if task_add == 'normal':
            task_add_main(url, token, domain, index + 1)
        elif task_add == 'fofa':
            task_fofa_add_main(url, token, policy_id, domain, index + 1)
        elif task_add == 'all':
            task_add_main(url, token, domain, index + 1)
            task_fofa_add_main(url, token, policy_id, domain, index + 1)

if __name__ == '__main__':
    logo()
    parser = argparse.ArgumentParser(description='选择任务')

    # 添加命令行选项
    parser.add_argument('--finger_add', action='store_true', help='执行添加指纹任务')
    parser.add_argument('--task_add', choices=['normal', 'fofa', 'all'], help='执行添加普通任务')
    parser.add_argument('--start', default=1, type=int, help='设置任务初始位置')
    parser.add_argument('--task_schedule_add', choices=['cycle', 'calm', 'all'], help='执行添加计划任务类型')
    parser.add_argument('--task_get', action='store_true', help='执行获取数据任务')
    parser.add_argument('--task_delete', action='store_true', help='执行删除任务')
    parser.add_argument('--task_schedule_delete', action='store_true', help='执行删除计划任务')
    parser.add_argument('--task_restart', action='store_true', help='执行重启任务')
    parser.add_argument('--task_custom_delete', action='store_true', help='执行自定义删除任务')
    parser.add_argument('--task_custom_restart', action='store_true', help='执行自定义重启任务')
    parser.add_argument('--config', default="config/config.yaml", help='配置文件路径')
    parser.add_argument('--finger_file', default="config/finger.json", help='配置指纹文件')
    parser.add_argument('--url_file', default="config/url.txt", help='配置目标文件')
    parser.add_argument('--task_id_file', default="config/task_id.txt", help='配置任务ID文件')
    parser.add_argument('--task_status', default='', help="任务状态筛选。示例:查询指定状态: --status waiting, 排除指定状态: --status no_done")
    args = parser.parse_args()
    
    print(f"Load config file: {args.config}")
    push_config = read_config(args.config)
    if push_config:
        if push_config.get('username') and push_config.get('password'):
            print(f"[+] Platform URL:{push_config.get('url')}")
            print(f"[+] Login username:{push_config.get('username')}, password:{push_config.get('password')}")
            login_token = arl_login_main(push_config.get('url'), push_config.get('username'), push_config.get('password'))
            if not login_token:
                print(f"[+] Token login: {push_config.get('token')}")
                token = token_verification_main(push_config.get('url'), push_config.get('token'))
            else:
                print(f"[+] Token login: {login_token}")
                token = login_token
        else:
            print(f"[+] Token login: {push_config.get('token')}")
            token = token_verification_main(push_config.get('url'), push_config.get('token'))
        
        if token:
            # 执行添加指纹任务
            if args.finger_add:
                finger_add_main(push_config.get('url'), token, args.finger_file)

            # 执行添加普通任务
            if args.task_add:
                domain_list = read_url_file(args.url_file)
                process_tasks(push_config.get('url'), token, args.task_add, push_config.get('policy_id'), domain_list, args.start)

            # 执行添加计划任务
            if args.task_schedule_add:
                domain_list = read_url_file(args.url_file) 
                task_schedule_add_main(push_config.get('url'), token, push_config.get('policy_id'), domain_list, args.task_schedule_add, args.start)

            # 执行获取任务数据
            if args.task_get:
                task_get_main(push_config.get('url'), token, args.task_status)

            # 根据任务状态删除普通或fofa任务
            if args.task_delete:
                task_items, task_data_number = get_task_ids(push_config.get('url'), token, args.task_status)
                task_delete_main(push_config.get('url'), token, task_items, task_data_number)

            # 根据任务ID删除任务
            if args.task_custom_delete:
                task_custom_delete_main(push_config.get('url'), token, args.task_id_file)

            # 执行删除计划任务
            if args.task_schedule_delete:
                task_schedule_delete_main(push_config.get('url'), token, args.task_status)

            # 根据任务状态重启任务
            if args.task_restart:
                task_items, task_data_number = get_task_ids(push_config.get('url'), token, args.task_status)
                task_restart_main(push_config.get('url'), token, task_items, task_data_number)

            # 根据任务ID重启任务
            if args.task_custom_restart:
                task_custom_restart_main(push_config.get('url'), token, args.task_id_file)
