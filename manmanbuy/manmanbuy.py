#-*- coding:utf-8 -*-

from selenium import webdriver
from lxml import etree
import time


class manmanbuy(object):
    def __init__(self):
        self.baseUrl = 'http://www.manmanbuy.com/'

    def searchGoods(self,inputGoodsName):
        self.browser = webdriver.Chrome('/Users/Eilene/PycharmProjects/chromedriver')
        self.browser.maximize_window()
        self.browser.get(self.baseUrl)
        self.browser.find_element_by_id('skey').send_keys(inputGoodsName)
        self.browser.find_element_by_name('btnSearch').click()
        page_source = self.browser.page_source
        #print self.browser.page_source
        #self.browser.close()
        return page_source

    def get_info(self,html):
        html = etree.HTML(html)
        #result = etree.tostring(html)
        #print type(html)
        results = html.xpath('//div[@class="pic"]/a/@href')
        for result in results:
            self.browser.get(result)
            page_source = self.browser.page_source
            self.get_goods_details(page_source)
            #print result
        self.browser.close()
    def get_goods_details(self,html):
        print html
        html = etree.HTML(html)
        self.get_lowst_goods_details(html)
        pass

    def get_lowst_goods_details(self,html):
        result = html.xpath('//div[@class="pro-detail-box"]')[0]
        lowstGoodsDetail={}
        lowstGoodsDetail['title'] = result.xpath('//div[@class="title"]/h1/text()')[0].encode('utf-8').strip()
        lowstGoodsDetail['price'] = result.xpath('//div[@class="pro-detail-price"]')[0].xpath('string(.)').replace('\n','').replace(' ','')
       # lowstGoodsDetail['priceGraph'] =

        lowstGoodsDetail['star']  = result.xpath('//div[@class="pro-detail-info"]/p[@class="star"]')[0].xpath('string(.)').replace('\n','').replace(' ','')
        lowstGoodsDetail['xl'] = result.xpath('//div[@class="pro-detail-info"]/p[@class="xl"]')[0].xpath('string(.)').replace('\n', '').replace(' ', '')

        print lowstGoodsDetail['title'],lowstGoodsDetail['price'],lowstGoodsDetail['star'],lowstGoodsDetail['xl'],lowstGoodsDetail['priceGraph']

if __name__ == '__main__':
    GoodsName = input('请输入搜索的商品名称或型号:\n')
    GoodsName = GoodsName.strip()
    buy = manmanbuy()
    html = buy.searchGoods(GoodsName)
    buy.get_info(html)