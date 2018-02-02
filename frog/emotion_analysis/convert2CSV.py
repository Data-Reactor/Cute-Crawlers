import os
import csv

csv_file = open('emotion.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['title', 'nonnegative', 'negative'])

files = ['weibo_articles']

for f in os.listdir('./zhuanlan'):
    files += ['./zhuanlan/' + f]

for f in os.listdir('./answer'):
    files += ['./answer/' + f]
    
for f in os.listdir('./weixin_articles'):
    files += ['./weixin_articles/' + f]

for f in files:
    fi = open(f, 'r')
    data = eval(fi.read())[0]
    nonnegative = data[0]
    negative = data[1]
    writer.writerow([f, nonnegative, negative])
    fi.close()

csv_file.close()

