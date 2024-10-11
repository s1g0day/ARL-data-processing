# 删除任务
from modules.task_management.stop_task import task_stop_main
from modules.task_management.del_task import del_task_main

# 根据任务状态
def task_delete_main(url, token, task_items, task_data_number):
    json_data = {
        "task_id": [
        ],
    }
    for index, task in enumerate(task_items):
        task_id = task["_id"]
        # print(f"Progress of:{index + 1}/{task_data_number}, id:{task_id}, Status:{task['status']}")
        json_data["task_id"].append(task_id)    # 追加字符到'_id'键对应的列表中
    '''
    删除任务时需要先停止，在删除
    '''
    # 停止
    task_stop_main(url, json_data, token)
    # 删除
    del_task_main(url, json_data, token)

# 根据任务ID删除
def task_custom_delete_main(url, delete_id_file, token):
    with open(delete_id_file, "r", encoding="utf-8") as files:
        files = files.readlines()
        for i in files:
            json_data = {
                'task_id': [
                ],
            }
            aaa = i.strip()
            json_data['task_id'].append(aaa) 
            # 停止
            task_stop_main(url, json_data, token)
            # 删除
            del_task_main(url, json_data, token)
