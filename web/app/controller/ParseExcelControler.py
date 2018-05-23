# encoding:utf-8
from app import db
from flask_restful import Resource, reqparse

class ParseExcelControler(Resource):

    def post(self):
        return 'ok'