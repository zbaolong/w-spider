# encoding:utf-8
from flask_restful import Resource,reqparse
from app.models.Analysis import Analysis
from app.parser import pagingParser
from util.RespEntity import RespEntity

class ResultController(Resource):

    def get(self):
        args = pagingParser.parse_args()
        items = Analysis.query.paginate(
            args.get('offset'), per_page=args.get('count'),
            error_out=False
        ).items
        return RespEntity.success(
            [item.toJsonString() for item in items]
        )

class ResultDetailController(Resource):

    def get(self,uuid):
        ans = Analysis.query.filter(Analysis.uuid == uuid).first()
        return RespEntity.success(
            ans.toJsonString(hasParagraph=True)
        )