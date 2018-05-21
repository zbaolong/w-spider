#encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet,configure_uploads,patch_request_class,DATA,IMAGES
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

files = UploadSet('files',DATA)
configure_uploads(app, files)

from app import models
from app import blueprint