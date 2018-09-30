# -*- coding: utf-8 -*-
from flask import render_template
from app_rank.model import fit_model, a_turn_page
from app_rank import app_rank


# Home Page
@app_rank.route("/")
def index():
    return render_template("ancestrytype_clothing.html")


# a 跳转控制
@app_rank.route("/a_turn", methods=['GET', 'POST'])
def a_turn():
    page = a_turn_page.a_turn_page()
    return render_template(page)


# 训练model
@app_rank.route("/fit_rank", methods=['GET', 'POST'])
def sim_by_pid():
    return fit_model.fit_rank()


# 前端json 加载控制
@app_rank.route("/getJson", methods=['GET', 'POST'])
def get_json():
    return a_turn_page.get_json()
