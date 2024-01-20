# 重启任务
from modules.task_management.get_task_ids import get_task_ids
from modules.task_management.restart_task import restart_task_main
from modules.task_management.del_task import del_task_main

# 这种是先获取所有需要删除的id，然后统一重启。
def task_restart_main(url, token):
    task_items, datas = get_task_ids(url, token)
    json_data = {
        "task_id": [
        ],
    }
    for index, task in enumerate(task_items):
        # if task['status'] != "done" and task['status'] != "stop":
        if task['status'] == "stop":
            task_id = task["_id"]
            # print(f"第{index + 1}/{datas}个任务调度 id: {task_id}, 状态为{task['status']}")
            json_data["task_id"].append(task_id)    # 追加字符到'_id'键对应的列表中
    '''
    重启任务时会创建新任务，因此需要先重启，然后删除原任务
    '''
    
    # 重启
    restart_task_main(url, json_data, token)
    # 删除
    del_task_main(url, json_data, token)

# 根据自定义id 进行重启
def task_custom_restart_main(url, restart_id_file, token):

    with open(restart_id_file, "r", encoding="utf-8") as files:
        files = files.readlines()
        for i in files:
            json_data = {
                'task_id': [
                ],
            }
            aaa = i.strip()
            json_data['task_id'].append(aaa) 
            # print(json_data)
            # 重启
            restart_task_main(url, json_data, token)
            # 删除
            del_task_main(url, json_data, token)