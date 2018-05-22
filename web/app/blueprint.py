# encoding:utf-8
from app import app
from app.controller.ParseController import ParseCsvController
from app.controller.ParseController import ParseSourceController
from app.controller.ParseExcelControler import ParseExcelControler
from app.controller.UploadController import UploadController
from flask_restful import Api

api = Api(app)

api.add_resource(ParseCsvController,'/parse/csv')
api.add_resource(ParseSourceController,'/parse/source')
api.add_resource(ParseExcelControler,'/parse/excel')
api.add_resource(UploadController,'/uploads')
