# encoding: utf-8
from app.models.Abstraction import Abstraction
from flask_restful import Resource, reqparse
from app import db
from util.ErrorTemplate import *
from app.parser import pagingParser
from sqlalchemy import and_

parser = reqparse.RequestParser()

parser.add_argument('uuid', help='Primary key cannot be empty', location='json', type=str, required=True)
parser.add_argument('itemNumber', help='ItemNumber cannot be empty', location='json', type=int, required=True)
parser.add_argument('class', help='', location='json', type=str, required=True)

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
        """
        json = parser.parse_args()
        abs = Abstraction.query.filter(
            and_(
                Abstraction.uuid == json.get('uuid'),
                Abstraction.item_number == json.get('itemNumber')
            )
        ).first()
        if not abs:
            return InstanceNotFoundError()
        abs.class_by_user = json.get('class')
        db.session.add(abs)
        db.session.commit()
        return RespEntity.success(abs.toJsonString())

class AbsDetailController(Resource):

    def get(self,uuid,number):
        """
        查看某条元数据的详细信息
        :param uuid: 采集任务序列号
        :param number: 条目序号
        """
        abs = Abstraction.query.filter(
            and_(
                Abstraction.uuid == uuid,
                Abstraction.item_number == number
            )
        ).first()
        if not abs:
            return InstanceNotFoundError()
        return RespEntity.success(
            abs.toJsonString(hasAll=True)
        )