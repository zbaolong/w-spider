# encoding:utf-8
from app import db
from util.parse.ParseCsv import ParseCsv
from app.models.Abstraction import Abstraction
import uuid
from flask_restful import Resource, reqparse

# parser = reqparse.RequestParser()
# parser.add_argument('rate', help='Rate to charge for this resource',location='args',type=str)

class CsvController(Resource):

    def get(self):
        # args = parser.parse_args()
        reader = ParseCsv('data1.csv').called()
        index = 0
        for item in list(reader):
            if index == 0:
                pass
            else:
                if item[0] != '':  # 判断标题是否为空
                    abs = Abstraction(
                        uuid=str(uuid.uuid4()),
                        why=item[0],
                        category=item[1],
                        picture=item[2],
                        # what=item[4],
                        # when=item[5],
                        tag=item[6],
                        how=item[8],
                        where=item[9],
                        item_number=index
                    )
                    db.session.add(abs)
                    db.session.commit()
            index += 1
        return {'status':'ok'}