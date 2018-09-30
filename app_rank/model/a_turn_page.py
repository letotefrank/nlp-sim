from flask import request, jsonify
import json
import config


# 前端a标签跳转接口
def a_turn_page():
    page_name = request.args.get("page")
    return page_name


# 返回前端对应的json文件接口
def get_json():
    json_name = request.args.get("jsonName")
    file = config.json_path + json_name
    with open(file) as f:
        json_file = json.load(f)
        resp = jsonify({json_name: json_file})
        return resp
