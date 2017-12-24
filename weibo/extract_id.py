import re
pat = re.compile("http://weibo.com/\d+")
id_list = []

def extract_id(file_name):
    text = open(file_name).read()
    matches = pat.findall(text)
    matches = list(set(matches))
    for m in matches:
        m_id = re.search("\d+", m)
        id_list.append(m_id.group())

files = ["hongkong1.html", "hongkong2.html", "mainland1.html", "mainland2.html"]

for file_name in files:
    extract_id(file_name)


print(len(id_list))

out = open("id_list", "w")
for _id in id_list:
    for _ in range(10):
        out.write(_id+"\r\n")
out.close()
