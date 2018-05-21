from app import app,db
from flask import render_template,redirect,url_for,request,jsonify,abort

@app.route('/')
def index():
    return "hello world"