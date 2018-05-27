# encoding:utf-8
# 分类数据库，记录每一个条目的分类统计情况
from app import db
from app.models.Detail import Detail
from app.models.Abstraction import Abstraction
from sqlalchemy import and_

class Analysis(db.Model):
    __tablename__ = 'analysis_table'
    uuid = db.Column(db.String(36),primary_key=True)
    item_number = db.Column(db.Integer, comment='条目序号', primary_key=True)
    item_total_size = db.Column(db.Integer, comment='内容文本总长度', default=0)
    visited_number = db.Column(db.Integer, comment='访问次数', default=0)
    clicked_number = db.Column(db.Integer, comment='点击次数', default=0)
    better_number = db.Column(db.Integer, comment='点赞次数', default=0)
    class_result = db.Column(db.String(64), comment='分类结果')

    def toJsonString(self,hasParagraph=False):
        abs = Abstraction.query.filter(
            and_(Abstraction.uuid == self.uuid, Abstraction.item_number == self.item_number)
        ).first()
        baseData = {
            'uuid':self.uuid,
            'itemNumber':self.item_number,
            'itemTotalSize':len(self.getParagraphData()),
            'visitedNumber':self.visited_number,
            'clickedNumber':self.clicked_number,
            'betterNumber':self.better_number,
            'classResult':self.class_result,
            'title':abs.why   # 解析结果所属文章的标题
        }
        if hasParagraph:
            baseData['paragraph'] = self.getParagraphData()
        return baseData

    def getParagraphData(self):
        details = Detail.query.filter(Detail.uuid == self.uuid).all()
        return [item.toJsonString() for item in details]