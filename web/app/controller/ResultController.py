# encoding:utf-8
from flask_restful import Resource,reqparse
from app.models.Analysis import Analysis
from app.ParamsParser import pagingParser
from util.RespEntity import RespEntity

class ResultController(Resource):

    def get(self):
        args = pagingParser.parse_args()
        analysis = [item.toJsonString() for item in Analysis.query.all()]
        return RespEntity.success(analysis)