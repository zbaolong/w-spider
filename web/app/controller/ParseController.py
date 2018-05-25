# encoding:utf-8
from app import db
from util.RespEntity import RespEntity
from util.parse.ParseCsv import ParseCsv
from util.DataFormateUtil import DataFormateUtil
from app.models.Abstraction import Abstraction
from app.models.CollectionTask import CollectionTask
from flask_restful import Resource, reqparse
from app.models.Detail import Detail
import re
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('uuid', help='UUID cannot be empty',location='json',type=str,required = True)

class ParseCsvController(Resource):

    def post(self):
        json = parser.parse_args()
        collection = CollectionTask.query.filter(CollectionTask.uuid == json.get('uuid')).first()
        reader = ParseCsv(collection.file[0].addr).called()
        index = 0
        for item in list(reader):
            if index == 0:
                pass
            else:
                when = DataFormateUtil.stringToDateTime(item[3])
                if item[0] != '':  # 判断标题是否为空
                    abs = Abstraction(
                        uuid = collection.uuid,
                        why = item[0],
                        what = item[1],
                        who = item[2],
                        when = when,
                        whole = item[4],
                        tag = item[5],
                        category = item[6],
                        how = item[7],
                        item_number = index
                    )
                    db.session.add(abs)
            index += 1

        collection.abstraction_over = True  # 已经处理转换为5W1H
        collection.save_to_history_over = True # 已归档
        db.session.add(collection)
        db.session.commit()
        return RespEntity().success(collection.toJsonString())

class ParseSourceController(Resource):

    def post(self):
        """
        该接口用于客户端请求Abstraction的uuid，解析whole字段的源代码内容。并将解析出的数据存储到detail_table表中
        :return:
        """
        json = parser.parse_args()
        abs = Abstraction.query.filter(Abstraction.uuid == json.get('uuid')).first()
        print (abs.uuid)
        body = re.findall('<p>(.*?)</p>',abs.whole) #匹配所有p标签
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
            print(paragraph_type)
            detail = Detail(
                uuid=abs.uuid,
                item_number=index+1,
                type='',
                paragraph_number=index+1,
                paragraph_type=paragraph_type,
                paragraph_content=end,
            )
            index += 1

            db.session.add(detail)
            db.session.commit()

        return jsonify(data=detail)