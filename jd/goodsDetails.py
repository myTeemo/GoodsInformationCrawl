# -*- coding:utf-8 -*-

from selenium import webdriver
from lxml import etree
from lang import lang
import time
import requests
import json
import re
import chardet


___author__ = 'Mingyang HE'

class goodsDetails(object):

    '''
        该类将获取每一个链接对应商品的价格、参数、图片、以及用户的评论
    '''
    def __init__(self,href):

        self.href = href
        self.browser = webdriver.Chrome(lang.chromeDriver)
        self.score = '0'
        self.sortType = '3'
        self.page = '0'
        self.pageSize = '10'

    def getGoodsArgs(self):
        self.browser.get(self.href)
        time.sleep(2)

        pageSource = self.browser.page_source
        # print pageSource
        pageSource = etree.HTML(pageSource)
        GoodsArgs={}

        # 在网页中,他的标签信息会有不同,则会有如下两种方案
        name =pageSource.xpath(lang.JD_Goods_Name_Arg_1)
        if len(name) == 0:
            name = pageSource.xpath(lang.JD_Goods_Name_Arg_2)
        GoodsArgs['name'] = name[0]

        # 价格的获取
        GoodsArgs['price'] = pageSource.xpath(lang.JD_Goods_Price_Arg)[0].xpath('string(.)').replace('\n','').replace(' ','')

        try:
            # 商品参数
            GoodsIndroduce = pageSource.xpath(lang.JD_Goods_Introduce_Parent)[0]
            brand = GoodsIndroduce.xpath(lang.JD_Goods_Introduce_Brand)[0].xpath('string(.)').replace('\n','').replace(' ','')
            args =  GoodsIndroduce.xpath(lang.JD_Goods_Introduce_Args_1)
            if len(args) == 0:
                args = GoodsIndroduce.xpath(lang.JD_Goods_Introduce_Args_2)

            GoodsArgs['brand'] = brand

        except Exception as e:

            print lang.JD_Exception.substitute(e)

        finally:
            # 输出信息
            print GoodsArgs['name']
            print GoodsArgs['price']

            for arg in args:

                print arg.xpath('string(.)').replace('\n','').replace(' ','')

            GoodsArgs['images'] = self.getGoodsImages(pageSource)
            self.getGoodsComments()
    # 获取商品的图片链接
    def getGoodsImages(self,html):
        GoodsImages = []
        # 根据网页中发现,页面中的图片链接是在一个 script标签中的一个为desc的配置中里面包含了链接的地址 '//dx.3.cn/desc/10082905269?cdn=2',通过下面
        # 的方法,获取里面的字段值
        try:
            script = html.xpath(lang.JD_Goods_Images_script_Args1)[0].replace('\n','').replace(' ','').encode('utf-8')
        except:
            script = html.xpath(lang.JD_Goods_Images_script_Args2)[0].replace('\n','').replace(' ','').encode('utf-8')
        index = script.find('=')
        script = script[index+1:]
        image_desc = ''
        for desc in script.split(','):
            if desc.startswith('desc'):
                # 去除两端的''
                image_desc = desc.split(':')[1][1:-1]

        image_desc = lang.JD_Href.substitute(href=image_desc)

        # 图片链接的json地址
        print lang.JD_Goods_Images_Href_Addr.substitute(desc=image_desc)
        show_image_desc = requests.get(image_desc)
        content = show_image_desc.content
        index = content.find('(')
        # print chardet.detect(content)
        content_json = content[index+1:-1].decode('GB18030')
        content_json = json.loads(content_json)
        image_content = content_json['content']
        # print image_content
        # 将图片链接部分的代码解析成HTML
        image_content = etree.HTML(image_content)
        ImagesHrefList = image_content.xpath(lang.JD_Goods_Images_Src)
        # 从HTML中获取图片链接
        print lang.JD_Goods_Images_Href_Counts.substitute(imageCounts=len(ImagesHrefList))
        for imageHref in ImagesHrefList:
            if imageHref.startswith('http:https:') or imageHref.startswith('http:'):
                imageHref = imageHref[5:]
            else:
                if imageHref.startswith('https:http:'):
                    imageHref = imageHref[6:]
                else:
                    imageHref = 'https:'+imageHref
            print imageHref
            GoodsImages.append(imageHref)
        # 返回图片链接列表
        return GoodsImages

    # 获取商品的评价

    def getGoodsComments(self):

        pattern = re.compile(r'\d+')
        productId = re.findall(pattern,self.href)[0]

        comments_addr=lang.JD_Goods_Comments_JSON.substitute(productId=productId, score=self.score, sortType=self.sortType, page=self.page,pageSize=self.pageSize)
        print  comments_addr
        comment_Json = requests.get(comments_addr)
        # print  comment_Json.content
        # print comment_Json.encoding
        # 这里的编码是一个坑,request返回的结果是GBK,但是却给报
        # UnicodeDecodeError: 'gbk' codec can't decode bytes in position 48923-48924: illegal multibyte sequence
        # 这样的错误,后来发现原因是这里面返回的结果的某些字符,GBK不能解码的。于是尝试比GBK更具有兼容性的GB18030编码,于是解决问题
        comment_Json_content = comment_Json.content.decode('GB18030')

        comment_Json_content = json.loads(comment_Json_content)

        # 商品的评论概要,返回一个字典
        productCommentSummary = comment_Json_content['productCommentSummary']
        # 热点评论标签统计,返回一个列表,列表里面的每一个元素是一个字典
        hotCommentTagStatistics = comment_Json_content['hotCommentTagStatistics']
        # 当前搜索评分下的最大页数,返回int类型
        maxPage = comment_Json_content['maxPage']
        # 评分  0:全部评论;1:差评;2中评;3:好评;4:晒图;5:追评 返回int类型
        score = comment_Json_content['score']
        # 分类类型 默认是3 这个字段没有看懂是什么意思,但是却是必须要有的,否则会得不到返回的结果,返回int类型
        sortType = comment_Json_content['soType']
        # 图片列表的数量,这里表示晒图中一共有多上张图片,返回int类型
        imageListCount = comment_Json_content['imageListCount']
        # 评论主体部分,是一个列表,列表里面的每一个元素是一个字典
        comments = comment_Json_content['comments']

        # 过滤商品评论概要
        productCommentSummary_Filter = self.productCommentSummaryFilter(productCommentSummary)
        # 过滤热点商品标签统计
        hotCommentTagStatistics_Filter = self.hotCommentTagStatisticsFilter(hotCommentTagStatistics)
        # 过滤买家评论
        comments_Filter = self.commentsFilter(comments)
        # print productCommentSummary_Filter
        # print hotCommentTagStatistics_Filter
        # print comments_Filter
        self.outputProductCommentSummary_Filter(productCommentSummary_Filter)
        self.outputHotCommentTagStatistics_Filter(hotCommentTagStatistics_Filter)
        self.outputcomments_Filter(comments_Filter)
    # 过滤商品评论概要,返回字典
    def productCommentSummaryFilter(self,productCommentSummary):
        # 过滤商品评论概要
        productCommentSummary_Filter = {}
        # 好评率
        productCommentSummary_Filter['goodRateShow'] = productCommentSummary['goodRateShow']
        # 中评率
        productCommentSummary_Filter['generalRateShow'] = productCommentSummary['generalRateShow']
        # 差评率
        productCommentSummary_Filter['poorRateShow'] = productCommentSummary['poorRateShow']
        # 差评数量
        productCommentSummary_Filter['poorCountStr'] = productCommentSummary['poorCountStr'].encode('utf-8')
        # 中评数量
        productCommentSummary_Filter['generalCountStr'] = productCommentSummary['generalCountStr'].encode('utf-8')
        # 好评数量
        productCommentSummary_Filter['goodCountStr'] = productCommentSummary['goodCountStr'].encode('utf-8')
        # 追评数量
        productCommentSummary_Filter['afterCountStr'] = productCommentSummary['afterCountStr'].encode('utf-8')
        # 全部评论数量
        productCommentSummary_Filter['commentCountStr'] = productCommentSummary['commentCountStr'].encode('utf-8')
        return productCommentSummary_Filter

    # 过滤热点商品标签统计,返回列表,列表的每一个元素是一个字典
    def hotCommentTagStatisticsFilter(self,hotCommentTagStatistics):
        hotCommentTagStatistics_Filter=[]
        for hotCommentTagStatistic in hotCommentTagStatistics:
            temp_dict={}
            temp_dict['name'] = hotCommentTagStatistic['name'].encode('utf-8')
            temp_dict['count'] = hotCommentTagStatistic['count']
            hotCommentTagStatistics_Filter.append(temp_dict)
        return hotCommentTagStatistics_Filter

    # 过滤买家评论
    def commentsFilter(self,comments):
        comments_Filter=[]
        for comment in comments:
            temp_dict={}
            temp_dict['content'] = comment['content'].encode('utf-8')
            temp_dict['score'] = comment['score']
            temp_dict['userProvince'] = comment['userProvince'].encode('utf-8')
            temp_dict['userRegisterTime'] = comment['userRegisterTime'].encode('utf-8')
            temp_dict['nickname'] = comment['nickname'].encode('utf-8')
            temp_dict['userLevelName'] = comment['userLevelName'].encode('utf-8')
            try:
                temp_image_list = []
                for image in comment['images']:
                    if image['imgUrl'].startswith('http'):
                        temp_image_list.append(image['imgUrl'].encode('utf-8'))
                    else:
                        temp_image_list.append('https:'+image['imgUrl'].encode('utf-8'))

                temp_dict['imageUrl'] = temp_image_list
            except:
                pass

            try:
                temp_commentTags_list=[]
                for commentTag in comment['commentTags']:
                    temp_commentTags_list.append(commentTag['name'].encode('utf-8'))
                temp_dict['commentTags'] = temp_commentTags_list
            except:
                pass

            if comment['isMobile'] :
                temp_dict['userClientShow'] = comment['userClientShow'].encode('utf-8')
            else:
                temp_dict['userClientShow']=''

            temp_dict['days'] = comment['days']
            comments_Filter.append(temp_dict)
        return comments_Filter


    def outputProductCommentSummary_Filter(self,productCommentSummary_Filter):
        print '好评率:'+str(productCommentSummary_Filter['goodRateShow'])+'%'
        print '中评率:'+str(productCommentSummary_Filter['generalRateShow'])+'%'
        print '差评率:'+str(productCommentSummary_Filter['poorRateShow'])+'%'
        print '总评数:'+productCommentSummary_Filter['commentCountStr']
        print '差评数:'+productCommentSummary_Filter['poorCountStr']
        print '中评数:'+productCommentSummary_Filter['generalCountStr']
        print '好评数:'+productCommentSummary_Filter['goodCountStr']
        print '追评数:'+productCommentSummary_Filter['afterCountStr']

    def outputHotCommentTagStatistics_Filter(self,hotCommentTagStatistics_Filter):
        for hotCommentTag in hotCommentTagStatistics_Filter:
            print '有 '+str(hotCommentTag['count'])+' 人评论说: '+hotCommentTag['name']

    def outputcomments_Filter(self,comments_Filter):
        for comment in comments_Filter:
            if comment['userClientShow']:
                if comment['userProvince']:
                    print '来自 '+comment['userProvince']+' 的在 '+comment['userRegisterTime']+' 注册的 '+comment['nickname']+' '+comment['userLevelName']+' 使用 '\
                                +comment['userClientShow']+' 评论说: '+comment['content']+'并给予 '+str(comment['score'])+' 分评价',
                    if comment.has_key('imageUrl'):
                        print '并附上图片:'
                        for imageUrl in comment['imageUrl']:
                            print imageUrl





if __name__ =='__main__':

    details = goodsDetails(lang.JD_Goods_Href);
    try:
        details.getGoodsArgs()
    except Exception as e:
        print e
    finally:
        details.browser.close()
