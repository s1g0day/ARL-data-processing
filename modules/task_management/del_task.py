import json
import urllib3
import requests
from common.arl_headers import arl_headers_main
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 删除任务
def task_delete(url, json_data, token):
    # 追加 "del_task_data" 到 "json_data" 字典中
    json_data.update({'del_task_data': True})

    task_delete_response = requests.post(url + '/api/task/delete/', json=json_data, headers=arl_headers_main(url,token), verify=False, timeout=(4,20))
    task_delete_data = json.loads(task_delete_response.text)
    print(f"Delete_status:{task_delete_data['message']}")

# 先处理json_data数据,然后再删除
def del_task_main(url, json_data, token):
    
    chunk_size = 500
    # 将字典对象转换回 JSON 字符串
    result_json_str = json.dumps(json_data)
    # 将字符串解析为字典对象
    data = json.loads(result_json_str)

    # 如果 result_json_str 的长度小于等于 chunk_size，则不进行拆分
    if len(data['task_id']) <= chunk_size:
        # 创建一个新的字典对象，只包含 "task_id" 键和原始值
        chunk_data = {"task_id": data['task_id']}
        # 调用任务删除函数
        task_delete(url, chunk_data, token)
    else:
        # 拆分 JSON 数据
        chunks = [list(data['task_id'][i:i+chunk_size]) for i in range(0, len(data['task_id']), chunk_size)]
        total_chunks = len(chunks)

        # 处理每个部分
        for i, chunk in enumerate(chunks):
            # 创建一个新的字典对象，只包含 "task_id" 键和当前部分的值
            chunk_data = {"task_id": chunk}
            task_delete(url, json_data, token)

            # 显示进度信息
            progress = (i + 1) / total_chunks * 100
            print("Progress: {:.2f}%".format(progress))