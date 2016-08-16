# -*- coding=utf8 -*-

import re
import time
import requests
from pyquery import PyQuery

def getip181Proxy():
    html = requests.get('http://www.ip181.com').content.decode('gb2312', 'ignore')
    pq = PyQuery(html)

    proxys = []
    for tr in pq("tr"):
        element = [PyQuery(td).text() for td in PyQuery(tr)("td")]
        if 'HTTPS' not in element[3]:
            continue

        ret = re.search(r'\d+\.\d+', element[4], re.UNICODE)
        if ret and float(ret.group()) > 5:
            continue

        proxys.append((element[0], element[1]))

    return proxys

if __name__ == '__main__':
    print getip181Proxy()
