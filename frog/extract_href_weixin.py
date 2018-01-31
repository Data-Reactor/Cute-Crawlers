import re
import os
from bs4 import BeautifulSoup

files = os.listdir('./weixin')
f2w = open('hrefs', 'w')

for f in files:
    f2r = open('./weixin/' + f, 'r')
    text = f2r.read()
    soup = BeautifulSoup(text, 'html.parser')
    hrefs = []
    tags = soup.find_all('a', href=re.compile('mp.weixin.qq.com'), uigs=re.compile('article_title'))
    for a in tags:
        hrefs.append(a.attrs['href'])
    f2w.write('\n')
    f2w.write('\n'.join(hrefs))
    f2r.close()
f2w.close()

