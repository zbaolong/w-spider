# encoding:utf-8
from app import db
from app import files
from app.models.CollectionTask import CollectionTask
import hashlib, time
import uuid
from flask_restful import Resource, reqparse
from flask import request

class UploadController(Resource):

    def post(self):
        hash = hashlib.md5((str(time.time())).encode('utf-8')).hexdigest()
        files.save(request.files['file'],name='{}.'.format(hash))
        collection = CollectionTask(
            uuid = str(uuid.uuid4()),
            keywords = '',
            type = '',
            source = '',
            name = ''
        )
        db.session.add(collection)
        db.session.commit()
        return {
            'data': None,
            'message': '',
            'code':200
        }