import re
import requests
import time
from bs4 import BeautifulSoup

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
def contain_zh(word):
    global zh_pattern
    m = zh_pattern.search(word)
    if m:
        return True
    return False

answer_hrefs = open('answer_hrefs', 'r')
hrefs = answer_hrefs.read().split('\n')
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
    
    post_time = soup.find('meta', itemprop='dateCreated')
    if not post_time:
        post_time = 'No time info'
    else:
        post_time = post_time.attrs['content']

    answer_num = soup.find('a', class_='QuestionMainAction')
    if not answer_num:
        answer_num = 'Not found answer number'
    else:
        answer_num_m = re.search('\d+', answer_num.string)
        answer_num = answer_num_m.group()
        answer_num = '回答数：' + answer_num

    title = soup.find('div', class_='ContentItem AnswerItem')
    if not title:
        print('No title')
        continue
    title = eval(title.attrs['data-zop'])['title']

    contents = soup.find('span', class_='CopyrightRichText-richText')
    #contents = str(contents).split('<br/>')
    strings = answer_num + '\n' + post_time + '\n' + title + '\n'
    strings += contents.get_text()
    #for s in contents:
    #    strings += s

    f = open('./answer/' + title.replace('/', ' '), 'w')
    f.write(strings)
    f.close()

    print('Progress: ' + str(count) + '\n')
    count += 1
    time.sleep(1)

