#According to keyword ......
import requests
import re
import urllib
import urllib2
from bs4 import BeautifulSoup




# headers
User_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/54.0'
headers = {'User-agent':User_agent}

'''
url = "http://www.baidu.com"
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)
print(response.read())
'''

baseURL = "https://www.baidu.com/s?"

keywords_path = "/home/manyue/Project/Git/Spider/Baidu/keywords.txt" 
link_path = "/home/manyue/Project/Git/Spider/Baidu/get_link.txt"
text_path = "/home/manyue/Project/Git/Spider/Baidu/get_text.txt"

with open(keywords_path,'r') as f:
	for word in f:
		data = {'ie':'utf-8','tn':'baiduurt','wd':word}
		searchURL = baseURL + urllib.urlencode(data)

		try:
			request = urllib2.Request(searchURL,headers=headers)
			response = urllib2.urlopen(request)
			read_response = response.read()
			soup = BeautifulSoup(read_response,"html.parser")
			all_link = soup.find_all(attrs={'class':'result c-container '})

			for link in all_link:
				with open(link_path,'a') as f_w:
					f_w.write(link.a['href'] + '\n')	

		except Exception as e:
			pass

with open(link_path,'r') as f:
	for link in f:
		try:
			request = urllib2.Request(link,headers=headers)
			response = urllib2.urlopen(request)
			read_response = response.read()
			soup = BeautifulSoup(read_response,"html.parser")
			find_text = soup.find('article',attrs={'class':'article'})
			content = find_text.find_all('p')
			string = ''

			for t in content:

				print(t.text)


				
				
			#	print(t.text)


			#with open(text_path,'w'):

   			#	file.write(string + '\n')
  					
		

		except Exception as e:
			pass


	
