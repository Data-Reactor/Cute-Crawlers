import requests
import json
import re


f = open('movie_list')
url_pat = re.compile('\d{8}')
base_api_url = 'http://api.douban.com/v2/movie/subject/'
title_rate = open('title_rate', 'w')


while 1:
    line = f.readline()
    if not line:
        break
    movie_id = url_pat.search(line).group()
    res = requests.get(base_api_url + movie_id)
    res = eval(res.text)

    movie = Movie()
    movie.title = res['title']
    movie.average_rating = res['rating']['average']
    
    title_rate.write('{} {} {}\n'.format(movie_id, movie.title, movie.average_rating))

f.close()
title_rate.close()

