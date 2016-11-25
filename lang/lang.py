# -*- coding:utf-8 -*-

from string import Template


___author__ = 'Mingyang HE'

# 浏览器驱动位置
chromeDriver = '/Users/Eilene/PycharmProjects/chromedriver'
input = '请输入你要搜索的商品名称\n'

# 京东商城配置信息
JD_Base_Url = 'https://www.jd.com/'
start_IN_JD_Search = Template('开始在京东商城搜索关键字为 "$GoodsName" 商品的信息')
stop_IN_JD_Search = Template('终止在京东商城搜索关键字为 "$GoodsName" 商品的信息')
finish_IN_JD_Search = Template('已完成在京东商城搜索关键字为 "$GoodsName" 商品的信息')
JD_Find_Input_Goods_ID ='key'
JD_Find_Input_Goods_Button = 'button'
JD_Find_Goods_Counts= Template('已搜索到 $counts 件商品 共 $pages 页 关于 $GoodsName 商品的信息')

JD_Load_Every_Count = Template('正在搜索第 $count 页')
# 找到搜索的关键字一个有多少个相关的类目
JD_Find_Goods_Counts_T = '//div[@class="f-result-sum"]/span[@id="J_resCount"]/text()'
# 找到获取页数的输入框
JD_Find_Input_Counts= '//div[@class="p-wrap"]/span[@class="p-skip"]/input[@type="text"]'
# 找到获取页数输入框的按钮
JD_Find_Input_Counts_Button = '//div[@class="p-wrap"]/span[@class="p-skip"]/a'
# 找到搜索关键字的商品页数
JD_Find_Counts = '//div[@class="page clearfix"]/div[@id="J_bottomPage"]/span[@class="p-skip"]/em/b/text()'
# 找到每一页商品的连接
JD_Find_Goods_Href = '//div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@href'
# 获取完整的连接
JD_Href = Template('https:$href')
# 意外中断
JD_Exception = Template('程序意外中断,原因是:$reason')

# 京东商城商品参数获取信息
JD_Goods_Href = 'https://item.jd.com/1211546112.html'
# 根据观察发现,想要获取商品的名字, 在网页中,他的标签信息会有不同,则会有如下两种方案
JD_Goods_Name_Arg_1 = '//div[@class="itemInfo-wrap"]/div[@class="sku-name"]/text()'
JD_Goods_Name_Arg_2 = '//div[@id="itemInfo"]/div[@id="name"]/h1/text()'

# 网页中,价格的获取信息标签也会存在不同,则对改标签使用'*'这样的通配符进行获取
JD_Goods_Price_Arg = '//div[@class="dd"]/*[@class="p-price"]'

JD_Goods_Introduce_Parent = '//div[@class="p-parameter"]'
JD_Goods_Introduce_Brand =  './ul[@id="parameter-brand"]'
JD_Goods_Introduce_Args_1 = './ul[@class="parameter2 p-parameter-list"]/li'
JD_Goods_Introduce_Args_2 = './ul[@id="parameter2"]/li'

# 商品的图片参数,由于script会有两种形式,所以这里面给出两种查询方式(通过观察发现),
JD_Goods_Images_script_Args1 = '//script[@charset="gbk"]/text()'
JD_Goods_Images_script_Args2 = '//script/text()'
JD_Goods_Images_Href_Addr = Template('正在从 $desc 中获取图片链接')
JD_Goods_Images_Href_Counts = Template('已获得共计 $imageCounts 个图片链接')
# 商品的图片链接参数
JD_Goods_Images_Src = '//img/@data-lazyload'

