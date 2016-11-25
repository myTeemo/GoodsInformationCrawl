# -*- coding:utf-8 -*-

from selenium import webdriver
from lxml import etree
from lang import lang
import time
import requests
import json

___author__ = 'Mingyang HE'

class goodsDetails(object):

    '''
        该类将获取每一个链接对应商品的价格、参数、图片、以及用户的评论
    '''
    def __init__(self,href):
        self.href = href
        self.browser = webdriver.Chrome(lang.chromeDriver)

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
            self.getGoodsComments(pageSource)
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
        # 注意这列面的str的格式为'gbk',不解码的话很容易因为里面含有中文导致出现乱码导致失败
        content_json = content[index+1:-1].decode('gbk')
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

    def getGoodsComments(self,html):
        pass
        #print comment



if __name__ =='__main__':

    details = goodsDetails(lang.JD_Goods_Href);
    try:
        details.getGoodsArgs()
    except Exception as e:
        print e
    finally:
        details.browser.close()
