import re
import requests
comment_pat = re.compile('<p class=""> .+\n')

box_date = open('box_date', 'r')
comment_base_url = 'https://movie.douban.com/subject/{mid}/comments'

while 1:
    line = box_date.readline()
    if not line:
        break
    line_split = line.split()
    mid = line_split[0]
    title = line_split[1]
    res = requests.get(comment_base_url.format(mid=mid)).text
    comment_m = comment_pat.findall(res)
    comment_f = open(title + '_comments', 'w')
    for comment in comment_m:
        comment_f.write(comment[12:])
    comment_f.close()
box_date.close()


