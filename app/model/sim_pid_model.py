import pandas as pd
import os
import jieba
import fastText as ft
import config
import json
from app.utils.utils import get_sims
from app.model.vision_sim_model import vision_sim
from flask import jsonify, request

jieba.load_userdict('{}local_dict'.format(config.stop_words_path))

model = ft.load_model('{}local_model.bin'.format(config.model_path))
# model = ft.load_model('{}wiki.zh.bin'.format(config.model_path))
id_url_df = pd.read_csv(os.path.join(config.data_path, 'id_url.csv'))


def get_by_pid():
    # 存放相似矩阵，为analysis提供数据
    # 第一列为主pid,以行为单位，每行为一个主id的相似序列
    sim_ids = []
    data = request.get_data().decode('utf-8')

    # req_data = json.loads(data)
    # pid = int(req_data['pid'])
    # sim_num = int(req_data['rec_num'])
    # end_flag = int(req_data['end_flag'])
    # print(pid)

    pid = int(request.args.get("pid"))
    sim_num = int(request.args.get("rec_num"))
    end_flag = int(request.args.get("end_flag"))

    # vision接入
    pids, urls = vision_sim(pid, sim_num)

    with open('{}/id_vec_dict.json'.format(config.model_path), 'r') as rf:
        id_vec_dict = json.load(rf)

    # 得到pid对应的sim_num个相似商品
    sim_product_list = get_sims(id_vec_dict, id_url_df, sim_num, pid)

    # append vision
    sim_product_list.append(urls)
    sim_product_list.append(pids)

    # save analysis data ,if end_flag = true
    sim_ids.append(sim_product_list[0])
    if end_flag:
        sim_ids_df = pd.DataFrame(sim_ids)
        sim_ids_df.to_csv('{}/sim_ids_df.csv'.format(config.sim_path), index=False, encoding='UTF-8')

    resp = jsonify({'rec_pid_url': sim_product_list, 'rec_num': sim_num})
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    return resp
