import requests
import re
from bs4 import BeautifulSoup
import os
import time

hrefs_file = open('./em_guzai_hrefs')
hrefs = hrefs_file.read().split('\n')

count = 1
for href in hrefs:
    if 'video' in href:
        continue
    mode = 1
    if href.strip() == '':
        continue
    res = requests.get(href)
    res.encoding = res.apparent_encoding
    if res.status_code != 200:
        print('Error:' + str(res.status_code))
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    h1 = soup.find('h1')
    if not h1:
        print('No title ' + href + '\n')
        continue
    h1 = h1.string.strip()
    content = soup.find('div', class_='Body')
    if not content:
        print('No article ' + href + '\n')
        continue
    [s.extract() for s in content('script')]
    [s.extract() for s in content('style')]
    comment = soup.find('div', class_='BodyEnd')
    a = comment.find('a', href=re.compile('http://guba.eastmoney.com'))
    comments = []
    if a:
        com_href = a.attrs['href']
        com = requests.get(com_href)
        com.encoding = com.apparent_encoding
        com_soup = BeautifulSoup(com.text, 'html.parser')
        for div in com_soup.find_all('div', class_='zwlitext stockcodec'):
            comments.append(div.get_text())

    strings = h1 + '\n' + content.get_text()

    f = open('./em_guzai/' + h1.replace('/', ' '), 'w')
    f.write(strings)
    f.close()

    if comments != []:
        f_com = open('./em_guzai/' + h1.replace('/', ' ') + '_comment', 'w')
        f_com.write('\n'.join(comments))
        f_com.close()

    time.sleep(1)
    print('Progress: ' + str(count) + '\n')
    count += 1

