# encoding:utf-8
from app.models.CollectionTask import CollectionTask
from util.RespEntity import RespEntity
from flask_restful import Resource,reqparse

parser = reqparse.RequestParser()
parser.add_argument('offset', help='',location='args', required = True, type = int)
parser.add_argument('count', help='',location='args', required = True, type = int)

class CollectionController(Resource):

    def get(self):
        args = parser.parse_args()
        result = CollectionTask.query.paginate(
            args.get('offset'), per_page=args.get('count'),
            error_out=False
        ).items
        collections = [item.toJsonString(hasFile=False) for item in result]
        return RespEntity.success(collections)