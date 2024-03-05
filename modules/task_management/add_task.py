import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 添加任务
def task_add_main(url, token, domain):

    json_data = {
        'name': domain + "_task",
        'target': domain,
        'domain_brute_type': 'big',
        'port_scan_type': 'all',
        'domain_brute': True,
        'alt_dns': True,
        'dns_query_plugin': True,
        'arl_search': True,
        'port_scan': True,
        'service_detection': True,
        'os_detection': True,
        'ssl_cert': True,
        'skip_scan_cdn_ip': True,
        'site_identify': True,
        'search_engines': True,
        'site_spider': True,
        'site_capture': True,
        'file_leak': True,
        'findvhost': True,
        'nuclei_scan': True,
        'web_info_hunter': True,
    }

    response = requests.post(url + '/api/task/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    data = json.loads(response.text)
    print(f"Domain:{domain}, Add_task_status:{data['message']}")
