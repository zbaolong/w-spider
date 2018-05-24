# encoding:utf-8
from flask_restful import Resource
from app.models.Abstraction import Abstraction
from util.RespEntity import RespEntity
from sqlalchemy import and_

class ClassDetailController(Resource):

    def get(self,uuid,number):
        abs = Abstraction.query.filter(
            and_(
                Abstraction.uuid == uuid,
                Abstraction.item_number == number
            )
        ).first()
        return RespEntity.success(
            abs.toJsonString(hasAll=True)
        )