# encoding:utf-8
import json
from lxml import etree
import requests
import PyV8
from pymongo import MongoClient

class JrttSpider(object):

    def __init__(self,urlList):
        self.urlList = urlList
        self.conn = MongoClient('localhost', 27017)
        self.db = self.conn.itableSpider
        self.collections = self.db.jrtt

    def request(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        return etree.HTML(requests.get(url,headers=headers).text)

    def toJsonString(self,object):
        """
        该方法通过使用PyV8库执行JavaScript代码文件，将js对象转换成JSON字符串
        :param object: String,从原HTML文件中爬取到的json对象（当前为字符串）
        :return: object经过转换后的JSON字符串
        """
        with PyV8.JSContext() as ctxt:
            ctxt.eval(
                u"""
                    object = {};
                    jsonString = JSON.stringify(object);
                """.format(object)
            )
            vars = ctxt.locals
            return vars.jsonString

    def parseElement(self,element):
        """
        该方法用于解析element中的HTML标签内容，包括meta标签的关键字和描述
        :param element: Element对象的HTML
        :return: 文章的关键字、描述
        """
        try:
            keywords = element.xpath('//*[@name="keywords"]/@content')
            description = element.xpath('//*[@name="description"]/@content')
            return keywords[0], description[0]
        except IndexError,e:
            print e
            return None, None

    def run(self):
        for url in self.urlList:
            parseElemet = self.request(url)
            # scriptBlock = list(parseElemet.xpath('//script/text()'))[4][16:]
            # scriptBlockJson = self.toJsonString(scriptBlock)
            # print scriptBlockJson
            keywords, description = self.parseElement(parseElemet)
            column = {
                'keywords':keywords,
                'description':description
            }
            self.collections.insert(column)
            break

    def called(self):
        self.run()

if __name__ == '__main__':
    spider = JrttSpider(
        ['https://www.toutiao.com/a6557871064444043779/',
         'https://www.toutiao.com/a6557884307371721229/']
    )
    spider.called()