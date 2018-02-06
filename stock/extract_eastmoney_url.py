import requests
import json
import re
import os

files_guzai = os.listdir('./东方财富/股灾')
files_xiadie = os.listdir('./东方财富/股市下跌')

f2w = open('em_guzai_hrefs', 'w')

for f in files_guzai:
    f2r = open('./东方财富/股灾/' + f, 'r')
    text = f2r.read()
    index = text.index('{')
    json_data = json.loads(text[index:])['Data']
    hrefs = []
    for data in json_data:
        hrefs.append(data['Art_Url'])
    f2w.write('\n')
    f2w.write('\n'.join(hrefs))
    f2r.close()

f2w.close()

f2w = open('em_xiadie_hrefs', 'w')

for f in files_xiadie:
    f2r = open('./东方财富/股市下跌/' + f, 'r')
    text = f2r.read()
    index = text.index('{')
    json_data = json.loads(text[index:])['Data']
    hrefs = []
    for data in json_data:
        hrefs.append(data['Art_Url'])
    f2w.write('\n')
    f2w.write('\n'.join(hrefs))
    f2r.close()

f2w.close()

