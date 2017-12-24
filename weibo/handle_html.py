import os
import re
import json
from bs4 import BeautifulSoup


files1 = os.listdir('./part1')
files2 = os.listdir('./part2')
files3 = os.listdir('./part3')
out = open('result', 'w')
## ctt 第一个标签为用户名-> name
## ctt span 标签第四个开始为微博
## ct span 标签为发布时间

'''
{
    name: username,
    content: 微博内容,
    date: 日期,
    time: 具体时间
}
'''

def handle_time(time_str):

    date_pat = re.compile(u"\d+月\d+日".encode('utf-8').decode())
    time_pat = re.compile(" .+?:.+\xa0")
    date_m = date_pat.search(str(time_str))
    time_m = time_pat.search(str(time_str))
    if not date_m:
        date_pat = re.compile('\d{4}-\d{2}-\d{2}')
        date_m = date_pat.search(str(time_str))
        if not date_m:
            date_m = re.search(u"今天".encode('utf-8').decode(), str(time_str))
            if not date_m:
                return 'unknown type', 'unknown type'
    time_text = ""
    if not time_m:
        time_m = re.search(" .+?:.+", str(time_str))
        time_text = time_m.group()
    else:
        time_text = time_m.group()[1:-1]
    return date_m.group(), time_text

data = []
def extract_weibo(file_name):
    text = open(file_name).read()
    soup = BeautifulSoup(text, 'html.parser')
    user_info = soup.find('div', attrs={'class': 'ut'})
    if not user_info:
        print(file_name)
    weibo = soup.find_all('span', attrs={'class': 'ctt'})
    time_info = soup.find_all('span', attrs={'class': 'ct'})
    
    user_pat = re.compile('class="ctt">.+?<img')
    user_m = user_pat.search(str(user_info))
    username = ""
    weibo_content = []
    if not user_m:
        user_pat = re.compile('class="ut">.+?\xa0')
        user_m = user_pat.search(str(user_info))
        username = user_m.group()
        username = username[11:-1]
        weibo_content = weibo
    else:
        username = user_m.group()
        username = username[12:-4]
        weibo_content = weibo[3:]

    time_list = []
    weibo_list = []
    length = len(weibo_content)
    assert(length == len(time_info))
    for i in range(length):
        w = weibo_content[i]
        t = time_info[i]
        w_str = w.text
        t_str = t.text
        date, time_detail = handle_time(t_str)
        one_piece = {'username': username, 'content': w_str, 'date': date, 'time': time_detail}
        data.append(one_piece)



for f in files1:
    file_name = './part1/' + f
    extract_weibo(file_name)
for f in files2:
    file_name = './part2/' + f
    extract_weibo(file_name)
for f in files3:
    file_name = './part3/' + f
    extract_weibo(file_name)

out.write(json.dumps(data))

out.close()
