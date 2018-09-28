# -*- coding: utf-8 -*-
from flask import render_template
from app_rank.model import fit_model
from app_rank import app_rank


@app_rank.route("/")
def index():
    return render_template("index.html")


@app_rank.route("/fit_rank", methods=['GET', 'POST'])
def sim_by_pid():
    return fit_model.fit_rank()
