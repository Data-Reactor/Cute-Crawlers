## 数据源

- 微博搜索 [http://s.weibo.com/list/replage?search=旅行青蛙&page=1](http://s.weibo.com/list/replage?search=旅行青蛙&page=1)
- 搜狗知乎 [http://zhihu.sogou.com](http://zhihu.sogou.com)
- 搜狗微信 [http://weixin.sogou.com](http://weixin.sogou.com)


## 数据格式

*这次数据全部从HTML提取，没有使用API，但是zhihu的API还是比较好用的，下次再尝试*


- 微信公众号发布的文章(微信文章链接有一定有效期，再次使用需要重新抓取搜索结果提取新的链接) 共采集285条
	- 以 `<h2 class='rich_media_title' />` 为标题
	- 以 `<div class='rich_media_content ' />` 为文章内容
	- 以 `<em id='post-date' />` 为发布时间
	- 文章中每部分文字被 `<span />` 包裹
	- 少部分为转发内容，标题和文章内容检索不到，简单跳过不作处理
- 知乎问答 共采集271条
	- 以 `<div class='ContentItem AnswerItem' />` 为回答卡片
		- 其中 `data-zop` json 属性含问题标题 `title`
	- 以 `<span class='CopyrightRichText-richText' />` 为回答内容
	- 回答数目含于 `<a class='QuestionMainAction' />` 文本中
	- 以 `<meta itemprop="dateCreated" />` 为回答发布时间
		- 其中 `content` 文本属性为发布时间的字符串
- 知乎专栏文章 共采集183条
	- 以 `<h1 class='PostIndex-title' />` 为标题
	- 以 `<time />` 为时间
		- 其中 `datetime` 属性含发布时间的字符串
	- 文字每部分文字被 `<p />` 包裹
	- 以 `<span class='BlockTitle-title' />` 为评论数
- 微博文章搜索结果 共采集178条
	- 以 `<a class='W_texta W_fb' />` 中的 title 属性为标题
	- 以 `<a class='W_textb' title='\u5206\u4eab'>` 为分享数 
