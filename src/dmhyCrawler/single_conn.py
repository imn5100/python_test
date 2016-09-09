# -*- coding: utf-8 -*-
import redis
from redis._compat import iteritems


# 下载脚本运行时间较长，无法快速返回请求的redis连接。所以这里提供 单连接操作redis 执行一次命令获得一次连接 并在执行后立即返回。
# 正常使用redis应使用 # r = redis.StrictRedis(host='localhost', port=6379, db=0)
def execute_low_level(command, *args, **kwargs):
    connection = redis.Connection(**kwargs)
    try:
        connection.connect()
        connection.send_command(command, *args)
        response = connection.read_response()
        if command in redis.Redis.RESPONSE_CALLBACKS:
            return redis.Redis.RESPONSE_CALLBACKS[command](response)
        return response
    finally:
        connection.disconnect()
        del connection


host = '127.0.0.1'
port = 6379


def SET(key, value):
    return execute_low_level("LPUSH", key, value, host=host, port=port)


def LPUSH(lkey, value):
    return execute_low_level("LPUSH", lkey, value, host=host, port=port)


def LREM(lkey, value):
    return execute_low_level("LREM", lkey, 1, value, host=host, port=port)


def RPOPLPUSH(popKey, pushKey):
    jstr = execute_low_level("RPOPLPUSH", popKey, pushKey, host=host, port=port)
    return jstr


def HEXISTS(key, field):
    resp = execute_low_level("HEXISTS", key, field, host=host, port=port)
    if resp == 1 or resp == "1":
        return True
    else:
        return False


def HMSET(name, mapping):
    if not mapping:
        return False
    items = []
    for pair in iteritems(mapping):
        items.extend(pair)
    return execute_low_level("HMSET", name, *items, host=host, port=port)


def HGET(key, field):
    resp = execute_low_level("HEXISTS", key, field, host=host, port=port)
    return resp


def EXPIRE(key, senconds):
    return execute_low_level("EXPIRE", key, senconds, host=host, port=port)


def EXPIREAT(key, timestamp):
    return execute_low_level("EXPIREAT", key, timestamp, host=host, port=port)


# test
if __name__ == '__main__':
    data = {"google": "www.google.com", "yahoo": "www.yahoo.com", "bing": "www.bing.com"}
    HMSET("site2", data)
