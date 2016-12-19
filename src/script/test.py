# -*- coding=utf-8 -*-
import codecs
import hashlib
import json
import os
import subprocess

import requests

from Aria2Rpc import Aria2JsonRpc

user_data = {"username": "*", "password": "*"}
STATUS_MAP = {
    "init": 1,
    "start": 2,
    "over": 3,
    "fail": 4,
}
# 脚本登录接口，ip必须为白名单ip
remote_login_url = "https://shawblog.me/blogger/script/login.do"
# 获取任务消息 200 成功有数据返回 201成功但无数据  1001 传参为空或格式错误 600因为异常操作失败
consumer_url = "https://shawblog.me/admin/remote/consumerMsg.do"
# id 操作的任务数据主键  type 1-4 重新启用任务 开启任务 完成任务 任务失败 默认为开启任务
callback_url = "https://shawblog.me/admin/remote/callBackMsg.do"  # 需要传递md5密码


def md5lower(str):
    md5c = hashlib.md5()
    md5c.update(str)
    return md5c.hexdigest().lower()


def get_aria2_client():
    rpc_url = "http://localhost:6800/jsonrpc?tm=%s"
    aria2_path = "D:/Program Files/aria2-1.27.1/"
    return Aria2JsonRpc(rpc_url, aria2_path)


def auth(user_data):
    user_data["password"] = md5lower(user_data["password"])
    s = requests.Session()
    r = s.post(remote_login_url, user_data, timeout=5)
    if r.text == "200":
        return s
    else:
        print(r.text)
        return None


def download(msg_data):
    if msg_data:
        resultobj = json.loads(msg_data)
        if resultobj["code"] == 200:
            url = resultobj["data"]["contents"]
            get_aria2_client().addUris([url], "E:/download/")
            return resultobj["data"]["id"]
        else:
            print(resultobj)
            return None


def test_download():
    s = auth(user_data)
    msg_data = s.get(consumer_url, params={"topic": "download"})
    msg_id = download(msg_data.text)
    if msg_id:
        s.get(callback_url, params={"id": msg_id, "type": STATUS_MAP["over"]})


def build_file(resultobj):
    if resultobj["code"] == 200:
        contents = resultobj["data"]["contents"]
        filename = "exctmp/python_%s.py" % resultobj["data"]["id"]
        exc_file = codecs.open(filename, "w", encoding='utf-8')
        exc_file.write(contents)
        exc_file.close()
        return filename
    else:
        print(resultobj)
        return None


def test_python():
    s = auth(user_data)
    msg_data = s.get(consumer_url, params={"topic": "python"})
    try:
        resultobj = json.loads(msg_data.text)
        filename = build_file(resultobj)
        if filename:
            file_path = os.path.abspath(filename)
            subprocess.call("python " + file_path)
            s.get(callback_url, params={"id": resultobj["data"]["id"], "type": STATUS_MAP["over"]})
    except Exception, e:
        print(e)
        s.get(callback_url, params={"id": resultobj["data"]["id"], "type": STATUS_MAP["fail"]})


if __name__ == '__main__':
    test_python()
