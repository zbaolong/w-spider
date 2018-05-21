# encoding:utf-8

class RespEntity():

    @staticmethod
    def called(code,msg,data):
        return {
            'data': data,
            'message': msg,
            'code': code
        }

    @staticmethod
    def success(data):
        return {
            'data': data,
            'message': '',
            'code': 200
        }

    @staticmethod
    def error(code,msg):
        return {
            'data': None,
            'message': msg,
            'code': code
        }