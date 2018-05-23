# encoding:utf-8
# 采集管理数据库，记录每次采集任务的相关管理信息
from app import db
from datetime import datetime

class CollectionTask(db.Model):
    __tablename__ = 'collection_task_table'
    uuid = db.Column(db.String(36),primary_key=True)
    keywords = db.Column(db.String(256), comment='关键词列表')
    type = db.Column(db.String(64), comment='行业',default='教育')
    source = db.Column(db.String(128), comment='采集提供方')
    name = db.Column(db.String(20), comment='采集人')
    batch_time = db.Column(db.DateTime, comment='上传时间', default=datetime.now)
    abstraction_over = db.Column(db.Boolean, default=False, comment='是否已经处理转换为5W1H')
    save_to_history_over = db.Column(db.Boolean, default=False, comment='是否已经归档')

    file = db.relationship('File', backref='collection', lazy='dynamic')

    def toJsonString(self,hasFile = False):
        baseData = {
            'uuid':self.uuid,
            'keywords':self.keywords,
            'type':self.type,
            'source':self.source,
            'name':self.name,
            'batchTime':str(self.batch_time),
            'abstractionOver':self.abstraction_over,
            'saveToHistoryOver':self.save_to_history_over,
        }
        if hasFile:
            baseData['file'] = [item.toJsonString() for item in self.file]
        return baseData

