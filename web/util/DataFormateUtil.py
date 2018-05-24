# encoding:utf-8
from datetime import datetime

class DataFormateUtil():

    @staticmethod
    def stringToDateTime(value):
        if value:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            return datetime.now()