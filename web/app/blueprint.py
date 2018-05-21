# encoding:utf-8
from app import app
from app.controller.CsvController import CsvController
from app.controller.UploadController import UploadController
from flask_restful import Api

api = Api(app)

api.add_resource(CsvController,'/parse')
api.add_resource(UploadController,'/uploads')