#coding=utf-8
import requests
import re
import json


def category(index):

	FindCategory=["书籍_杂志_报纸.json","收纳整理.json","男包.json","电子词典_电纸书_文化用品.json","女装.json","个性定制_设计服务_DIY.json"]
	categoryNUM = ["&cps=yes&cat=33","&cps=yes&cat=55098010","&cps=yes&cat=50072686","&cps=yes&cat=50018627","&cps=yes&cat=50102996","&cps=yes&cat=50096795"]
	
	return FindCategory[index], categoryNUM[index]


def taobao(index,good,maxpage):
	baseURL = "https://s.taobao.com/search?q=" + good
	file_name, link = category(index)

	with open(file_name,'w') as f:
		for i in range(1,maxpage):
			num = 44*i
			searchURL = baseURL + link +"&s=" + str(num)

			html = requests.get(searchURL)

			

			title = re.findall(r'"raw_title":"([^"]+)"',html.text)
			sales = re.findall(r'"view_sales":"([^"]+)"',html.text)
			nick_name = re.findall(r'"nick":"([^"]+)"',html.text)
			price = re.findall(r'"view_price":"([^"]+)"',html.text)
			shipping_fee = re.findall(r'"view_fee":"([^"]+)"',html.text)
			

			for j in range(0,len(title)):

				data = {
					'name' : title[j],
					'sales' : sales[j],
					'nick' : nick_name[j],
					'price' : price[j],
					'shipping_fee':shipping_fee[j]
				}

				json.dump(data,f,ensure_ascii=False,indent=4)

for i in range(0,6):
	taobao(i,"开学",11)