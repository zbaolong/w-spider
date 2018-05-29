# encoding:utf-8
from app import db
from util.parse.ParseCsv import ParseCsv
from util.ErrorTemplate import *
from app.models.Abstraction import Abstraction
from app.models.CollectionTask import CollectionTask
from app.models.Detail import Detail
from app.models.Analysis import Analysis
from datetime import datetime
import re
from bs4 import BeautifulSoup
from flask_restful import Resource, reqparse
from sqlalchemy import and_

parser = reqparse.RequestParser()
parser.add_argument('uuid', help='Primary key cannot be empty',location='json',type=str,required = True)

parser2 = reqparse.RequestParser()
parser2.add_argument('uuid', help='Primary key cannot be empty',location='json',type=str,required = True)
parser2.add_argument('itemNumber', help='Itemnumber cannot be empty',location='json',type=int,required = True)

class ParseCsvController(Resource):

    def post(self):
        json = parser.parse_args()
        abs = Abstraction.query.filter(Abstraction.uuid == json.get('uuid')).first()
        print abs
        if abs:
            return InstanceExistsError()
        collection = CollectionTask.query.filter(CollectionTask.uuid == json.get('uuid')).first()
        print collection
        reader = ParseCsv(collection.file[0].addr).called()
        index = 0
        for item in list(reader):
            if index == 0:
                pass
            else:
                # when = DataFormateUtil.stringToDateTime(item[3])
                when = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item[0] != '':  # 判断标题是否为空

                    if item[4] is not None:
                        what = item[4]
                    else:
                        # 得到摘要
                        soup = BeautifulSoup(item[5], 'lxml')
                        p_list = soup.find_all('p')
                        if p_list[0].img:
                            what = p_list[0].img.get('alt')
                        else:
                            what = p_list[0].text
                    abs = Abstraction(
                        uuid = collection.uuid,
                        why = item[1],
                        what = what,
                        who = item[2],
                        when = when,
                        whole = item[5],
                        tag = item[7],
                        content = item[6],
                        category = item[8],
                        how = item[0],
                        item_number = index
                    )
                    db.session.add(abs)
            index += 1

        collection.abstraction_over = True  # 已经处理转换为5W1H
        collection.save_to_history_over = True # 已归档
        db.session.delete(collection)
        db.session.add(collection)
        db.session.commit()
        return RespEntity().success(collection.toJsonString())


class ParseSourceController(Resource):

    def post(self):
        """
        该接口用于客户端请求Abstraction的uuid，解析whole字段的源代码内容。并将解析出的数据存储到detail_table表中
        :return:
        """
        json = parser2.parse_args()
        abs = Abstraction.query.filter(
            and_(Abstraction.uuid == json.get('uuid'),
                 Abstraction.item_number == json.get('itemNumber')
        )).first()
        if not abs:
            return InstanceNotFoundError()
        body = re.findall('<p>(.*?)</p>',abs.whole) # 匹配所有p标签
        article_type = u'文字'
        if 'http' in abs.whole:  # 判断文章类型
            article_type = u'混合'
        index = 0
        for each in body:  # 遍历p标签，找到所有的图片url
            img_url = ''
            # image_url_list = re.findall('<img src=""(.*?)""|<a href=""(.*?)"">', each)
            image_url_list = re.findall('<img src=\"(.*?)"', each)
            if len(image_url_list) != 0:
                img_url = image_url_list[0]
            text = re.sub('<strong>|</strong>', '', each)
            txt = re.sub('<img(.*?)>|<a href=""(.*?)"">', img_url, text)  # 将图片url替换为正确格式
            end = re.sub('    <style>(.*?)</style>    ', '', txt)  # 移除<style>···</style>
            if end.find('http')+1:
                paragraph_type = u'图片'
            else:
                paragraph_type = u'文字'
            detail = Detail(
                uuid=abs.uuid,
                item_number=abs.item_number,
                type=article_type,
                paragraph_number=index+1,
                paragraph_type=paragraph_type,
                paragraph_content=end,
            )
            index += 1
            db.session.add(detail)
        db.session.delete(abs)

        analysis = Analysis(
            uuid = abs.uuid
        )
        db.session.add(analysis)
        db.session.commit()
        return RespEntity.success('success')
