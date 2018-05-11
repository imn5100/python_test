# -*- coding: utf-8 -*-
import urllib

if __name__ == '__main__':
    keyword = urllib.pathname2url("编码")
    searchUrl = "http://share.dmhy.org/topics/list/page/%u?keyword=%s" % (1, keyword);
    print searchUrl
