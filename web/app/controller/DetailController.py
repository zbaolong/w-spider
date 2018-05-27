# encoding:utf-8
from flask_restful import Resource
from app.models.Detail import Detail
from sqlalchemy import and_
from flask_restful import Resource, reqparse
from app import db
from flask import request


class DetailController(Resource):

    def put(self,uuid,itemNumber,pnNumber):
        """
        更改某个元数据解析后的段落信息
        :param uuid:
        :param itemNumber:
        :param pnNumber:
        :return:
        """
        detail = Detail.query.filter(and_(uuid == uuid,\
                                          Detail.item_number == itemNumber,\
                                          Detail.paragraph_number == pnNumber)).first()
        detail.paragraph_content = request.json.get('paragraph_content')
        db.session.commit()
        return 'put success'


    def delete(self,uuid,itemNumber,pnNumber):
        """
        删除某条元数据解析后的段落信息
        :param uuid:
        :param itemNumber:
        :param pnNumber:
        :return:
        """
        detail = Detail.query.filter(and_(uuid == uuid, \
                                          Detail.item_number == itemNumber, \
                                          Detail.paragraph_number == pnNumber)).first()
        db.session.delete(detail)
        db.session.commit()
        return 'detele success'