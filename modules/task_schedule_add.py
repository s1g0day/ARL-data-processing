# 添加ARL计划任务
import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 定时任务
def task_schedule_add_main(url, token, domain):
    # 在每5天的0点10分执行任务 资产发现任务
    task_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'recurrent_scan',
        'policy_id': '658e21403ad7ec59a44fc30a',
        'cron': '10 0 */5 * *',
        'task_tag': 'task',
    }
    # 在每5天的12点10分执行任务 风险巡航任务
    risk_cruising_json_data = {
        'name': domain,
        'target': domain,
        'schedule_type': 'recurrent_scan',
        'policy_id': '658e21403ad7ec59a44fc30a',
        'cron': '10 12 */5 * *',
        'task_tag': 'risk_cruising',
    }

    task_response = requests.post(url + '/api/task_schedule/', json=task_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    risk_cruising_response = requests.post(url + '/api/task_schedule/', json=risk_cruising_json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_data = json.loads(task_response.text)
    risk_cruising_data = json.loads(risk_cruising_response.text)
    print(domain + "_资产发现任务添加任务状态: " + task_data['message'])
    print(domain + "_风险巡航任务添加任务状态: " + risk_cruising_data['message'])

