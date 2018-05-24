# encoding: utf-8
from app.models.Abstraction import Abstraction
from flask_restful import Resource, reqparse
from app import db
from util.RespEntity import RespEntity
from sqlalchemy import and_
parser = reqparse.RequestParser()
parser.add_argument('uuid', help='UUID cannot be empty', location=['json', 'args'], type=str)
parser.add_argument('itemNumber', help='UUID cannot be empty', location=['json', 'args'], type=str)
parser.add_argument('status', help='', location='json', type=str)
parser.add_argument('page', help='', location='args', type=int)
parser.add_argument('perpage', help='', location='args', type=int)


class ModifyStatusController(Resource):

    def get(self):
        args = parser.parse_args()
        if args.get('uuid') and args.get('itemNumber'):
            abs = Abstraction.query.filter(
                and_(
                    Abstraction.uuid == args.get('uuid'),
                    Abstraction.item_number == args.get('itemNumber')
                )
            ).first()
            return RespEntity.success(abs.toJsonAll())
        else:
            pagination = Abstraction.query.paginate(
                page=args.get('page'), per_page=args.get('perpage'), error_out=False
            )
            items = pagination.items
            return RespEntity.success(
                {
                    'abstractionData':[item.toJsonString() for item in items],
                    'pages': pagination.pages,
                    'count': pagination.total
                }
            )

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
