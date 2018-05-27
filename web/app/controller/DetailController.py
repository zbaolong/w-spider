# encoding:utf-8
from app import db
from util.RespEntity import RespEntity
from app.models.Detail import Detail
from sqlalchemy import and_
from flask_restful import Resource, reqparse
from flask import request

class DetailController(Resource):

    def put(self,uuid,itemNumber,pnNumber):
        """
        更改某个元数据解析后的段落信息
        """
        detail = Detail.query.filter(and_(
            uuid == uuid,
            Detail.item_number == itemNumber,
            Detail.paragraph_number == pnNumber
        )).first()
        detail.paragraph_content = request.json.get('paragraphContent')
        db.session.commit()
        return RespEntity.success(
            detail.toJsonString()
        )


    def delete(self,uuid,itemNumber,pnNumber):
        """
        删除某条元数据解析后的段落信息
        """
        detail = Detail.query.filter(and_(
            uuid == uuid,
            Detail.item_number == itemNumber,
            Detail.paragraph_number == pnNumber
        )).first()
        detail.is_deprecated = True  # 修改该段落为不可用
        db.session.commit()
        return RespEntity.success()