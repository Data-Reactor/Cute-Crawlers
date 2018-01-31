import re
import os
from bs4 import BeautifulSoup

files = os.listdir('./zhihu')
zhuanlan_f2w = open('zhuanlan_hrefs', 'w')
answer_f2w = open('answer_hrefs', 'w')

for f in files:
    f2r = open('./zhihu/' + f, 'r')
    text = f2r.read()
    soup = BeautifulSoup(text, 'html.parser')
    zhuanlan_hrefs = []
    answer_hrefs = []
    zhuanlan_tags = soup.find_all('a', href=re.compile('zhuanlan.zhihu.com'))
    answer_tags = soup.find_all('a', href=re.compile('www.zhihu.com/question/\d+/answer/\d+'))
    for a in zhuanlan_tags:
        zhuanlan_hrefs.append(a.attrs['href'])
    zhuanlan_hrefs = list(set(zhuanlan_hrefs))

    for a in answer_tags:
        answer_hrefs.append(a.attrs['href'])
    answer_hrefs = list(set(answer_hrefs))

    zhuanlan_f2w.write('\n')
    zhuanlan_f2w.write('\n'.join(zhuanlan_hrefs))

    answer_f2w.write('\n')
    answer_f2w.write('\n'.join(answer_hrefs))

    f2r.close()
zhuanlan_f2w.close()
answer_f2w.close()

