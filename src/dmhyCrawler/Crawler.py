# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from src.dmhyCrawler.DbOperator import DatabaseConnection
from src.dmhyCrawler.DmhyDataOperator import DmhyDataOperator
from src.dmhyCrawler.DmhyDataOperator import DmhyData


# 这里http请求存在超时问题。10秒 如果url无响应，则抛出timeout异常。（不包括响应的时间）
def getDMHYHtml(url):
    r = requests.get(url, headers=buildHeader(), timeout=10);
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
    for tr in body.findAll("tr"):
        tds = tr.findAll("td")
        dmhy = [""]
        time = tds[0].find("span").text
        dmhy.append(time)
        classi = tds[1].find("font").text
        dmhy.append(classi)
        title = tds[2].find("a", target="_blank").text
        dmhy.append(title)
        magnetLink = tds[3].find("a")["href"]
        dmhy.append(magnetLink)
        size = tds[4].text
        dmhy.append(size)
        sendNum = tds[5].find("span").text
        dmhy.append(sendNum if sendNum.strip() != '' else '0')
        downNum = tds[6].find("span").text
        dmhy.append(downNum if downNum.strip() != '' else '0')
        comNum = tds[7].text
        dmhy.append(comNum if comNum.strip() != '' else '0')
        publisher = tds[8].find("a").text
        dmhy.append(publisher if publisher.strip() != ''else "")
        dmhy_datas.append(DmhyData(dmhy))
        print(
            "time:" + time + " classi:" + classi + " title:" + title + " magnetLink:" + magnetLink + " size:" + size + " sendNum:" + sendNum + " downNum:" + downNum + " comNum:" + comNum + " publisher:" + publisher)
    return dmhy_datas


if __name__ == '__main__':
    text = getDMHYHtml("http://share.dmhy.org/topics/list/page/1")
    dmhydatas = analysisHtml(text)
    db = DatabaseConnection("127.0.0.1", user="root", passwd='xlsw', db='test')
    dmop = DmhyDataOperator(db);
    dmop.add_dmhydata_list(dmhydatas)
