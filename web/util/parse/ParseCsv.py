# encoding:utf-8
import csv

class ParseCsv(object):

    def __init__(self,path):
        self.path = path

    def called(self):
        csvFile = open(str(self.path))
        reader = csv.reader(csvFile)
        return reader

if __name__ == '__main__':
    p = ParseCsv('/static/182af1b89a371a705244da5b600ffa1d.csv')
    p.called()