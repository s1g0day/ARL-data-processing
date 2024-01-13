# ARL-data-processing
用作灯塔(ARL)上传数据、管理任务等

当前最新版本: [V2.6.1](https://github.com/TophantTechnology/ARL/releases/tag/v2.6.1)

一般官方不修改接口的话，后续版本应该是可以用的。

# 使用方法

具体使用方法还是看main.py吧，比较复杂。

## main.py部分解读
代码
```
    url = "https://192.168.88.21:5003"
    url_file = "config/url_debug.txt"
    json_file = "config/finger_debug.json"

    # 登录获取session
    # username = "admin"
    # password = "123456"
    # token = arl_login_main(url, username, password)
    token = "dc56cb8f9167923519953d69c4c3b096"

```
url_file 就是需要批量导入的url文件,一般为根域名。

获取token有两种，一种是自动登录获取token，另一种是手动指定，根据场景选择。

至于其他功能都是按需要解开注释使用，但fofa任务需要注意的是fofa api 请求次数过多的话就会导致当天的请求数用完。

finger_add.py使用的是： https://github.com/loecho-sec/ARL-Finger-ADD
