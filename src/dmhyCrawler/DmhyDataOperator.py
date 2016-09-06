# -*- coding: utf-8 -*-

from src.dmhyCrawler.DbOperator import DatabaseConnection


class DmhyDataOperator(object):
    def __init__(self, db):
        self.db = db

    def add_dmhydata(self, dmhydata):
        sql = "insert into  dmhy(`time`, `classi`, `title`, `magnetLink`, `size`, `seedNum`, `downNum`, `comNum`, `publisher`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.db.put(sql, (
            dmhydata.time, dmhydata.classi, dmhydata.title, dmhydata.magnetLink, dmhydata.size, dmhydata.sendNum,
            dmhydata.downNum, dmhydata.comNum, dmhydata.publisher,))

    def add_dmhydata_list(self, dmhy_data_list):
        sql = "insert into  dmhy(`time`, `classi`, `title`, `magnetLink`, `size`, `seedNum`, `downNum`, `comNum`, `publisher`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = []
        for dmhydata in dmhy_data_list:
            params.append((
                dmhydata.time, dmhydata.classi, dmhydata.title, dmhydata.magnetLink, dmhydata.size, dmhydata.sendNum,
                dmhydata.downNum, dmhydata.comNum, dmhydata.publisher))
        self.db.put_many(sql, params)

    def getby_title(self, title):
        datas = self.db.get_all("select *  from dmhy where title like %s order by time desc", ('%' + title + '%',))
        dmhydatas = []
        for data in datas:
            dmhydataObj = DmhyData(data)
            dmhydatas.append(dmhydataObj)
        return dmhydatas;

    def get_one_bytitle(self, title):
        data = self.db.get_one("select *  from dmhy where title like %s order by time desc", (title,))
        return DmhyData(data)

    def getby_title_time(self, title, start_time, end_time, classi='動畫'):
        datas = self.db.get_all(
                'select *  from dmhy where  title in (select title from dmhy where  title like %s) and time>%s and time<%s and classi=%s',
                ('%' + title + '%', start_time, end_time, classi,))
        dmhydatas = []
        for data in datas:
            dmhydataObj = DmhyData(data)
            dmhydatas.append(dmhydataObj)
        return dmhydatas;

    def getby_id(self, id):
        sql = "select * from dmhy where id=%s"
        data = self.db.get_one(sql, (id,))
        return DmhyData(data)

    # 只针对关键数据更新，其他数据不管
    def update(self, dmhydata):
        if None == dmhydata.id or None == dmhydata.magnetLink or dmhydata.magnetLink.strip() == '':
            return False
        sql = 'UPDATE dmhy SET magnetLink=%s,size=%s,seedNum=%s,downNum=%s,comNum=%s  WHERE id=%s '
        self.db.put(sql, (dmhydata.magnetLink, dmhydata.size, dmhydata.sendNum,
                          dmhydata.downNum, dmhydata.comNum, dmhydata.id,))
        return True


class DmhyData(object):
    def __init__(self):
        self.sendNum = '0'
        self.downNum = '0'
        self.comNum = '0'
        self.publisher = ''

    def __init__(self, data):
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


# 避免类型转换异常
def set_int(intNum):
    try:
        return int(intNum)
    except:
        return 0


def sort_dmhy_list(dmhydatas):
    dmhydatas.sort(None, key=lambda dmhy_data: (dmhy_data.sendNum + dmhy_data.comNum + dmhy_data.downNum), reverse=True)


# test
if __name__ == '__main__':
    db = DatabaseConnection("127.0.0.1", user="root", passwd='xlsw', db='test')
    dmop = DmhyDataOperator(db)
    dmhydatas = dmop.getby_title_time('NEW GAME', '2016/09/06 00:00', '2016/09/07 00:00')
    for obj in dmhydatas:
        print  (
            "time:" + obj.time + " classi:" + obj.classi + " title:" + obj.title + " size:" + obj.size + " sendNum:" + str(
                    obj.sendNum) + " downNum:" + str(obj.downNum) + " comNum:" + str(obj.comNum) + " sorted:" + str(
                    obj.sendNum + obj.comNum + obj.downNum))
    print "-" * 10
    dmhydatas.sort(None, key=lambda dmhy_data: (dmhy_data.sendNum + dmhy_data.comNum + dmhy_data.downNum), reverse=True)
    for obj in dmhydatas:
        print  (
            "time:" + obj.time + " classi:" + obj.classi + " title:" + obj.title + " size:" + obj.size + " sendNum:" + str(
                    obj.sendNum) + " downNum:" + str(obj.downNum) + " comNum:" + str(obj.comNum) + " sorted:" + str(
                    obj.sendNum + obj.comNum + obj.downNum))


def test_update(dmop):
    dmhydata = dmop.getby_id(80)
    dmhydata.magnetLink = dmhydata.magnetLink + "1"
    dmhydata.size = "80MB"
    dmhydata.sendNum = dmhydata.sendNum + 1
    dmhydata.downNum = dmhydata.downNum + 1
    dmhydata.comNum = dmhydata.comNum + 1
    dmop.update(dmhydata)
