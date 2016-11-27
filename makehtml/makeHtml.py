# -*- coding:utf-8 -*-

import markdown
import re
from jd import goodsDetails
from lang import lang
import  sys
__author__ = 'Mingyang HE'

reload(sys)
sys.setdefaultencoding("utf-8")

class MakeHtml(object):

    def __init__(self,goodhref,goodargs):
        pattern = re.compile(r'\d+')
        self.goodHref = goodhref
        self.productId =re.findall(pattern,self.goodHref)[0]

        self.goodName = goodargs['name']
        self.goodPrice = goodargs['price']
        self.goodBrand = goodargs['brand']
        self.goodArgs  = goodargs['args']
        self.goodImages= goodargs['images']
        self.goodComments = goodargs['comments']
        self.productCommentSummary = self.goodComments[0]
        self.hotCommentTagStatistics = self.goodComments[1]
        self.allComments = self.goodComments[2]

    def writeMD(self):

        # print self.goodName,self.goodHref
        with open(self.productId+'.md','w') as File:
            File.write('<center>\n')
            File.write('## ['+self.goodName+']('+self.goodHref+')  \n</center>\n\n')
            File.write('### 商品介绍\n\n')
            File.write('- 京东价：'+self.goodPrice+'\n')
            File.write('- '+self.goodBrand+'\n')

            for arg in self.goodArgs:
                File.write('- '+arg+'\n')
            File.write('\n')

            File.write('### 商品图片\n\n')
            index = 1
            for image in self.goodImages:
                File.write('!['+str(index)+']('+image+')')
                index += 1

            File.write('\n\n')
            productCommentSummary = self.productCommentSummary


            File.write('### 商品评论参数\n\n')
            File.write('\n<center>\n\n')
            File.write('|属性|值|\n')
            File.write('|:---:|:---:|\n')
            File.write('|好评率|' +  str(productCommentSummary['goodRateShow'])   +'|\n')
            File.write('|中评率|' + str(productCommentSummary['generalRateShow']) +'|\n')
            File.write('|差评率|' + str(productCommentSummary['poorRateShow'])    +'|\n')
            File.write('|差评数|' + productCommentSummary['poorCountStr']         +'|\n')
            File.write('|中评数|' + productCommentSummary['generalCountStr']      +'|\n')
            File.write('|好评数|' + productCommentSummary['goodCountStr']         +'|\n')
            File.write('|追评数|' + productCommentSummary['afterCountStr']        +'|\n')
            File.write('|总评数|' + productCommentSummary['commentCountStr']      +'|\n\n\n')
            File.write('\n</center>\n\n')

            File.write('### 商品评论标签\n\n')
            File.write('\n<center>\n\n')
            File.write('|评论标签|支持人数|\n')
            File.write('|:---:|:---:|\n')

            for listDict in self.hotCommentTagStatistics:
                File.write('|'+listDict['name']+'|'+str(listDict['count'])+'|\n')
            File.write('\n\n\n')
            File.write('\n</center>\n\n')
            # print self.allComments

            File.write('### 用户评论\n\n')
            File.write('\n<center>\n\n')
            File.write('|属性参数|属性值|\n')
            File.write('|:---:|:---:|\n')
            for listDict in self.allComments:
                File.write('|所在省份|' + listDict['userProvince']     + '|\n')
                File.write('|注册时间|' + listDict['userRegisterTime'] + '|\n')
                File.write('|昵   称|' + listDict['nickname']          + '|\n')
                File.write('|会员身份|' + listDict['userLevelName'] + '|\n')
                File.write('|评   分|' + str(listDict['score']) + '|\n')

                if listDict['days'] == 0 :
                    days = '当天'
                else:
                    days = str(listDict['days'])

                File.write('|评论时间|购买后' + days + '天评论|\n')
                File.write('|评论内容|' + listDict['content'] + '|\n')

                if len(listDict['commentTags']) >0 :
                    File.write('|评论标签|')
                    for commentTag in listDict['commentTags']:
                        File.write(commentTag+'、')
                    File.write('|\n')

                if len(listDict['imageUrl']) >0:
                    File.write('|图片|')
                    for image in listDict['imageUrl']:
                        File.write('![]('+image+')')
                    File.write('|\n')

            File.write('\n<center>\n')

if __name__ == '__main__':

    try:

        JD = goodsDetails.GoodsDetails(lang.JD_Goods_Href);
        href = JD.href
        goodArgs = JD.getGoodsArgs()
        MakeHtml(href,goodArgs).writeMD()
    except Exception as e:
        print e
    finally:
        JD.browser.close()

