import pandas as pd
import numpy as np
import os
import jieba
import fastText as ft
import config
import json
from app.utils.utils import stop_words, jb_text, get_sims_text

from flask import jsonify, request

jieba.load_userdict('{}local_dict'.format(config.stop_words_path))

id_url_df = pd.read_csv(os.path.join(config.data_path, 'id_url.csv'))


model = ft.load_model('{}local_model.bin'.format(config.model_path))
# model = ft.load_model('{}wiki.zh.bin'.format(config.model_path))


def get_by_text():
    texts = request.args.get("text")
    sim_num = int(request.args.get("rec_num"))
    # data = request.get_data()
    # req_data = json.loads(data)
    # texts = req_data['text']
    # sim_num = req_data['rec_num']

    # 加载停用词表
    stopwords = stop_words()

    # jieba处理（分词，词性提取，去停用词)
    pre_data = [jb_text(texts, stopwords)]
    np.savetxt('{}pre_data1.txt'.format(config.jb_path), np.array(pre_data), fmt='%s')

    # get 前端输入文本的 sentence-vector
    u_vector = model.get_sentence_vector(''.join(i for i in pre_data))

    # 加载 sentence-vector : {'id':id,'vector':[]}
    with open('{}/id_vec_dict.json'.format(config.model_path), 'r') as rf:
        id_vec_dict = json.load(rf)

    # 得到sim_num个相似商品
    results = get_sims_text(id_vec_dict, id_url_df, u_vector, sim_num)
    return jsonify({'text_pid_url': results,
                    'rec_num': sim_num
                    })
