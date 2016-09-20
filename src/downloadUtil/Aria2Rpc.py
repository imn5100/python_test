# -*- coding: utf-8 -*-
import requests
import os
import time
import base64


class Aria2JsonRpc(object):
    def __init__(self, rpc_url, arai2_path):
        self.rpc_url = rpc_url
        self.arai2_path = arai2_path

    def openAria2RPC(self):
        os.system("\"" + self.arai2_path + "aria2c\"  --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all -c")

    # 构造json请求头
    def buildHeader(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Content-Type'] = 'gzip'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        headers['Connection'] = 'keep-alive'
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        return headers

    def execuetJsonRpcCmd(self, method, param=None):
        payload = {"jsonrpc": "2.0", "method": method, "id": 1, "params": param}
        tm = long(time.time() * 1000)
        url = rpc_url % str(tm)
        r = requests.post(url, None, payload, headers=self.buildHeader());
        print(str(payload))
        print r.json()
        return r.status_code;

    def addUri(self, url, dir=None, out=None):
        params = [];
        download_config = {"dir": dir, "out": out}
        params.append(url);
        params.append(download_config)
        print(self.execuetJsonRpcCmd("aria2.addUri", params))

    #官方例子有BUG 暂时不用
    def addTorrent(self, path, dir=None, out=None):
        bits =  open(path).read();
        torrent = base64.b64encode(bits)
        params = [];
        download_config = {"dir": dir, "out": out}
        params.append(torrent);
        params.append([]);
        params.append(download_config)
        print(self.execuetJsonRpcCmd("aria2.addTorrent", params))


if __name__ == '__main__':
    rpc_url = "http://localhost:6800/jsonrpc?tm=%s"
    aria2_path = "D:/Program Files/aria2-1.27.1/"
    rpcClient = Aria2JsonRpc(rpc_url, aria2_path);
    # 下载链接
    download_url = ["magnet:?xt=urn:btih:JLFNIBG6IMJAIL2TXOF6GGQB3EJ2KP3V&dn=&tr=http%3A%2F%2F208.67.16.113%3A8000%2Fannounce&tr=udp%3A%2F%2F208.67.16.113%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.prq.to%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=http%3A%2F%2Ftr.bangumi.moe%3A6969%2Fannounce&tr=https%3A%2F%2Ft-115.rhcloud.com%2Fonly_for_ylbud&tr=http%3A%2F%2Fbtfile.sdo.com%3A6961%2Fannounce&tr=http%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=https%3A%2F%2Ftr.bangumi.moe%3A9696%2Fannounce&tr=http%3A%2F%2Fmgtracker.org%3A2710%2Fannounce&tr=http%3A%2F%2Ft.acg.rip%3A6699%2Fannounce&tr=http%3A%2F%2Fshare.camoe.cn%3A8080%2Fannounce&tr=http%3A%2F%2Fopen.nyaatorrents.info%3A6544%2Fannounce&tr=http%3A%2F%2Ftracker.tfile.me%2Fannounce&tr=http%3A%2F%2Fpubt.net%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=http%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.skyts.net%3A6969%2Fannounce&tr=http%3A%2F%2Ft.nyaatracker.com%2Fannounce&tr=http%3A%2F%2Ftorrentsmd.com%3A8080%2Fannounce&tr=http%3A%2F%2Fretracker.krs-ix.ru%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"]
    rpcClient.addUri(download_url, "E:/download/aria2test");
    # rpcClient.addTorrent("E:/download/code11.torrent", "E:/download/aria2test", "torrenttest");
