# http://service.library.mtime.com/CMS.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetSearchNewsList&Ajax_CrossDomain=1&Ajax_CallBackArgument0={title}&Ajax_CallBackArgument1={page}
import re
import requests
import math

title_pat = re.compile('"title":".+?","url"')
count_pat = re.compile('"newsCount":\d+')
news_base_url = 'http://service.library.mtime.com/CMS.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetSearchNewsList&Ajax_CrossDomain=1&Ajax_CallBackArgument0={title}&Ajax_CallBackArgument1={page}'
page_size = 20

box_date = open('box_date', 'r')

while 1:
    line = box_date.readline()
    if not line:
        break
    line_split = line.split()
    title = line_split[1]
    news_f = open(title + '_news', 'w')
    res = requests.get(news_base_url.format(title=title, page=1)).text
    count_m = count_pat.search(res)
    count = 0
    if count_m:
        count = count_m.group()[12:]
    else:
        continue
    title_m = title_pat.findall(res)
    for m in title_m:
        news_title = m[9:-7]
        news_f.write(news_title + '\n')
    pages = math.ceil(int(count) / page_size)
    for p in range(pages - 1):
        res = requests.get(news_base_url.format(title=title,page=p+2)).text
        title_m = title_pat.findall(res)
        for m in title_m:
            news_title = m[9:-7]
            news_f.write(news_title + '\n')
    news_f.close()

