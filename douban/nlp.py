import re
import os
import json
import requests
header = {'Content-Type': 'application/json'}
#header = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Token': 'zG6frEro.21938.CSkDG_VWENc4'}
files = os.listdir(os.getcwd())
comments = []
news = []
for i in files:
    if '_comments' in i:
        comments.append(i)
    if '_news' in i:
        news.append(i)

def emotion_analyse(data):
    res = requests.post('https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.93e74bba8e232c1cb0d009c5cc077dab.2592000.1518354788.282335-10682969', headers=header, data=json.dumps(data).encode())
    return res.text


def keywords_extract(whole):
    res = requests.post('http://api.bosonnlp.com/keywords/analysis', headers=header, data=whole.encode())
    return res.json()

for f in comments + news:
    result = open(f + '_emotion_result', 'w')
    f = open(f, 'r')
    whole = f.read()
    text = whole.split('\n')
    for one in text:
        data = {"text": one}
        emo_result = emotion_analyse(data)
        try:
            item = json.loads(emo_result)['items'][0]
            result.write(str(item['positive_prob']) + ' ' + str(item['negative_prob']) + '\n')
        except:
            pass

    # keywords = keywords_extract(json.dumps(whole))
    # for weight, word in keywords:
    #     result.write(str(weight) + ' ' + word + '\n')
    result.close()
    f.close()

