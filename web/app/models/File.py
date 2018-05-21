# encoding:utf-8
from app import db
from datetime import datetime

class File(db.Model):
    __tablename__ = 'files'
    uuid = db.Column(db.String(64), primary_key=True)
    file_name = db.Column(db.String(64), comment='源文件名')
    file_name_hash = db.Column(db.String(64), comment='经过HASH处理过的文件名')
    uploader = db.Column(db.String(64), comment='上传人')
    addr = db.Column(db.String(128), comment='文件位置')
    url = db.Column(db.String(128), comment='文件URL')
    upload_time = db.Column(db.DateTime,default=datetime.now, comment='上传时间')

    collection_uuid = db.Column(db.String(36),db.ForeignKey('collection_task_table.uuid'))

    def toJsonString(self):
        return {
            'uuid':self.uuid,
            'fileName':self.file_name,
            'fileNameHash':self.file_name_hash,
            'uploader':self.uploader,
            'addr':self.addr,
            'url':self.url,
            'uploadTime':str(self.upload_time),
            'collectionUUID':self.collection_uuid
        }