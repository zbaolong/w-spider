# encoding:utf-8
# 元数据库，记录每次采集完成后，导出数据转换为5W1H 结构
from app import db

class Abstraction(db.Model):
    __tablename__ = 'abstraction_table'
    uuid = db.Column(db.String(36),primary_key=True)
    item_number = db.Column(db.Integer, comment='条目序号')
    why = db.Column(db.String(256), comment='标题')
    what = db.Column(db.String(1024), comment='摘要')
    who = db.Column(db.String(256), comment='作者')
    when = db.Column(db.DateTime, comment='发布日期')
    where = db.Column(db.String(128), comment='内容提供方')
    how = db.Column(db.String(1024), comment='来源，新闻详情链接')
    parse_source = db.Column(db.Text, comment='用于内容解析源代码')
    picture = db.Column(db.String(1024), comment='封面图')
    category = db.Column(db.String(64), comment='分类')
    tag = db.Column(db.String(256), comment='标签')
    detail_over = db.Column(db.Boolean,default=False, comment='是否已经完成网页解析')
    save_to_history_over = db.Column(db.Boolean,default=False, comment='是否已经归档')
    whole_content_check_over = db.Column(db.Boolean,default=False, comment='是否整个内容可用')


    def toJsonString(self):
        return {
            'uuid':self.uuid,
            'itemNumber':self.item_number,
            'why':self.what,
            'what':self.what,
            'who':self.who,
            'when':self.when,
            'where':self.where,
            'how':self.how,
            'picture':self.picture,
            'category':self.category,
            'tag':self.tag,
            'detailOver':self.detail_over,
            'saveToHistoryOver':self.save_to_history_over,
            'wholeContentCheckOver':self.whole_content_check_over
        }