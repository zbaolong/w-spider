# encoding: utf-8
from app import app
from app.models.Abstraction import Abstraction
from flask_restful import Resource, reqparse
from app import db
from util.RespEntity import RespEntity
from app.ParamsParser import pagingParser
from sqlalchemy import and_

parser = reqparse.RequestParser()

parser.add_argument('uuid', help='UUID cannot be empty', location='json', type=str, required=True)
parser.add_argument('itemNumber', help='UUID cannot be empty', location='json', type=int, required=True)
parser.add_argument('status', help='', location='json', type=str, required=True)

class AbstractionController(Resource):

    def get(self):
        args = pagingParser.parse_args()
        pagination = Abstraction.query.paginate(
            page=args.get('offset'), per_page=args.get('count'),
            error_out=False
        )
        items = pagination.items
        return RespEntity.success([item.toJsonString() for item in items])

    def put(self):
        """
        该接口用于标注此文章面向的人群类型
        :return:
        """
        json = parser.parse_args()
        abs = Abstraction.query.filter(
            and_(
                Abstraction.uuid == json.get('uuid'),
                Abstraction.item_number == json.get('itemNumber')
            )
        ).first()
        abs.class_by_user = json.get('status')
        db.session.add(abs)
        db.session.commit()
        return RespEntity.success(abs.toJsonString())
