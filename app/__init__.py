# coding:utf-8

from flask import Flask
from flask_cors import *

app = Flask(__name__)
CORS(app, allow_headers='Access-Control-Allow-Origin', supports_credentials=True)

from app.view import views
