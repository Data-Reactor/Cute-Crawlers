## 抓取信息列表

- 过滤信息
	- 大陆
	- 2017年
	- 4-6分
- 豆瓣id
- 豆瓣评分
- 豆瓣短评第一页
- 时光网信息
- 票房
- 上映时间


## 实现

- [base_info.py](base_info.py) 请求豆瓣API `http://api.douban.com/v2/movie/subject/` 获取基本信息（评分、电影名、豆瓣ID）
- [comments.py](comments.py) 直接访问短评页面并提取短评文字信息
- [box_date.py](box_date.py) 通过 `www.cbooo.cn` 获取票房和上映日期，同时通过判断信息是否缺失过滤网剧
- [news.py](news.py) 直接访问 `mtime.com` 电影新闻搜索页面抓取新闻标题
- [nlp.py](nlp.py) (部分语言处理代码) 通过百度API或其他可行NLP API进行文本分析


