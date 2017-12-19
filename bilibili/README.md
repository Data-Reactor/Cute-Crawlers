# bilibili Crawler
程序很小，熟悉新手练习。


- 无报错重试。
- 无粉丝信息（文尾有API，有需要可以自己加）。
- 收藏、作品、订阅信息只爬取了第一页。


## 运行环境
- Ubuntu 16.04
- Python 3.*
- 实际上开发的时候在anaconda3的docker里面跑的。
- Run: `python3 crawler.py` or `python crawler.py`
  - 输入期望爬取的有效数据量、最大爬取的用户量（有效和无效的总量）、开始爬取的用户UID


## 数据导出
- 程序结束后生成 `result` 文件，为未转码非格式化文件，可执行 `cat result | jq . > out.json` 导出格式化并且中文正常显示的 json 文件。
  - （`jq`需额外安装，`apt-get install jq`）
- 每100个数据分批存储，`result` `result1.0` `result2.0` ...
- **建议下Linux下阅读数据，Windows的数据格式看起来:)...**


## 报错信息
- 报错信息输出在 `error` 文件中，内置两类报错 `Error` 和 `Timeout`
- `Error` 一般为response状态码异常，有时是200返回信息中提示 `'message':'false'` 之类的。
- `Timeout` requests请求超时，全部设为2s，可以在源码中修改。


## 数据格式
- 为对象数组。每个对象格式如下：


```
{
	"mid": user_id,
	"name": name,
	"sex": sex,
	"birthday": birthday,
	"submitVideos": [
		"aid": video_id,
		"title": video_title,
		"tags": [tag1, tag2]
	],
	"bangumi": [
		"season_id": bangumi_id,
		"title": bangumi_title,
		"tags": [tag1, tag2]
	],
	"favorite": [
		"aid": video_id,
		"title": video_title,
		"tags": [tag1, tag2]
	]
}
```


## APIs 
这些API是通过开发者工具、Burpsuite、Postman、Restlet Client等工具找到的，忽略了不必要的params，可以自行检测进行深入研究。


- 粉丝信息 `GET https://api.bilibili.com/x/relation/followers?vmid=9161638`
- 收藏夹 `GET http://api.bilibili.com/x/v2/fav/video?vmid=552`
	- param: `pn` 页数
- 视频作品 `GET http://space.bilibili.com/ajax/member/getSubmitVideos?mid=5551`
	- params: `page` 页数, `pagesize` 每页数据量
- 视频标签 `GET https://api.bilibili.com/x/tag/archive/tags?aid=17348774`
- 个人信息 `POST https://space.bilibili.com/ajax/member/GetInfo`
	- Header: `{"Content-Type": "application/x-www-form-urlencoded
", "Referer": "Referer: https://space.bilibili.com/5551
"}`
	- Body: `mid=5551&csrf=null`
- 订阅视频: `GET http://space.bilibili.com/ajax/Bangumi/getList?mid=5551`
- 番剧标签: `GET http://bangumi.bilibili.com/jsonp/seasoninfo/6446.ver?callback=seasonListCallback`


## Some Other Notes
- 活跃用户密度会逐渐下将，推荐爬取靠前的用户。
- 最大用户UID在200,000,000左右，注册于2017年12月。

