# encoding:utf-8
from spider.util.DataFormateUtil import DataFormateUtil
import json
import logging
import HTMLParser
from multiprocessing import Process
from lxml import etree
import xlrd
import requests
import PyV8
from pymongo import MongoClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReadExcel(object):

    @staticmethod
    def called():
        excel = xlrd.open_workbook('data2.xls')
        sh = excel.sheet_by_index(0)
        rowCount = sh.nrows
        logging.info("Read excel successful, a total of {} rows".format(rowCount))
        list = []
        for i in range(1, rowCount):
            data = {
                'index': '',
                'url': '',
                'source': '',
                'category': '',
                'facedgroup': '',
                'uploader':''
            }
            Data1 = sh.cell(i, 0).value
            data['index'] = int(Data1)
            Data2 = sh.cell(i, 1).value
            data['url'] = Data2
            Data3 = sh.cell(i, 2).value
            data['source'] = Data3
            Data4 = sh.cell(i, 3).value
            data['category'] = Data4
            Data5 = sh.cell(i, 4).value
            data['facedgroup'] = Data5
            Data5 = sh.cell(i, 5).value
            data['uploader'] = Data5
            list.append(data)
        return list

class JrttSpider(object):

    def __init__(self,sourceDataList,isFirst,recSource):
        """
        :param urlList: 解析的URL列表
        :param isFirst: 是否为第一次爬取（非推荐URL）
        :param recSource: 推荐来源，若为第一次爬取，则为None
        """
        self.isFirst = isFirst
        self.sourceDataList = sourceDataList
        self.recSource = recSource
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
        html = HTMLParser.HTMLParser().unescape(content)
        element = etree.HTML(html)
        imgUrlList = element.xpath('//img/@src')
        return imgUrlList,len(imgUrlList)

    def run(self,sourceData):
        if sourceData == None:
            return
        else:
            url = sourceData.get('url')
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
            imgUrlList,imgCount = self.parseContent(content)  # 解析出图片的链接和图片的数量

            column = {
                'title': title,
                'content': content,
                'imgUrlList':imgUrlList,
                'imgCount':imgCount,
                'description': description,
                'author': author,
                'publishTime': publishTime,
                'category': category,
                'tags': tags,
                'keywords': str(keywords.encode('utf-8')).split(','),
                'feedLinkList': feedLinkList,
                'source':sourceData.get('source'),
                'sourceIndex': sourceData.get('index'),
                'sourceUrl':url,
                'sourceCategory':sourceData.get('category'),
                'sourceFacedgroup':sourceData.get('facedgroup'),
                'sourceUploader':sourceData.get('uploader'),
                'isVerified': 0,
                'isRecommended': 0 if self.isFirst == True else 1,  # 是否为原始还是推荐的
                'recSource': self.recSource, # 推荐的来源
                'readers': [],
                'readNum': long(0)
            }
            self.collections.insert(column)
            logging.info('finished 【{}】 —— {}'.format(title.encode('utf-8'),url))

            if self.isFirst == True:
                feedInfoList = []
                for item in feedLinkList:
                    dict = {
                        'index': sourceData.get('index'),
                        'url': item,
                        'source': sourceData.get('source'),
                        'category': sourceData.get('category'),
                        'facedgroup': sourceData.get('facedgroup'),
                        'uploader':sourceData.get('uploader')
                    }
                    feedInfoList.append(dict)
                p = Process(target=startNewThread, args=(feedInfoList,url))
                p.start()

    def called(self):
        for sourceData in self.sourceDataList:
            try:
                self.run(sourceData)
            except Exception:
                continue

def startNewThread(urlList,recSource):
    spider = JrttSpider(
        urlList, isFirst=False, recSource=recSource
    )
    spider.called()

if __name__ == '__main__':
    urlList = [
        'https://www.toutiao.com/a6557871064444043779/',
        # 'https://www.toutiao.com/a6557884307371721229/',
        # 'https://www.toutiao.com/item/6510055424719323655/',
        # 'https://www.toutiao.com/item/6509330340098605575/',
        # 'https://www.toutiao.com/item/6507810141432185352/'
    ]
    sourceDataList = ReadExcel.called()
    spider = JrttSpider(
        sourceDataList, isFirst=True, recSource=None
    )
    spider.called()