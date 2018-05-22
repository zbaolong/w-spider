# encoding:utf-8
from app import db
from app import files
from app.models.CollectionTask import CollectionTask
from app.models.File import File
from util.RespEntity import RespEntity
import hashlib, time
import uuid
from flask_restful import Resource, reqparse
from flask import request

parser = reqparse.RequestParser()
parser.add_argument('name', help='',location='form', required = True)
parser.add_argument('source', help='',location='form', required = True)
parser.add_argument('type', help='',location='form', required = True)

class UploadController(Resource):

    def post(self):
        json = parser.parse_args()
        requestFile = request.files['file']
        hash = hashlib.md5((str(time.time())).encode('utf-8')).hexdigest()
        saveFileName = files.save(requestFile, name='{}.'.format(hash))
        collectionUUID = str(uuid.uuid4())
        collection = CollectionTask(
            uuid = collectionUUID,
            keywords = '',
            type = json.get('type'),
            source = json.get('source'),
            name = json.get('name')
        )
        file = File(
            uuid = str(uuid.uuid4()),
            file_name = requestFile.filename,
            file_name_hash = hash,
            addr = '/static/{}'.format(saveFileName),
            uploader = json.get('name'),
            collection_uuid = collectionUUID
        )
        db.session.add(collection)
        db.session.add(file)
        db.session.commit()
        return RespEntity.success(collection.toJsonString())