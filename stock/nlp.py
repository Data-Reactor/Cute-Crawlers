import os
import json
import requests

API_key = 'jneHH1DBcyO0aqUKjNE7d690'
secret_key = 'OC7BKNCq1bAe1BkyGDM7h19OpcbenoKD'
# boson 提供的免费次数较少，可以多申请几个
X_Token1 = '6vNOGKRD.21931.okrZDxJqR4xG'
X_Token2 = 'zG6frEro.21938.CSkDG_VWENc4'
X_Token3 = 'kKARO_Sx.21937.iqsLwybu46Ab'

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

    kw_result.write('ratio,word\n')
    emo_result.write('title,nonnegative,negative\n')

    emo_res = boson_emo(json.dumps(text))
    emo2w = eval(emo_res)[0]
    emo_result.write(emo_f + ',' + str(emo2w[0]) + ',' + str(emo2w[1]))

    keywords = keywords_extract(json.dumps(text))
    for weight, word in keywords:
        kw_result.write(str(weight) + ',' + word + '\n')
    
    kw_result.close()
    emo_result.close()

dirs = ['/em_guzai' , '/em_xiadie', '/sina_guzai', '/sina_xiadie']

count = 1

for d in dirs:
    for f in os.listdir('.' + d):
        emo_f = './emotion_analysis' + d + '/' + f
        kw_f = './keywords' + d + '/' + f
        fi = open('.' + d + '/' + f, 'r')
        text = fi.read()
        fi.close()
        write_data(text, kw_f, emo_f)

        count += 1
        if count == 495:
            if boson_header['X-Token'] == X_Token1:
                boson_header['X-Token'] = X_Token2
            else:
                boson_header['X-Token'] = X_Token3

