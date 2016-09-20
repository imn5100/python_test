# -*- coding: utf-8 -*-
import os
import subprocess


class Aria2DownloadTool:
    def __init__(self, **kwargs):
        self.gdriveid = str(kwargs['client'].get_gdriveid())
        self.url = kwargs['url']
        self.path = kwargs['path']
        self.size = kwargs['size']
        self.resuming = kwargs.get('resuming')

    def finished(self):
        assert os.path.getsize(self.path) <= self.size, 'existing file (%s) bigger than expected (%s)' % (
            os.path.getsize(self.path), self.size)
        return os.path.getsize(self.path) == self.size and not os.path.exists(self.path + '.aria2')

    def __call__(self):
        gdriveid = self.gdriveid
        download_url = self.url
        path = self.path
        resuming = self.resuming
        dir = os.path.dirname(path)
        filename = os.path.basename(path)
        aria2_opts = ['aria2c', '--header=Cookie: gdriveid=' + gdriveid, download_url, '--out', filename,
                      '--file-allocation=none']
        if dir:
            aria2_opts.extend(('--dir', dir))
        if resuming:
            aria2_opts.append('-c')
        exit_code = subprocess.call(aria2_opts)
        if exit_code != 0:
            raise Exception('aria2c exited abnormally')


def openAria2RPC(aria2_path):
    subprocess.call("\"" + aria2_path + "/aria2c\"  --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all -c")


if __name__ == '__main__':
    aria2_path = "D:\\Program Files\\aria2-1.27.1"
    download_url = "https://codeload.github.com/imn5100/autoDanime/zip/master"
    filename = "master.zip";
    dir = "E:/download/aria2test";
    subprocess.Popen(["D:\\Program Files\\aria2-1.27.1\\aria2c", download_url, "--out", filename, "--dir", dir],
                     shell=True)
