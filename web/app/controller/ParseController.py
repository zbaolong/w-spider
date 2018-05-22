# encoding:utf-8
from datetime import datetime

from app import db
from util.RespEntity import RespEntity
from util.parse.ParseCsv import ParseCsv
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
                try:
                    when = datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    when = datetime.now()
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
                    db.session.commit()
            index += 1
        return RespEntity().success(None)


class ParseSourceController(Resource):

    def post(self):
        json = parser.parse_args()
        abs = Abstraction.query.filter(Abstraction.uuid == json.get('uuid')).first()
        print abs.parse_source
        return RespEntity.success('ok')