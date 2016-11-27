# -*- coding:utf-8 -*-

from selenium import webdriver
from lxml import etree
from lang import lang
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'Mingyang HE'


class JD(object):

    """
        对输入的每一个关键字,在京东商城上查找改关键字,并获取每一个商品的链接,为后续工作做准备。
    """

    def __init__(self):
        self.baseUrl = lang.JD_Base_Url
        # self.browser = webdriver.Chrome(lang.chromeDriver)
        self.browser = webdriver.PhantomJS()
        self.browser.set_page_load_timeout(30)
        self.searchGoodsName = ''
        self.goodsHref_Set = set()

    def searchGoods(self):
        self.browser.get(self.baseUrl)
        self.browser.find_element_by_id(lang.JD_Find_Input_Goods_ID).send_keys(self.searchGoodsName.decode('utf-8'))
        self.browser.find_element_by_class_name(lang.JD_Find_Input_Goods_Button).click()
        time.sleep(5)

        # 异常处理,对于搜索的商品没有信息,则抛出异常
        try:
            pageSource = self.browser.page_source

            # print pageSource
            # 查找当前的搜索商品的一共拥有的页数
            pages, counts = self.findTotalPage(pageSource)
        except:
            pages = '0'
            counts = '0'
        finally:
            print lang.JD_Find_Goods_Counts.substitute(counts=counts, pages=pages, GoodsName=self.searchGoodsName)

        # 获取每一页的商品链接
        for page in range(1, int(pages) + 1):
            try:
                print lang.JD_Load_Every_Count.substitute(count=str(page))
                self.browser.find_elements_by_xpath(lang.JD_Find_Input_Counts)[0].clear()
                self.browser.find_elements_by_xpath(lang.JD_Find_Input_Counts)[0].send_keys(page)
                self.browser.find_elements_by_xpath(lang.JD_Find_Input_Counts_Button)[0].click()
                # time.sleep(5)
                pageSource = self.browser.page_source
                self.goodsHref(pageSource)
            except Exception as e:

                print  lang.JD_Exception.substitute(reason=str(e).encode('utf-8'))

        print lang.finish_IN_JD_Search.substitute(GoodsName=self.searchGoodsName)

        self.browser.close()

    # 获取搜索商品的页数
    def findTotalPage(self, pageSource):
        pageSource = etree.HTML(pageSource)

        page = pageSource.xpath(lang.JD_Find_Counts)[0].decode('utf-8')
        count = pageSource.xpath(lang.JD_Find_Goods_Counts_T)[0].decode('utf-8')
        return page, count

    # 获取所有商品的链接
    def goodsHref(self, pageSource):
        pageSource = etree.HTML(pageSource)
        results = pageSource.xpath(lang.JD_Find_Goods_Href)
        # print len(results)
        for result in results:
            if str(result).startswith('https:') == False:
               result = lang.JD_Href.substitute(href=result)
            print result
            self.goodsHref_Set.add(result)
                # print self.browser.page_source

                # time.sleep(30)
if __name__ == '__main__':
    try:
        searchGoodsName = raw_input(lang.input)
        JDSearch = JD()
        JDSearch.searchGoodsName = searchGoodsName
        print lang.start_IN_JD_Search.substitute(GoodsName=searchGoodsName)
        JDSearch.searchGoods()
        print len(JDSearch.goodsHref_Set)
    except KeyboardInterrupt:
        print lang.stop_IN_JD_Search.substitute(GoodsName=searchGoodsName)
    except Exception as e:
        print lang.JD_Exception.substitute(reason=str(e).encode('utf-8'))
        JDSearch.browser.close()
