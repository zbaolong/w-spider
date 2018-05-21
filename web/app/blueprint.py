# encoding:utf-8
from app import app
from app.api.CsvController import CsvController
from flask_restful import Api

api = Api(app)

api.add_resource(CsvController,'/parse')