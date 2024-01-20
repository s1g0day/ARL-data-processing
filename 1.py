# 处理 task_get.py数据
with open("2.txt", "r", encoding="utf-8") as files:
    files = files.readlines()
    done_targets = []
    done_targets1 = []
    done_targets2 = []

    for i in files:
        task_parts = i.strip().split(', ')
        # 创建空字典
        task_dict = {}

        # 遍历任务信息部分
        for part in task_parts:
            # 分割键值对
            key, value = part.split(': ')
            # 添加到字典
            task_dict[key] = value
        # 打印字典
        if task_dict['status'] != "stop" and task_dict['status'] != "waiting" and task_dict['status'] != "done":
            done_targets.append(task_dict['id'])
            print(task_dict)
    print(len(done_targets))