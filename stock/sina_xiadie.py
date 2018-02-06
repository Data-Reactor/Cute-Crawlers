import requests
from bs4 import BeautifulSoup
import os
import time

hrefs_file = open('./sina_xiadie_hrefs')
hrefs = hrefs_file.read().split('\n')

count = 1
for href in hrefs:
    mode = 1
    if href.strip() == '':
        continue
    res = requests.get(href)
    res.encoding = res.apparent_encoding
    if res.status_code != 200:
        print('Error:' + str(res.status_code))
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    h1 = soup.find('h1', class_='main-title')
    if not h1:
        print('No main_title ' + href + '\n')
        h1 = soup.find('h1', id='artibodyTitle')
        mode = 2
        if not h1:
            print('No artibodyTitle' + href + '\n')
            continue
    h1 = h1.string.strip()
    if mode == 1:
        content = soup.find('div', class_='article')
    else:
        print('No article' + href + '\n')
        content = soup.find('div', id='artibody')
        if not content:
            print('No artibody' + href + '\n')
            continue

    [s.extract() for s in content('style')]
    [s.extract() for s in content('script')]
    strings = h1 + '\n' + content.get_text()

    f = open('./sina_xiadie/' + h1.replace('/', ' '), 'w')
    f.write(strings)
    f.close()

    time.sleep(1)
    print('Progress: ' + str(count) + '\n')
    count += 1

