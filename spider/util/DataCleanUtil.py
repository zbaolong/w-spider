# encoding:utf-8

class DataCleanUtil:

    @staticmethod
    def listJoinToStringBynewline(list):
        return '\n'.join(list)

    @staticmethod
    def sliceByColon(value):
        colonIndex = value.find("：")
        return value[colonIndex+1:]

    @staticmethod
    def replaceEquaSign(value):
        return value.replace('&#x3D;','=')


if __name__ == '__main__':
    pass