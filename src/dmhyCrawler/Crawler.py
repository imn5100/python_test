# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import redis
import single_conn
from DmhyDataOperator import *
import DbOperator
import time
import urllib

MAGNET_QUEUE = "Magnet_Queue"
DOWNLOAD_START = "Download_Start_%s"
DMHY_MAP_TITLES_MAGNET = "DMHY_Map_Titles_Magnet"


# 这里http请求存在超时问题。10秒 如果url无响应，则抛出timeout异常。（不包括响应的时间）
def getDMHYHtml(url):
    r = requests.get(url, headers=buildHeader(), timeout=10)
    return r.text


def buildHeader():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Content-Type'] = 'gzip'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'gzip'
    headers['Host'] = 'share.dmhy.org'
    headers['referer'] = 'http://share.dmhy.org'
    headers[
        'Cookie'] = '__cfduid=d1a9b70e02b3116c622b3747893a44ef81472616279; Hm_lvt_e4918ccc327a268ee93dac21d5a7d53c=1472616271,1472692420,1472779166,1472803144; Hm_lpvt_e4918ccc327a268ee93dac21d5a7d53c=1472803144'
    return headers


def analysisHtml(text):
    soup = BeautifulSoup(text)
    body = soup.find('tbody')
    dmhy_datas = []
    #统一同一批次数据插入时间
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
        dmhy.sendNum = (sendNum if sendNum.strip() != '' else '0')
        downNum = tds[6].find("span").text
        dmhy.downNum = (downNum if downNum.strip() != '' else '0')
        comNum = tds[7].text
        dmhy.comNum = (comNum if comNum.strip() != '' else '0')
        publisher = tds[8].find("a").text
        dmhy.publisher = (publisher if publisher.strip() != ''else "")
        dmhy.createTime = createTime
        dmhy_datas.append(dmhy)
        print(
            "time:" + dmhy.time + " classi:" + dmhy.classi + " title:" + dmhy.title + " magnetLink:" + dmhy.magnetLink + " size:" + dmhy.size + " sendNum:" + dmhy.sendNum + " downNum:" + dmhy.downNum + " comNum:" + dmhy.comNum + " publisher:" + dmhy.publisher + " createTime:" + str(
                    dmhy.createTime))
    return dmhy_datas


def filter_datas(dmhy_datas):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    add_list = []
    update_list = []
    add_map = {}
    for data in dmhy_datas:
        if r.hexists(DMHY_MAP_TITLES_MAGNET, data.title):
            update_list.append(data)
        else:
            add_list.append(data)
            add_map[data.title] = data.magnetLink
    return {"add_list": add_list, "update_list": update_list, "add_map": add_map}


if __name__ == '__main__':
    page=1
    keyword=urllib.pathname2url("")
    searchUrl = "http://share.dmhy.org/topics/list/page/%u?keyword=%s" % (1, keyword);
    text = getDMHYHtml(searchUrl)
    dmhydatas = analysisHtml(text)
    db = DbOperator.DatabaseConnection("127.0.0.1", user="root", passwd='xlsw', db='test')
    dmop = DmhyDataOperator(db)
    data_map = filter_datas(dmhydatas)
    update_count = 0
    for data in data_map["update_list"]:
        db_data = dmop.get_one_bytitle(data.title)
        if db_data:
            db_data.magnetLink = data.magnetLink
            db_data.comNum = data.comNum
            db_data.downNum = data.downNum
            db_data.sendNum = data.sendNum
            db_data.size = data.size
            if dmop.update(db_data): update_count = update_count + 1
    print ("update:" + str(update_count))
    if data_map["add_map"]:
        if single_conn.HMSET(DMHY_MAP_TITLES_MAGNET, data_map["add_map"]):
            dmop.add_dmhydata_list(data_map["add_list"])
