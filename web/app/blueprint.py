# encoding:utf-8
from app import app
from app.controller.ParseController import ParseSourceController
from app.controller.parse.ParseExcelControler import ParseExcelControler
from app.controller.upload.UploadController import UploadController
from app.controller.CollectionController import CollectionController
from app.controller.ResultController import ResultController
from app.controller.AbstractionController import AbstractionController
from app.controller.ClassDetailController import ClassDetailController
from app.controller.ParseController import ParseCsvController

from flask_restful import Api

api = Api(app)

api.add_resource(ParseCsvController, '/api/parse/csv')
api.add_resource(ParseSourceController,'/api/parse/source')
api.add_resource(ParseExcelControler,'/api/parse/excel')
api.add_resource(UploadController,'/api/uploads')
api.add_resource(CollectionController,'/api/collections')
api.add_resource(ResultController,'/api/result')
api.add_resource(AbstractionController, '/api/abstractions')
api.add_resource(ClassDetailController, '/api/abstractions/<string:uuid>/<int:number>')
