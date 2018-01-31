import re
import os
from bs4 import BeautifulSoup

files = os.listdir('./weibo_search')
f2w = open('weibo_articles', 'w')

for f in files:
    f2r = open('./weibo_search/' + f, 'r')
    text = f2r.read()
    soup = BeautifulSoup(text, 'html.parser')
    html = eval(soup.find_all('script')[-4].string[41:-1])['html']
    soup = BeautifulSoup(html, 'html.parser')

    titles = []
    titles_tag = soup.find_all('a', class_='W_texta W_fb')
    for title in titles_tag:
        titles.append(title.attrs['title'])

    f2w.write('\n')
    f2w.write('\n'.join(titles))
    f2r.close()
f2w.close()

