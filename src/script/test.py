# -*- coding=utf-8 -*-

import requests
import hashlib

data = {"username": "shaw", "password": "**"}


def md5lower(str):
    md5c = hashlib.md5()
    md5c.update(str)
    return md5c.hexdigest().lower()


if __name__ == '__main__':
    url = "http://localhost:8099/blogger/script/login.do"
    url2 = "http://localhost:8099/admin/remote/consumerMsg.do"
    data["password"] = md5lower(data["password"])
    s = requests.Session()
    r = s.post(url, data)
    print(r.text)
    main_page = s.get(url2, params={"topic": "download"})
    print(main_page.text)
