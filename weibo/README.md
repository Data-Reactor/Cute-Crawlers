# 微博数据爬取

目标：<br>

- 爬取内地、港台明星势力榜前50名的明星近期微博数据。
- http://chart.weibo.com/?rank_type=3&version=v1
- http://chart.weibo.com/?rank_type=5&version=v1


达成：<br> 

- 爬取共100名明星微博。
- 共计24219条微博。


## 技术路线

1. 获取排行榜 HTML，利用 Python3 抽取出明星微博 ID 列表。
2. 用 Burpsuite 截取登录后对 `weibo.cn/id` 的访问请求，添加至 `Intruder`。（为了快速爬取，把每页条数设置为50; 为了获取获取页数参数，在页面翻页器里输入1）
3. 设置 POST Request URL 中 ID 部分和 Body Parameter 里 page 值为 Intruder Position，进行批量并发爬取（为降低封号概率，可降低并发线程数和请求时间间隔）
	- `http://weibo.cn/$ 12345678 $`
	- `page=$ 1 $`
4. 保存下批量获取的 HTML 后，用 Python3 读取逐个文件提取信息。


Blog for details: https://today2tmr.com/2017/12/24/微博数据爬取/
