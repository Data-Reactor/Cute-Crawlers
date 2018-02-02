import os
import csv

files = ['weibo_articles']

for f in os.listdir('./zhuanlan'):
    files += ['./zhuanlan/' + f]

for f in os.listdir('./answer'):
    files += ['./answer/' + f]
    
for f in os.listdir('./weixin_articles'):
    files += ['./weixin_articles/' + f]

for f in files:
    csv_file = open(f + '.csv', 'w')
    writer = csv.writer(csv_file)
    writer.writerow(['ratio', 'word'])

    fi = open(f, 'r')
    data = fi.read().replace(' ', ',')
    csv_file.write(data)
    fi.close()

    csv_file.close()


