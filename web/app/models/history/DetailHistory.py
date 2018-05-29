# encoding:utf-8
from app import db

class DetailHistory(db.Model):
    __tablename__ = 'detail_history_table'
    uuid = db.Column(db.String(36), primary_key=True)
    item_number = db.Column(db.Integer, comment='条目序号', primary_key=True)
    type = db.Column(db.String(64), comment='内容类型，例如文本、图片、混合')
    paragraph_number = db.Column(db.Integer, comment='段落序号', primary_key=True)
    paragraph_type = db.Column(db.String(64), comment='段落类型，文本、图片')
    paragraph_content = db.Column(db.Text, comment='段落内容')

    def toJsonString(self):
        return {
            'uuid':self.uuid,
            'itemNumber':self.item_number,
            'type':self.type,
            'paragraphNumber':self.paragraph_number,
            'paragraphType':self.paragraph_type,
            'paragraphContent':self.paragraph_content
        }