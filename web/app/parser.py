# encoding:utf-8
from app import app
from flask_restful import reqparse

# 分页参数解析
pagingParser = reqparse.RequestParser()
pagingParser.add_argument('offset', help='', location='args', type=int, default=1)
pagingParser.add_argument('count', help='', location='args', type=int, default=app.config.get('DEFAULT_MAX_PAGE_COUNT'))