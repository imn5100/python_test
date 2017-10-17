# -*- coding: utf-8 -*-


def build_headers():
    return {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.100 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'cookie': '',
            'upgrade-insecure-requests': '1',
            }


def get_acgnx():
    from hyper import HTTPConnection

    conn = HTTPConnection("share.acgnx.se", port=443)
    headers = build_headers()
    conn.request('GET', '/', headers=headers)
    resp = conn.get_response()

    print(resp.read())
    print(resp.status)
    print(resp.headers)

    print (resp.headers['set-cookie'])
    for cookie in resp.headers['set-cookie']:
        headers['cookie'] = headers['cookie'] + cookie.split(';')[0] + "; "
    print (headers['cookie'])
    conn.request('GET', '/', headers=headers)
    resp = conn.get_response()
    print(resp.read())
    print(resp.status)
    print(resp.headers)


if __name__ == '__main__':
    # get_acgnx()
    response_js = "<!doctype html><html><head><meta charset=\"utf-8\"><meta http-equiv=\"pragma\" " \
                  "content=\"no-cache\"><meta http-equiv=\"cache-control\" content=\"no-store\"><script " \
                  "type=\"text/javascript\">eval(function(p,a,c,k,e,r){e=function(c){return c.toString(a)};if(" \
                  "!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){" \
                  "return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g')," \
                  "k[c]);return p}('f 8={2:\"k\",c:\"j\"};6 e(a){g 0<4.2.7&&(3=4.2.9(a+\"=\"),-1!=3)?(3=3+a.7+1," \
                  "5=4.2.9(\";\",3),-1==5&&(5=4.2.7),h(4.2.i(3,5))):\"\"}6 d(a,b){4.2=a+\"=\"+l(b)+\";m=/;\"}6 n(){d(" \
                  "\"o\",8.2);p.q=8.c};',27,27," \
                  "'||cookie|c_start|document|c_end|function|length|data|indexOf|||uri|setCookie|getCookie|var|return" \
                  "|unescape|substring|https://share.acgnx.se/|4ddf4480c5293b125ad0d312832c6593|escape|path|jump" \
                  "|d196174838d710e1e8f850c3569b33ed|window|location'.split('|'),0,{}))</script></head><body " \
                  "onLoad=\"javascript:jump()\"></body></html> "

    key_index = response_js.find('jump|')
    value_index = response_js.find("|escape")
    key = response_js[key_index + 5:key_index + 5 + 32]
    value = response_js[value_index - 32: value_index]
    print (key + ":" + value)
