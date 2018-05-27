# encoding:utf-8
from flask_restful import Resource

class DetailController(Resource):

    def put(self,uuid,itemNumber,pnNumber):
        """
        更改某个元数据解析后的段落信息
        :param uuid:
        :param itemNumber:
        :param pnNumber:
        :return:
        """
        pass

    def delete(self,uuid,itemNumber,pnNumber):
        """
        删除某条元数据解析后的段落信息
        :param uuid:
        :param itemNumber:
        :param pnNumber:
        :return:
        """
        pass