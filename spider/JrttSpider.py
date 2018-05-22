# encoding:utf-8
from spider.util.DataFormateUtil import DataFormateUtil
import json
import HTMLParser
from lxml import etree
import requests
import PyV8
from pymongo import MongoClient

class JrttSpider(object):

    def __init__(self,urlList):
        self.urlList = urlList
        self.conn = MongoClient('localhost', 27017)
        self.db = self.conn.wspider
        self.collections = self.db.jrtt

    def request(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        return etree.HTML(requests.get(url,headers=headers).text)

    def toJsonString(self, object):
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

    def parseContent(self,content):
        """
        该方法解析网页的源代码部分，解析出图片连接列表，和图片的数量
        :param content: 源代码
        :return: html：转义后的HTML;imgUrlList：图片链接列表;len(imgUrlList)：图片数量
        """
        html = HTMLParser.HTMLParser().unescape(content) # 转义
        element = etree.HTML(html)
        imgUrlList = element.xpath('//img/@src')
        return html,imgUrlList,len(imgUrlList)

    def run(self):
        for url in self.urlList:
            parseElemet = self.request(url)
            keywords, description = self.parseElement(parseElemet)
            scriptBlock = list(parseElemet.xpath('//script/text()'))[4][16:]
            scriptBlockJson = self.toJsonString(scriptBlock)
            scriptBlockDict = json.loads(scriptBlockJson)

            title = scriptBlockDict.get('articleInfo').get('title')
            content = scriptBlockDict.get('articleInfo').get('content')
            time = scriptBlockDict.get('articleInfo').get('subInfo').get('time')
            author = scriptBlockDict.get('articleInfo').get('subInfo').get('source')
            category = scriptBlockDict.get('headerInfo').get('chineseTag')
            tags = scriptBlockDict.get('articleInfo').get('tagInfo').get('tags')
            feedInfoInitList = scriptBlockDict.get('feedInfo').get('initList')

            # 格式化
            feedLinkInfo = [item.get('source_url') for item in feedInfoInitList]
            publishTime = DataFormateUtil.stringToDateTime(time)
            tags = [item.get('name') for item in tags]
            html, imgUrlList,imgCount =  self.parseContent(content)  # 解析出图片的链接和图片的数量

            column = {
                'title': title,
                'content': html,
                'imgUrlList':imgUrlList,
                'imgCount':imgCount,
                'description': description,
                'author': author,
                'publishTime': publishTime,
                'category': category,
                'tags': tags,
                'keywords': str(keywords.encode('utf-8')).split(','),
                'feedLinkInfo': feedLinkInfo,
                'source':'来源名',
                'sourceIndex': '来源序号',
                'sourceUrl':'URL来源',
                'sourceCategory':'来源分类',
                'sourceFacedgroup':'面向人群',
                'isVerified': 0
            }
            self.collections.insert(column)
            # break


    def called(self):
        self.run()

if __name__ == '__main__':
    spider = JrttSpider(
        [
         # 'https://www.toutiao.com/a6557871064444043779/',
         # 'https://www.toutiao.com/a6557884307371721229/',
         'https://www.toutiao.com/a6555987011059057166/',
         'https://www.toutiao.com/i6500077774579958286']
    )
    spider.called()