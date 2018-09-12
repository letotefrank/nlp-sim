import pandas as pd
import numpy as np
import os
import jieba
import fastText as ft
import config
import json
from app.utils.utils import stop_words, jb_text, similarity
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import pearsonr

from flask import jsonify, request

jieba.load_userdict('{}local_dict'.format(config.stop_words_path))

id_url_df = pd.read_csv(os.path.join(config.data_path, 'id_url.csv'))
# model = ft.load_model('{}wiki.zh.bin'.format(config.model_path))
model = ft.load_model('{}local_model.bin'.format(config.model_path))


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

    u_vector = model.get_sentence_vector(''.join(i for i in pre_data))
    with open('{}/id_vec_dict.json'.format(config.model_path), 'r') as rf:
        id_vec_dict = json.load(rf)
    sims = []
    ids = []
    for pid, vec in id_vec_dict.items():
        ids.append(pid)

        # sim = similarity(u_vector, vec)
        # sims.append(sim)

        # ed_sim = float(euclidean_distances([vec], [u_vector]))
        # sims.append(ed_sim)

        # pers
        pers_sim = pearsonr(vec, u_vector)
        sims.append(pers_sim[0])

    dict_d = {'pid': ids, 'sim_data': sims}
    sims_df = pd.DataFrame(dict_d)
    sims_df = sims_df.join(id_url_df)
    sims_df = sims_df.sort_values(by=['sim_data'], ascending=False)
    sims_df = sims_df.reset_index(drop=True)
    pids = sims_df.iloc[0:sim_num]['pid'].values.tolist()
    urls = sims_df.iloc[0:sim_num]['url'].values.tolist()
    results = [pids, urls]
    # print('api2的结果是{}'.format(results))
    return jsonify({'text_pid_url': results,
                    'rec_num': sim_num
                    })
