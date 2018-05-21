# encoding:utf-8
# 分类数据库，记录每一个条目的分类统计情况
from app import db

class Analysis(db.Model):
    __tablename__ = 'analysis_table'
    uuid = db.Column(db.String(36),primary_key=True)
    item_number = db.Column(db.Integer)
    item_total_size = db.Column(db.Integer)
    visited_number = db.Column(db.Integer)
    clicked_number = db.Column(db.Integer)