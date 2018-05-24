# encoding:utf-8
from app import app
from app.controller.ParseController import ParseCsvController
from app.controller.ParseController import ParseSourceController
from app.controller.ParseExcelControler import ParseExcelControler
from app.controller.UploadController import UploadController
from app.controller.CollectionController import CollectionController
from app.controller.ClassController import ModifyStatusController
from app.controller.ParseController import ParseCsvController

from flask_restful import Api

api = Api(app)

api.add_resource(ParseCsvController, '/api/parse/csv')
api.add_resource(ParseSourceController,'/api/parse/source')
api.add_resource(ParseExcelControler,'/api/parse/excel')
api.add_resource(UploadController,'/api/uploads')
api.add_resource(CollectionController,'/api/collections')
api.add_resource(ModifyStatusController, '/api/modify/state')
