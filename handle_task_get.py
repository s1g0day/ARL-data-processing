# 处理 task_get.py数据
# 1.txt格式
'''
id:65e5946a59963c71160bcc6c, status:done, name:test.com_task, targets:test.com
id:65e5946a52c2692663ea2c08, status:done, name:test.com_task, targets:test.com
id:65e5946959963c71160bcc6b, status:done, name:test.top_task, targets:test.top
'''

with open("1.txt", "r", encoding="utf-8") as files:
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
            key, value = part.split(':')
            # 添加到字典
            task_dict[key] = value
        # 打印字典
        if task_dict['status'] == "done":
            done_targets.append(task_dict['id'].strip())
            if task_dict['targets'].strip() and task_dict['targets'].strip() not in done_targets1:
                done_targets1.append(task_dict['targets'].strip())
                print(task_dict['targets'].strip())
            else:
                done_targets2.append(task_dict['id'].strip())
    print(len(done_targets))
    print(len(done_targets1))
    # print(len(done_targets2))