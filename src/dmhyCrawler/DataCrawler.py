# -*- coding: utf-8 -*-
import urllib

import requests
import time
from BeautifulSoup import BeautifulSoup


# 避免类型转换异常
def set_int(intNum):
    try:
        return int(intNum)
    except:
        return 0


class DmhyData(object):
    def __init__(self, *args):
        self.sendNum = '0'
        self.downNum = '0'
        self.comNum = '0'
        self.publisher = ''
        # 获取毫秒级别时间戳
        self.createTime = long(time.time() * 1000)
        if len(args) > 0:
            data = args[0];
            if data and len(data) > 9 and (isinstance(data, list) or isinstance(data, tuple)):
                self.init(data)

    def init(self, data):
        self.id = data[0]
        self.time = data[1]
        self.classi = data[2]
        self.title = data[3]
        self.magnetLink = data[4]
        self.size = data[5]
        self.sendNum = set_int(data[6])
        self.downNum = set_int(data[7])
        self.comNum = set_int(data[8])
        self.publisher = data[9]


def buildHeader():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/61.0.3163.100 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch', 'Content-Type': 'gzip',
               'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'cache-control': 'max-age=0',
               'cookie': '__cfduid=d98205d21eeda32bc056eab6376f4f0a71489391007; HstCfa3801674=1493787344743; '
                         'HstCla3801674=1493787344743; HstCmu3801674=1493787344743; HstPn3801674=1; HstPt3801674=1; '
                         'HstCnv3801674=1; HstCns3801674=1; Hm_lvt_e4918ccc327a268ee93dac21d5a7d53c=1506427818,'
                         '1506736762,1507606164,1508121182; Hm_lpvt_e4918ccc327a268ee93dac21d5a7d53c=1508122612',
               'if-modified-since': 'Mon, 16 Oct 2017 02:57:19 GMT'
               }
    return headers


def getDMHYHtml(url):
    r = requests.get(url, headers=buildHeader(), timeout=10)
    return r.text


def analysisHtml(text):
    soup = BeautifulSoup(text)
    body = soup.find('tbody')
    dmhy_datas = []
    # 统一同一批次数据插入时间
    createTime = long(time.time() * 1000)
    for tr in body.findAll("tr"):
        tds = tr.findAll("td")
        dmhy = DmhyData()
        dmhy_time = tds[0].find("span").text
        dmhy.time = dmhy_time
        classi = tds[1].find("font").text
        dmhy.classi = classi
        title = tds[2].find("a", target="_blank").text
        dmhy.title = (title)
        magnetLink = tds[3].find("a")["href"]
        dmhy.magnetLink = (magnetLink)
        size = tds[4].text
        dmhy.size = (size)
        sendNum = tds[5].find("span").text
        dmhy.sendNum = set_int(sendNum)
        downNum = tds[6].find("span").text
        dmhy.downNum = set_int(downNum)
        comNum = tds[7].text
        dmhy.comNum = set_int(comNum)
        publisher = tds[8].find("a").text
        dmhy.publisher = (publisher if publisher.strip() != ''else "")
        dmhy.createTime = createTime
        dmhy_datas.append(dmhy)
        print(
            "time:" + dmhy.time + " classi:" + dmhy.classi + " title:" + dmhy.title + " magnetLink:" + dmhy.magnetLink + " size:" + dmhy.size + " sendNum:" + str(
                dmhy.sendNum) + " downNum:" + str(dmhy.downNum) + " comNum:" + str(
                dmhy.comNum) + " publisher:" + dmhy.publisher + " createTime:" + str(
                dmhy.createTime))
    return dmhy_datas


def read_dmhy():
    page = 1
    keyword = urllib.pathname2url("")
    searchUrl = "https://share.dmhy.org/topics/list/page/%u?keyword=%s" % (1, keyword);
    text = getDMHYHtml(searchUrl)
    dmhydatas = analysisHtml(text)
    # 倒置数组，以显示最新更新
    dmhydatas.reverse()
    for data in dmhydatas:
        print (str(data.time) + ":" + data.title)


if __name__ == '__main__':
    read_dmhy()
    # from hyper import HTTPConnection
    #
    # conn = HTTPConnection('share.dmhy.org')
    # conn.request('GET', '/get', headers=buildHeader())
    # resp = conn.get_response()
    #
    # print(resp.read())
