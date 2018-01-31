import requests
import time
from bs4 import BeautifulSoup

zhuanlan_hrefs = open('zhuanlan_hrefs', 'r')
hrefs = zhuanlan_hrefs.read().split('\n')
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36', 'referer':'https://zhuanlan.zhihu.com/p/33354278'}

count = 1

for href in hrefs:
    if href.strip() == '':
        continue
    res = requests.get(href, headers=headers)
    if res.status_code != 200:
        print('Error: ' + str(res.status_code) + '\n')
        continue
    soup = BeautifulSoup(res.text, 'html.parser')
    
    post_time = soup.find('time')
    if not post_time:
        post_time = 'No time info'
    else:
        post_time = post_time.attrs['datetime']

    comment_num = soup.find('span', class_='BlockTitle-title')
    if not comment_num:
        comment_num = 'Not found comment number'
    else:
        comment_num = comment_num.string

    title = soup.find('h1', class_='PostIndex-title')
    if not title:
        print('No title')
        continue
    title = title.string

    contents = soup.find_all('p')
    strings = comment_num + '\n' + post_time + '\n' + title + '\n'
    for tag in contents:
        if not tag.string:
            continue
        if tag.string.strip() != '':
            strings += tag.string.strip()

    f = open('./zhuanlan/' + title, 'w')
    f.write(strings)
    f.close()

    print('Progress: ' + str(count) + '\n')
    count += 1
    time.sleep(1)

