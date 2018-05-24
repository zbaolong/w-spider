# encoding:utf-8
# 分类数据库，记录每一个条目的分类统计情况
from app import db

class Analysis(db.Model):
    __tablename__ = 'analysis_table'
    uuid = db.Column(db.String(36),primary_key=True)
    item_number = db.Column(db.Integer, comment='条目序号', primary_key=True)
    item_total_size = db.Column(db.Integer, comment='内容文本总长度')
    visited_number = db.Column(db.Integer, comment='访问次数')
    clicked_number = db.Column(db.Integer, comment='点击次数')
    better_number = db.Column(db.Integer, comment='点赞次数')
    class_result = db.Column(db.String(64), comment='分类结果')

    def toJsonString(self):
        return {
            'uuid':self.uuid,
            'itemNumber':self.item_number,
            'itemTotalSize':self.item_total_size,
            'visitedNumber':self.visited_number,
            'clickedNumber':self.clicked_number,
            'betterNumber':self.better_number,
            'classResult':self.class_result
        }