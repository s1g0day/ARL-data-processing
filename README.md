# ARL-data-processing
用作灯塔(ARL)上传数据、管理任务等

当前最新版本: [V2.6.1](https://github.com/TophantTechnology/ARL/releases/tag/v2.6.1)

一般官方不修改接口的话，后续版本应该是可以用的。

# 使用方法

具体使用方法还是看main.py吧，比较复杂。

## main.py部分解读
代码
```
    # 登录获取session
    url = "https://192.168.88.21:5003"
    # username = "admin"
    # password = "123456"
    # token = arl_login_main(url, username, password)
    token = "dc56cb8f9167923519953d69c4c3b096"

```
url_file 就是需要批量导入的url文件,一般为根域名。

获取token有两种，一种是自动登录获取token，另一种是手动指定，根据场景选择。

至于其他功能都是按需要解开注释使用，但fofa任务需要注意的是fofa api 请求次数过多的话就会导致当天的请求数用完。

finger_add.py使用的是： https://github.com/loecho-sec/ARL-Finger-ADD

## 添加任务

task_add.py 添加任务时默认为所有规则全开



![image](https://github.com/s1g0day/ARL-data-processing/assets/31206471/8295d5c4-8ca8-49b8-baa0-70ee7d946d4f)



![image](https://github.com/s1g0day/ARL-data-processing/assets/31206471/3e4a4105-72d4-4770-8da0-c35f330cd270)



如果想扫描部分端口的话，修改task_add.py中'port_scan_type'，将all修改为top100或top1000

```
'port_scan_type': 'top100'    #top100
'port_scan_type': 'top1000'    #top1000
'port_scan_type': 'all'    #全端口
```

## 添加计划任务

配置策略ID和任务类型(默认为定时任务)

```
# 策略ID
policy_id = "65fe317b428288ffefde56e3"    

# 周期任务： cycle  定时任务： calm
Task_Type = "calm"
```

