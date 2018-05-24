# encoding:utf-8
from datetime import datetime

class DataFormateUtil():

    @staticmethod
    def stringToDateTime(value):
        try:
            time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except Exception:
            time = datetime.now()
        return time
