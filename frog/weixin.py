import requests
from bs4 import BeautifulSoup
import os
import time

hrefs_file = open('./hrefs')
hrefs = hrefs_file.read().split('\n')

count = 1
for href in hrefs:
    if href.strip() == '':
        continue
    res = requests.get(href)
    if res.status_code != 200:
        print('Error:' + str(res.status_code))
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    h2 = soup.find('h2', class_='rich_media_title')
    if not h2:
        print('No rich_media_title ' + href + '\n')
        continue
    h2 = h2.string.strip()
    content = soup.find('div', class_='rich_media_content ')
    if not content:
        print('No rich_media_content ' + href + '\n')
        continue
    spans = content.find_all('span')
    strings = ''

    for s in spans:
        if not s.string:
            continue
        if s.string.strip() == '':
            continue
        strings += s.string.strip()

    strings = h2 + '\n' + strings

    f = open('./weixin_articles/' + h2.replace('/', ' '), 'w')
    f.write(strings)
    f.close()

    time.sleep(1)
    print('Progress: ' + str(count) + '\n')
    count += 1


