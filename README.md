# ARL-data-processing
用作灯塔(ARL)上传数据、管理任务等

灯塔项目地址: [adysec 备份项目](https://github.com/adysec/ARL)

> 注: 二开项目不修改接口的话，是可以通用的。

# 使用方法

## 配置

将`config\config.yaml.debug`重命名为`config\config.yaml`

```
url: "https://127.0.0.1:5003/"
username: ""
password: ""
token: "xxxxx"
```
获取token的方法有两种:

- 登录获取token。可以添加新用户用于脚本使用，同一个账户无法同时登录。

  ```
  docker exec -ti arl_mongodb mongo -u admin -p admin
  use arl
  db.user.insert({ username: 'process',  password: hex_md5('arlsalt!@#'+'admin123') })
  db.user.find()
  ```

- 指定token。每次使用都需要从浏览器提取登录后的token，推荐用上面的方法。

验证

```
# 登录获取token
> python3 ARL_data_processing.py

 ____  _        ___  ____              
/ ___|/ | __ _ / _ \|  _ \  __ _ _   _ 
\___ \| |/ _` | | | | | | |/ _` | | | |
 ___) | | (_| | |_| | |_| | (_| | |_| |
|____/|_|\__, |\___/|____/ \__,_|\__, |
         |___/                   |___/ 
                                       
Powered by S1g0Day
--------------------------------------
    
Load config file: config/config.yaml
[+] Platform URL:https://127.0.0.1:5003/
[+] Login username:admin, password:admin123
[+] Login Success!
[+] Token login: e3d5cd8836ab1a7d9bb8d17964d5d0ae
```



## 添加指纹

```
# 指纹信息
config/finger.json

代码参考：https://github.com/loecho-sec/ARL-Finger-ADD
```

```
使用默认指纹文件
python3 ARL_data_processing.py --finger_add

指定指纹文件
python3 ARL_data_processing.py --finger_add --finger_file config/finger.json
```



符合ARL格式的数据：https://github.com/adysec/ARL/blob/master/tools/%E6%8C%87%E7%BA%B9%E6%95%B0%E6%8D%AE.json

```
# finger_arl_file = "config/finger_arl.yaml"
# finger_update_data(url, finger_arl_file, token)
```



adysec项目

```
# 改指纹，/opt/ARL/tools/指纹数据.json
docker exec -it arl bash
cd /opt/ARL
python3.6 tools/add_finger.py
python3.6 tools/add_finger_ehole.py
```

## 添加普通任务

`add_task.py` 添加任务时默认为所有规则全开

```
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
```

如果想扫描部分端口的话，修改`add_task.py`中`port_scan_type`，将all修改为top100或top1000

```
'port_scan_type': 'top100'    #top100
'port_scan_type': 'top1000'    #top1000
'port_scan_type': 'all'    #全端口
```

普通任务

```
# 导入的url文件, 一般为根域名
config/url.txt

# 添加普通任务
python3 .\ARL_data_processing.py --task_add normal
```

fofa任务

```
# 策略ID
policy_id: "xxxxxx"

# 添加fofa任务，添加fofa任务需要注意，如果fofa api 请求次数过多的话就会导致当天的请求数用完。所以量少可以推荐使用
python3 .\ARL_data_processing.py --task_add fofa
```

```
# 两个都添加
python3 .\ARL_data_processing.py --task_add all

# 指定url文件
python3 .\ARL_data_processing.py --task_add normal --url_file config/url.txt
```

如果意外断开的话，可以通过指定开始位置进行添加

```
# 添加任务结果输出
Processing Domain 3/10: {test.com}
Domain:test.com, Add_task_status:success

如果Add_task_status为success，则从第四个开始
python3 .\ARL_data_processing.py --task_add normal --start 4
如果没有这条就从第三个开始
python3 .\ARL_data_processing.py --task_add normal --start 3
```

## 添加计划任务

```
# 策略ID
policy_id: "xxxxxx"
```

验证

```
使用默认配置文件
config/url.txt

# 添加周期任务
python3 .\ARL_data_processing.py --task_schedule_add cycle

# 添加定时任务
python3 .\ARL_data_processing.py --task_schedule_add calm

# 两个都添加
python3 .\ARL_data_processing.py --task_schedule_add all

# 指定url文件
python3 .\ARL_data_processing.py --task_schedule_add cycle --url_file config/url.txt
```

如果意外断开的话，可以通过指定开始位置进行添加

```
python3 .\ARL_data_processing.py --task_schedule_add cycle --start 4
```

## 获取任务数据

```
# 获取所有任务数据，任务状态默认为空
python3 .\ARL_data_processing.py --task_get

# 获取所有状态为done的任务数据
python3 .\ARL_data_processing.py --task_get --task_status done
```

## 删除普通或fofa任务数据

根据任务状态删除任务

```
# 删除所有任务
python3 .\ARL_data_processing.py --task_delete

# 删除所有状态为done的任务
python3 .\ARL_data_processing.py --task_delete --task_status done
```

根据任务ID删除任务

```
# 任务ID
config/task_id.txt

# 使用默认配置文件
python3 .\ARL_data_processing.py --task_custom_delete

# 使用指定配置文件
python3 .\ARL_data_processing.py --task_custom_delete --task_id_file config/task_id.txt
```

## 删除计划任务

```
# 删除所有任务
python3 .\ARL_data_processing.py --task_schedule_delete

# 删除所有状态为done的任务
python3 .\ARL_data_processing.py --task_schedule_delete --task_status done
```

## 重启任务

```
# 重启所有任务
python3 .\ARL_data_processing.py --task_restart

# 重启所有状态为done的任务
python3 .\ARL_data_processing.py --task_restart --task_status done
```

根据任务ID重启任务

```
# 任务ID
config/task_id.txt

# 使用默认配置文件
python3 .\ARL_data_processing.py --task_custom_restart

# 使用指定配置文件
python3 .\ARL_data_processing.py --task_custom_restart --task_id_file config/task_id.txt
```

# 贡献与支持

如果本项目对你有用，还请star鼓励一下。

无论是添加新功能、改进代码、修复BUG或提供文档。请通过GitHub的Issue和Pull Request提交您的贡献，我会尽快给予帮助及更新。