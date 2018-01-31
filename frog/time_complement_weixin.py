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
    time_tag = soup.find('em', id='post-date')
    if not time_tag:
        print('No time info')
        post_time = 'No time info'
    else:
        post_time = time_tag.string

    f = open('./weixin_articles/' + h2.replace('/', ' '), 'r+')
    raw_content = f.read()
    f.seek(0,0)
    f.write(post_time + '\n' + raw_content)
    f.close()

    time.sleep(1)
    print('Progress: ' + str(count) + '\n')
    count += 1


