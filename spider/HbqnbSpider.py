# encoding:utf-8
import requests
from lxml import etree
from util.DataCleanUtil import DataCleanUtil
from pymongo import MongoClient

class HbqnbSpider(object):
    def __init__(self):
        self.domian = 'http://www.hbqnb.com'
        self.url = 'http://www.hbqnb.com/index/8'
        self.categoryIndexList = ["1","2","5","8","7","9","10"]
        self.conn = MongoClient('localhost', 27017)
        self.db = self.conn.itableSpider
        self.collections = self.db.hbqnb

    def request(self,url):
        return etree.HTML(requests.get(url).text)

    def run(self):
        parseElemet = self.request(self.url)
        headerLinkList = parseElemet.xpath('//*[@class="one-newlist"]/header/a/@href')
        for link in headerLinkList:
            element = self.request(self.domian + link)
            try:
                title = element.xpath('//*[@class="newsdetail-top"]/h1/text()')[0]
                source = DataCleanUtil.sliceByColon(element.xpath('//*[@class="newsdetail-top"]/div/span[1]/text()')[0])
                datetime = element.xpath('//*[@class="newsdetail-top"]/div/span[2]/text()')[0]
                author = DataCleanUtil.sliceByColon(element.xpath('//*[@class="newsdetail-top"]/div/span[3]/text()')[0])
                content = DataCleanUtil.listJoinToStringBynewline(element.xpath('//*[@class="main-editor"]/p/text()'))
                imgs = element.xpath('//*[@class="main-editor"]//img/@src')
            except IndexError:
                title = source = datetime = author = content = imgs = None
            data = {
                'title':title,
                'source':source,
                'datatime':datetime,
                'author':author,
                'content':content,
                'imgs':imgs
            }
            self.collections.save(data)

if __name__ == '__main__':
    spider = HbqnbSpider()
    spider.run()
