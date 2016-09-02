# -*- coding: utf-8 -*-

from src.dmhyCrawler.DbOperator import DatabaseConnection


class DmhyDataOperator(object):
    def __init__(self, db):
        self.db = db

    def add_dmhydata(self, dmhydata):
        sql = "insert into  dmhy(`time`, `classi`, `title`, `magnetLink`, `size`, `seedNum`, `downNum`, `comNum`, `publisher`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        self.db.put(sql, (
            dmhydata.time, dmhydata.classi, dmhydata.title, dmhydata.magnetLink, dmhydata.size, dmhydata.sendNum,
            dmhydata.downNum, dmhydata.comNum, dmhydata.publisher))

    def add_dmhydata_list(self, dmhy_data_list):
        sql = "insert into  dmhy(`time`, `classi`, `title`, `magnetLink`, `size`, `seedNum`, `downNum`, `comNum`, `publisher`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        params = []
        i = 0
        for dmhydata in dmhy_data_list:
            params[i] = (
                dmhydata.time, dmhydata.classi, dmhydata.title, dmhydata.magnetLink, dmhydata.size, dmhydata.sendNum,
                dmhydata.downNum, dmhydata.comNum, dmhydata.publisher)
            i = i + 1
        self.db.put_many(sql, params)

    def getby_title(self, title):
        datas = self.db.get_all("select *  from dmhy where title like %s order by time desc", ('%' + title + '%',))
        dmhydatas = []
        for  data in datas:
            dmhydataObj = DmhyData(data)
            dmhydatas.__add__(dmhydataObj)
        return dmhydatas;

class DmhyData(object):
    def __init__(self, id, time, classi, title, magnetLink, size, seedNum=0, downNum=0, comNum=0, publisher=''):
        self.id = id
        self.time = time
        self.classi = classi
        self.title = title
        self.magnetLink = magnetLink
        self.size = size
        self.sendNum = seedNum
        self.downNum = downNum
        self.comNum = comNum
        self.publisher = publisher

    def build(self, data):
        self.id = data[0]
        self.time = data[1]
        self.classi = data[2]
        self.title = data[3]
        self.magnetLink = data[4]
        self.size = data[5]
        self.sendNum = data[6]
        self.downNum = data[7]
        self.comNum = data[8]
        self.publisher = data[9]


# test
if __name__ == '__main__':
    db = DatabaseConnection("127.0.0.1", user="root", passwd='xlsw', db='test')
