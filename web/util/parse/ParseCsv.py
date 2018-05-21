# encoding:utf-8
import csv
import copy

class ParseCsv(object):

    def __init__(self,fileName):
        self.fileName = fileName

    def called(self):
        csvFile = open('E:\\CDIO\\wSpider\\sources\\' + self.fileName)
        reader = csv.reader(csvFile)
        return reader

if __name__ == '__main__':
    p = ParseCsv('data1.csv')
    p.called()