# encoding:utf-8
from app.models.CollectionTask import CollectionTask
from util.RespEntity import RespEntity
from app.parser import pagingParser
from flask_restful import Resource

class CollectionController(Resource):

    def get(self):
        """
        查询所有的采集表中的记录，用于采集的管理和解析
        :return:
        """
        args = pagingParser.parse_args()
        result = CollectionTask.query.paginate(
            args.get('offset'), per_page=args.get('count'),
            error_out=False
        ).items
        collections = [item.toJsonString(hasFile=False) for item in result]
        return RespEntity.success(collections)