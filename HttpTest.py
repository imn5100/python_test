# -*- coding=utf-8 -*-
import json

import requests
import sys


def get_avg(name, params):
    if params and len(params) > 1 and name in params and (params.index(name) + 1) < len(params):
        return params[params.index(name) + 1]
    return None


if __name__ == '__main__':
    args = sys.argv
    method = 'get'
    if args and '-post' in args:
        method = 'post'
    url = get_avg('-url', args)
    if url and url.startswith('http'):
        data = get_avg('-data', args)
        print(url)
        print('*' * 10)
        print(data)
        print('*' * 10)
        if data:
            data = json.loads(data)
        else:
            data = {}
        response = requests.request(method, url, data=data)
        print(response.status_code)
        print(response.text)
    else:
        print("error url")
