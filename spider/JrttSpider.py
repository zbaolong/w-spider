# encoding:utf-8
from spider.util.DataFormateUtil import DataFormateUtil
import json
import logging
import HTMLParser
from multiprocessing import Process
from lxml import etree
import requests
import PyV8
from pymongo import MongoClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JrttSpider(object):

    def __init__(self,urlList,isFirst):
        self.isFirst = isFirst
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

    def run(self,url):
        parseElemet = self.request(url)
        if parseElemet.xpath('//*[@content="ixigua_pc_detail"]'):  # 如果匹配到视频的页面则不进行爬取
            return
        else:
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
            feedLinkList = [item.get('source_url') for item in feedInfoInitList] # 提取推荐列表的文章URL为列表
            publishTime = DataFormateUtil.stringToDateTime(time) # 格式化为时间日期格式
            tags = [item.get('name') for item in tags] # 提取tag标签内容为列表
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
                'feedLinkList': feedLinkList,
                'source':'来源名',
                'sourceIndex': '来源序号',
                'sourceUrl':'URL来源',
                'sourceCategory':'来源分类',
                'sourceFacedgroup':'面向人群',
                'isVerified': 0
            }
            self.collections.insert(column)
            logging.info('finished 【{}】 —— {}'.format(title.encode('utf-8'),url))

            if self.isFirst == True:
                p = Process(target=startNewThread, args=(feedLinkList,))
                p.start()

    def called(self):
        for url in self.urlList:
            try:
                self.run(url)
            except Exception:
                continue

def startNewThread(urlList):
    spider = JrttSpider(urlList,isFirst=False)
    spider.called()

if __name__ == '__main__':
    urlList = [
        'https://www.toutiao.com/a6557871064444043779/',
        'https://www.toutiao.com/a6557884307371721229/',
        'https://www.toutiao.com/item/6510055424719323655/',
        'https://www.toutiao.com/item/6509330340098605575/',
        'https://www.toutiao.com/item/6507810141432185352/'
    ]
    spider = JrttSpider(urlList,isFirst=True)
    spider.called()