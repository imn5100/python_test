# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from hyper import HTTPConnection


# 避免类型转换异常
def set_int(intNum):
    try:
        return int(intNum)
    except Exception:
        return 0


def build_headers():
    return {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.100 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'cookie': '',
            'upgrade-insecure-requests': '1',
            }


def analysisHtml(text):
    soup = BeautifulSoup(text)
    body = soup.find('tbody', id="data_list")
    datas = []
    for tr in body.findAll("tr"):
        tds = tr.findAll("td")
        data = {}
        data['time'] = tds[0]['title']
        data['classi'] = tds[1].find("font").text
        data['title'] = tds[2].find("a", target="_blank").text
        data['size'] = tds[3].text
        data['magnet_link'] = tds[4].find("a")["href"]

        data['sendNum'] = set_int(tds[5].find("span").text)
        data['downNum'] = set_int(tds[6].find("span").text)
        data['comNum'] = set_int(tds[7].find("span").text)

        publisher = tds[8].find("a").text
        data['publisher'] = (publisher if publisher.strip() != ''else "")

        datas.append(data)
        print(
            "time:" + data['time'] + " classi:" + data['classi'] + " title:" + data['title'] + " magnetLink:" + data[
                'magnet_link'] + " size:" + data['size'] + " sendNum:" + str(
                data['sendNum']) + " downNum:" + str(data['downNum']) + " comNum:" + str(
                data['comNum']) + " publisher:" + data['publisher'])
    return datas


def get_acgnx_index():
    conn = HTTPConnection("share.acgnx.se", port=443)
    headers = build_headers()
    conn.request('GET', '/', headers=headers)
    resp = conn.get_response()

    for cookie in resp.headers['set-cookie']:
        headers['cookie'] = headers['cookie'] + cookie.split(';')[0] + "; "
    print (headers['cookie'])
    conn.request('GET', '/', headers=headers)
    resp = conn.get_response()
    response_js = resp.read()

    key_index = response_js.find('jump|')
    value_index = response_js.find("|escape")
    key = response_js[key_index + 5:key_index + 5 + 32]
    value = response_js[value_index - 32: value_index]
    new_cookie = key + "=" + value + ";"
    headers['cookie'] = headers['cookie'] + new_cookie
    print (headers['cookie'])

    conn.request('GET', '/', headers=headers)
    resp = conn.get_response()
    return resp.read()


if __name__ == '__main__':
    # html = open("acgnx.html").read()
    html = get_acgnx_index()
    datas = analysisHtml(html)
    datas.reverse()
    for data in datas:
        print (str(data['time']) + " " + data['classi'] + ":" + data['title'])
