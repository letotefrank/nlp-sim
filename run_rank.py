#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    作者:     Frank
    版本:     1.0
    日期:     2018/09/05
    文件名:    app.py
    功能：     主程序
    任务：1. nlp_rec
"""
from app_rank import app_rank
from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 8081), app_rank).serve_forever()
