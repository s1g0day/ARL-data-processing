import json
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def finger_add_main(url, json_file, token):
    f = open(json_file,'r', encoding="utf-8")
    content =f.read()
    load_dict = json.loads(content)
        #dump_dict = json.dump(f)

    body = "body=\"{}\""
    title = "title=\"{}\""
    hash = "icon_hash=\"{}\""

    for i in load_dict['fingerprint']:
        finger_json =  json.loads(json.dumps(i))
        if finger_json['method'] == "keyword" and finger_json['location'] == "body":
            name = finger_json['cms']
            if len(finger_json['keyword']) > 0:
                for rule in finger_json['keyword']:
                    rule = body.format(rule)
                else:
                    rule = body.format(finger_json['keyword'][0])
                add_Finger(name, rule, url, token)

        elif finger_json['method'] == "keyword" and finger_json['location'] == "title":
            name = finger_json['cms']

            if len(finger_json['keyword']) > 0:
                for rule in finger_json['keyword']:
                    rule = title.format(rule)
                else:
                    rule = title.format(finger_json['keyword'][0])
                add_Finger(name, rule, url, token)
        else:
            name = finger_json['cms']
            if len(finger_json['keyword']) > 0:
                for rule in finger_json['keyword']:
                    rule = hash.format(rule)
                else:
                    rule = hash.format(finger_json['keyword'][0])
                add_Finger(name, rule, url, token)

def add_Finger(name, rule, url, token):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Connection": "close",
        "Token": "{}".format(token),
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json; charset=UTF-8"
    }
    url = "{}/api/fingerprint/".format(url)
    data = {"name" : name,"human_rule": rule}
    data_json = json.dumps(data)

    try:
        response = requests.post(url, data=data_json, headers=headers, verify=False)
        if response.status_code == 200:
            print(f'Add:{data_json}\nRsp:{response.text}')
    except Exception as e:
        print(e)

