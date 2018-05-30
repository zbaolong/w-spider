# encoding:utf-8
from app import db

class AbstractionHistory(db.Model):
    __tablename__ = 'abstraction_history_table'
    uuid = db.Column(db.String(36), primary_key=True)
    item_number = db.Column(db.Integer, comment='条目序号', primary_key=True)
    why = db.Column(db.String(256), comment='标题')
    what = db.Column(db.String(1024), comment='摘要')
    who = db.Column(db.String(256), comment='作者')
    when = db.Column(db.DateTime, comment='发布日期')
    where = db.Column(db.String(128), comment='内容提供方')
    how = db.Column(db.String(1024), comment='来源，新闻详情链接')
    whole = db.Column(db.Text, comment='用于内容解析源代码')
    content = db.Column(db.Text, comment='内容文字')
    picture = db.Column(db.String(1024), comment='封面图')
    category = db.Column(db.String(64), comment='分类')
    tag = db.Column(db.String(256), comment='标签')
    class_by_user = db.Column(db.String(256), comment='用户标注的面向人群类型')

    def toJsonString(self,hasAll = False):
        baseData = {
            'uuid':self.uuid,
            'itemNumber':self.item_number,
            'why':self.what,
            'what':self.what,
            'who':self.who,
            'when':str(self.when),
            'where':self.where,
            'how':self.how,
            'picture':self.picture,
            'category':self.category,
            'tag':self.tag,
            'classByUser': self.class_by_user
        }
        if hasAll:
            baseData['content'] = self.content
            baseData['whole'] = self.whole
        return baseData