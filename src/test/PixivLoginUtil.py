# -*- coding=utf-8 -*-
import getpass

import requests
import re

pixiv_url_login = "https://accounts.pixiv.net/login"
pixiv_url_login_post = 'https://accounts.pixiv.net/api/login'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'accounts.pixiv.net',
    'Referer': 'http://www.pixiv.net/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'
}


# 获取pixiv登录时需要的post__key
# 正则搜索网页中的input <input type="hidden" name="post_key" value="***">
def get_postkey(content):
    if content:
        postkey_str = re.search('name="post_key" value="\w*"', content)
        if postkey_str:
            # 匹配的字符串使用 " 分割后为['name=', 'post_key', ' value=', '***', '']
            return postkey_str.group().split('"')[-2]
    else:
        return None


def login(username, password):
    s = requests.session()
    r = s.get(pixiv_url_login, headers=headers)
    if r.ok:
        post_key = get_postkey(r.content)
        if post_key:
            post_data = {
                'pixiv_id': username,
                'password': password,
                'post_key': post_key,
                'source': 'accounts'
            }
        s.post(pixiv_url_login_post, data=post_data, headers=headers)
        print(s.cookies)
        return s
    else:
        print('get post_key error')


if __name__ == '__main__':
    print(login("username", "password"))
