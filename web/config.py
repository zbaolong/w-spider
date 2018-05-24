import os

DEBUG = True
SECRET_KEY = os.urandom(24)

UPLOADED_FILES_DEST = '/static'

DEFAULT_MAX_PAGE_COUNT = 10

DATEBASE_USERNAME = 'root'
DATEBASE_PASSWORD = '123456'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '3306'
DATABASE_NAME = 'wspider'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8" .format(DATEBASE_USERNAME,
                               DATEBASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)