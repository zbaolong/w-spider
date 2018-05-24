# encoding:utf-8
from flask_restful import Resource,reqparse
from app.models.Analysis import Analysis
from util.RespEntity import RespEntity

parser = reqparse.RequestParser()
parser.add_argument('offset', help='',location='args', required = True, type = int)
parser.add_argument('count', help='',location='args', required = True, type = int)

class ResultController(Resource):

    def get(self):
        args = parser.parse_args()
        analysis = [item.toJsonString() for item in Analysis.query.all()]
        return RespEntity.success(analysis)