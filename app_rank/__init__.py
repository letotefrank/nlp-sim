# coding:utf-8

from flask import Flask
from flask_cors import *

app_rank = Flask(__name__)
CORS(app_rank, allow_headers='Access-Control-Allow-Origin', supports_credentials=True)

from app_rank.view import views
