import os
import json
import requests

API_key = ''
secret_key = ''
# boson 提供的免费次数较少，可以多申请几个
X_Token1 = ''
X_Token2 = ''

baidu_header = {'Content-Type': 'application/json'}
boson_header = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Token': X_Token1}

baidu_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_key}&client_secret={secret_key}'.format(API_key=API_key, secret_key=secret_key)
baidu_at = requests.post(baidu_url).text


def boson_emo(whole):
    global boson_emo
    res = requests.post('http://api.bosonnlp.com/sentiment/analysis', headers=boson_header, data=whole.encode())
    return res.text


def keywords_extract(whole):
    global boson_header
    res = requests.post('http://api.bosonnlp.com/keywords/analysis', headers=boson_header, data=whole.encode())
    return res.json()


def write_data(text, kw_f, emo_f):
    kw_result = open(kw_f, 'w')
    emo_result = open(emo_f, 'w')

    emo_res = boson_emo(json.dumps(text))
    emo_result.write(emo_res)

    keywords = keywords_extract(json.dumps(text))
    for weight, word in keywords:
        kw_result.write(str(weight) + ' ' + word + '\n')
    
    kw_result.close()
    emo_result.close()


count = 1
for f in os.listdir('./weixin_articles'):
    emo_f = './emotion_analysis/weixin_articles/' + f
    kw_f = './keywords/weixin_articles/' + f
    fi = open('./weixin_articles/' + f, 'r')
    text = fi.read()
    fi.close()
    write_data(text, kw_f, emo_f)
    write_data(text, emo_f)

    count += 1
    if count == 495:
        boson_header['X-Token'] = X_Token2

for f in os.listdir('./answer'):
    emo_f = './emotion_analysis/answer/' + f
    kw_f = './keywords/answer/' + f
    fi = open('./answer/' + f, 'r')
    text = fi.read()
    fi.close()
    write_data(text, kw_f, emo_f)

    count += 1
    if count == 495:
        boson_header['X-Token'] = X_Token2

for f in os.listdir('./zhuanlan'):
    emo_f = './emotion_analysis/zhuanlan/' + f
    kw_f = './keywords/zhuanlan/' + f
    fi = open('./zhuanlan/' + f, 'r')
    text = fi.read()
    fi.close()
    write_data(text, kw_f, emo_f)

    count += 1
    if count == 495:
        boson_header['X-Token'] = X_Token2


fi = open('weibo_articles', 'r')
weibo_news = fi.read()
fi.close()
emo_f = './emotion_analysis/weibo_articles'
kw_f = './keywords/weibo_articles'
write_data(weibo_news, kw_f, emo_f)

