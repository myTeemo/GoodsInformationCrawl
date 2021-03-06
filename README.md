##京东商品、商品参数、商品评论爬虫

---
- jd/goodsHref.py 上JD商品的连接爬取,对输入的一个关键字,进行搜索,并返回商品链接
	1. 输入的字符串使用  "" 包含起来
	2. 使用selenium自动化测试工具,这个感觉不稳定,很容易受网络连接的影响,而导致获取网页过慢甚至无法获取网页,其方便之处,他说自动处理动态页面,而不需要考虑动态加载的问题。支持的驱动为Chrome、FireFox、IE、Safari等;后续将会对浏览器的参数进行设置,进一步的优化,或者使用无头浏览器PhantomJS等.
	3. 链接中处理部分使用xpath()语法,具体的配置可看lang/lang.py文件

---

- jd/goodsDetails.py


	1. 根据商品的链接爬取商品参数,包括名称、价格、常用参数、图片、评论等
	2. 商品的名称、价格处理还比较方便
 	3. 图片处理最棘手.
  		处理的步骤为:
     	- 在访问商品的连接返回的页面中找到script标签下的一个'desc'部分其对应的键值为商品的图片链接
    	- 然后在GET这个链接,得到内容
    	- 再解析成HTML
     	- 在使用xpath抽取图片链接
	4. 评论也有些麻烦。
     	- 评论存在一个特定的规律可循,根据这个链接可抓取相应的需要的数据
          [例子](https://sclub.jd.com/comment/productPageComments.action?productId=2402694&score=0&sortType=3&page=0&pageSize=10)

           固定: https://sclub.jd.com/comment/productPageComments.action?

        		- productId:商品Id唯一
        		- score:商品评分 0:所有评论;1:差评;2:中评;3好评;4晒图;5:追评
        		- sortType:默认为3
        		- page:当前评分高的起始页
        		- pageSize:获取的页面的评论条数多少,最多为10,最少为0,多余10,按照10来处理

    	- 然后抽取需要的参数部分

---

- makeHtml部分

	1\. 使用MarkDown语法导出相应文件  
	2\. 使用python中的markdown模块导出静态HTML文件（更新中）  
	

---
- 存在的问题:
    1. selenium的不问题性,会导致访问失败,同时参数的抽取失败等等不稳定的因素
    2. 在后续将使用多线程或者多线程的模式
    3. 同时考虑分布式爬虫
    4. ip代理
    5. 数据存储的不合理性
   	6. 后续将考虑使用WEB呈现,不过首选可能使用Markdown生成静态页面

-----持续更新-----