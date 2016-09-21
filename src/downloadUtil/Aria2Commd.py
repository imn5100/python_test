# -*- coding: utf-8 -*-
import subprocess


class Aria2DownloadTool:
    def __init__(self, aria2_path):
        self.aria2_path = aria2_path

    def download(self, download_url, filename=None, dir=None):
        aria2_opts = [self.aria2_path + '/aria2c', download_url]
        if filename:
            aria2_opts.extend(('--out', filename))
        if dir:
            aria2_opts.append(('--dir ', dir))
        # 这里只负责提交下载任务使用Popen 不阻塞等待返回，实际下载进度由YAAW维护。
        exit_code = subprocess.call(aria2_opts, shell=True)
        if exit_code != 0:
            raise Exception('aria2c exited abnormally')


def openAria2RPC(aria2_path):
    subprocess.call("\"" + aria2_path + "/aria2c\"  --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all -c")


if __name__ == '__main__':
    aria2_path = "D:\\Program Files\\aria2-1.27.1"
    # download_url = "https://codeload.github.com/imn5100/autoDanime/zip/master"
    # filename = "master.zip";
    # dir = "E:/download/aria2test";
    # tool = Aria2DownloadTool(aria2_path)
    # tool.download(download_url, filename, dir);
    openAria2RPC(aria2_path)
