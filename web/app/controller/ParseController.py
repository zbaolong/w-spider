# encoding:utf-8
from app import db
from util.RespEntity import RespEntity
from util.parse.ParseCsv import ParseCsv
from spider.util.DataFormateUtil import DataFormateUtil
from app.models.Abstraction import Abstraction
from app.models.CollectionTask import CollectionTask
import uuid
from flask_restful import Resource, reqparse

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
                        uuid=str(uuid.uuid4()),
                        why=item[0],
                        what = item[1],
                        who = item[2],
                        when = when,
                        parse_source = item[4],
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
        print abs.whole
        return RespEntity.success('')