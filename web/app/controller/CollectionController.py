# encoding:utf-8
from app.models.CollectionTask import CollectionTask
from util.RespEntity import RespEntity
from app.ParamsParser import pagingParser
from flask_restful import Resource

class CollectionController(Resource):

    def get(self):
        args = pagingParser.parse_args()
        result = CollectionTask.query.paginate(
            args.get('offset'), per_page=args.get('count'),
            error_out=False
        ).items
        collections = [item.toJsonString(hasFile=False) for item in result]
        return RespEntity.success(collections)