import requests
import json
from bs4 import BeautifulSoup
import re

null = None

class Movie:
    title = ''
    average_rating = None
    pubdate = None
    box = None
    news = {'Keywords': None, 'amount': None}
    comments = {'keywords': None, 'score': None}
    reviews = {'keywords': None, 'score': None}

search_base_url = 'http://www.cbooo.cn/search?k='

title_rate = open('title_rate', 'r')
search_pat = re.compile('href="http://www.cbooo.cn/m/\d+?" title=".+?"')
box_pat = re.compile('<span class="m-span">累计票房<br />.+?</span>')

box_date = open('box_date', 'w')

while 1:
    line = title_rate.readline()
    if not line:
        break
    line_split = line.split()
    title = line_split[1]

    res = requests.get(search_base_url + title).text
    match = search_pat.search(res)
    if not match:
        continue
    substr = match.group().split('"')
    url = substr[1]
    mtitle = substr[3]
    try:
        assert title == mtitle
    except:
        print(title, mtitle)
        continue
    detail = requests.get(url).text
    box_match = box_pat.search(detail)
    if not box_match:
        continue
    box = box_match.group()[31:-7]
    date_match = re.search('上映时间：.+?（中国）', detail)

    if not date_match:
        continue
    date = date_match.group()[5:-4]
    box_date.write(line[:-1] + ' ' + box + ' ' + date + '\n')

box_date.close()
title_rate.close()
