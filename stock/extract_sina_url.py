from bs4 import BeautifulSoup
import requests
import re
import os

files_guzai = os.listdir('./新浪财经/股灾')
files_xiadie = os.listdir('./新浪财经/股市下跌')

f2w = open('guzai_hrefs', 'w')

for f in files_guzai:
    f2r = open('./新浪财经/股灾/' + f, 'r', encoding='gbk')
    text = f2r.read()
    soup = BeautifulSoup(text, 'html.parser')
    hrefs = []
    tags = soup.find_all('div', class_='r-info r-info2')
    for tag in tags:
        a = tag.find('a')
        hrefs.append(a.attrs['href'])
    f2w.write('\n')
    f2w.write('\n'.join(hrefs))
    f2r.close()

f2w.close()

f2w = open('xiadie_hrefs', 'w')

for f in files_xiadie:
    f2r = open('./新浪财经/股市下跌/' + f, 'r', encoding='gbk')
    text = f2r.read()
    soup = BeautifulSoup(text, 'html.parser')
    hrefs = []
    tags = soup.find_all('div', class_='r-info r-info2')
    for tag in tags:
        a = tag.find('a')
        hrefs.append(a.attrs['href'])
    f2w.write('\n')
    f2w.write('\n'.join(hrefs))
    f2r.close()

