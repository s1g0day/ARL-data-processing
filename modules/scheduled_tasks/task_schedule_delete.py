from modules.scheduled_tasks.get_task_schedule_id import get_task_schedule_id_main
from modules.scheduled_tasks.del_task_schedule import del_task_schedule_main
from modules.scheduled_tasks.stop_task_schedule import stop_task_schedule_main

# 删除计划任务
def task_schedule_delete_main(url, token, status):
    task_schedule_ids, datas = get_task_schedule_id_main(url, token, status)
    json_data = {
        '_id': [
        ],
    }
    for index, task_schedule in enumerate(task_schedule_ids):
        task_schedule_id = task_schedule["_id"]
        # 追加字符到'_id'键对应的列表中
        json_data['_id'].append(task_schedule_id)

    stop_task_schedule_main(url, json_data, token)
    del_task_schedule_main(url, json_data, token)